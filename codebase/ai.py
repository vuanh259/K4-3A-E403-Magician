import json
import re
from typing import Any
from openai import AsyncOpenAI

from config import settings

SYSTEM_PROMPT = """
Bạn là AI Discord Assistant cho học viên.

Mục tiêu: biến nhiều tin nhắn Discord thành thông tin có thể hành động.

Chỉ tạo item nếu message chứa một trong các nhóm:
- assignment: bài/lab/form/việc cần hoàn thành
- deadline: hạn nộp/hạn hoàn thành
- meeting: lịch họp/workshop/buổi học có thời điểm rõ
- schedule_change: đổi lịch, đổi phòng, hủy/dời buổi

Bỏ qua:
- trò chuyện xã giao
- joke
- cảm ơn
- trao đổi kỹ thuật không tạo hành động mới
- tin thiếu căn cứ đến mức không xác định được hành động

Quy tắc an toàn:
- KHÔNG bịa deadline.
- KHÔNG bịa người gửi, channel, nguồn.
- Nếu không chắc, confidence thấp.
- source_message_id phải đúng với một message đầu vào.
- deadline_iso chỉ điền nếu đủ căn cứ; nếu không thì null.
- reason giải thích ngắn vì sao item quan trọng.

Priority:
- high: deadline gần / việc bắt buộc / thay đổi cần biết ngay.
- medium: cần hành động nhưng chưa gấp.
- low: đáng chú ý nhưng ít cấp bách.

Chỉ trả JSON hợp lệ:
{
  "items": [
    {
      "source_message_id": "string",
      "type": "assignment|deadline|meeting|schedule_change|info",
      "title": "string",
      "action_required": true,
      "deadline_iso": "ISO-8601 hoặc null",
      "priority": "high|medium|low",
      "confidence": 0.0,
      "reason": "string"
    }
  ]
}
""".strip()

def _client() -> AsyncOpenAI:
    if not settings.ai_api_key:
        raise RuntimeError("Thiếu AI_API_KEY trong .env")
    if not settings.ai_model:
        raise RuntimeError("Thiếu AI_MODEL trong .env")
    return AsyncOpenAI(api_key=settings.ai_api_key, base_url=settings.ai_base_url)

def _extract_json(text: str) -> dict[str, Any]:
    text = (text or "{}").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, flags=re.S)
        if not m:
            raise
        return json.loads(m.group(0))

async def analyze_messages(messages: list[dict], current_time_iso: str, timezone_name: str) -> dict:
    client = _client()
    payload = {
        "current_time": current_time_iso,
        "timezone": timezone_name,
        "messages": messages,
    }
    resp = await client.chat.completions.create(
        model=settings.ai_model,
        temperature=0,
        max_tokens=2500,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
    )
    data = _extract_json(resp.choices[0].message.content or "{}")
    if not isinstance(data.get("items"), list):
        data["items"] = []

    source_map = {str(m["message_id"]): m for m in messages}
    safe_items = []
    for item in data["items"]:
        sid = str(item.get("source_message_id", ""))
        src = source_map.get(sid)
        if not src:
            continue  # drop hallucinated sources

        # Re-ground source metadata from trusted input instead of model text.
        item["source_channel"] = src["channel_name"]
        item["source_author"] = src["author"]
        item["source_message"] = src["content"]
        item["source_url"] = src.get("jump_url")
        item["source_message_id"] = sid
        safe_items.append(item)

    data["items"] = safe_items
    return data
