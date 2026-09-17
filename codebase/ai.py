import json
import re
from datetime import datetime
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
- schedule_change: đổi lịch, đổi phòng, dời buổi (kể cả phương án dự phòng có điều kiện), thông báo HỦY hoặc ĐÓNG bài tập/form/buổi học

Bỏ qua (QUAN TRỌNG):
- CÂU HỎI THẮC MẮC của học viên hỏi về deadline/giờ giấc (ví dụ: "Ủa hạn là mấy giờ?", "Có phải tối nay không?"). Tuyệt đối KHÔNG biến câu hỏi thành task hay deadline. Chỉ trích xuất khi là THÔNG BÁO/HƯỚNG DẪN khẳng định.
- Việc ĐÃ HOÀN THÀNH trong quá khứ của cá nhân (ví dụ: "đã nộp xong lúc 9:00 sáng nay").
- Lời than thở, việc riêng cá nhân (ví dụ: "chắc 3h sáng mới xong prototype").
- Trò chuyện xã giao, joke, cảm ơn, rủ rê đi chơi/ăn uống.
- Trao đổi kỹ thuật không tạo hành động mới.
- Tin thiếu căn cứ đến mức không xác định được hành động.

Quy tắc đối với thông báo HỦY / ĐÃ ĐÓNG:
- VẪN TRÍCH XUẤT (gán type: schedule_change, action_required: true) để học viên kịp nắm thông tin (không mất công làm bài hoặc gửi form nữa).
- Tuyệt đối KHÔNG gán deadline_iso (đặt deadline_iso: null) để hệ thống không gửi reminder nhắc việc khi đến giờ.
- reason: giải thích rõ là đã hủy/đóng để không cần nộp hay chuẩn bị nữa.

Quy tắc đối với câu điều kiện / kế hoạch dự phòng:
- VẪN GIỮ và TRÍCH XUẤT các phương án dự phòng/có điều kiện (ví dụ: "Nếu chiều nay mưa thì buổi họp 15:00 dời sang online").
- Đặt action_required: true, giải thích rõ điều kiện phụ thuộc trong reason (ví dụ: "Dời sang online nếu trời mưa, cần theo dõi cập nhật").

Quy tắc tách nhiều hành động / deadline (BẮT BUỘC):
- Mỗi hành động hoặc deadline độc lập phải là MỘT item riêng trong mảng items.
- Nếu một message chứa N nhiệm vụ/mốc hạn khác nhau, phải trả đúng N item, dù các item có cùng source_message_id.
- KHÔNG gộp hai nhiệm vụ hoặc hai deadline vào một title/deadline_iso.
- Ví dụ "Task A hạn 19:30, Task B hạn 21:00 cùng ngày" phải trả 2 item: một item cho Task A lúc 19:30 và một item cho Task B lúc 21:00.

Quy tắc an toàn:
- KHÔNG bịa deadline.
- KHÔNG bịa người gửi, channel, nguồn.
- source_message_id phải đúng với một message đầu vào.
- deadline_iso chỉ điền nếu đủ căn cứ mốc thời gian rõ ràng; nếu không có giờ cụ thể thì đặt null.
- reason giải thích ngắn vì sao item quan trọng.

Quy tắc chấm confidence (0.0 đến 1.0):
- 0.95 - 1.0: Thông báo chính thức, có hạn nộp/thời điểm đầy đủ rõ ràng (ngày + giờ cụ thể).
- 0.80 - 0.90: Kế hoạch dự phòng có điều kiện ("nếu... thì..."), hoặc thông báo hủy/đóng task/buổi học.
- 0.65 - 0.75: Có việc/deadline nhưng mốc thời gian mơ hồ, chưa rõ giờ cụ thể (ví dụ: "tối nay", "ngày mai", "tuần này" mà không nêu rõ giờ).
- Dưới 0.5: Tin đồn, câu hỏi của học viên (BỎ QUA, không trích xuất).

Priority:
- high: thay đổi/đính chính/gia hạn/hủy lịch; đầu việc vận hành khẩn của BTC; Checkpoint 1, form cần BTC tổng hợp hoặc willing users bắt buộc.
- medium: deliverable học tập một lần như lab, spec, quiz, slide/video demo, đọc tài liệu; kể cả khi hạn là tối nay/ngày mai nhưng không phải thông báo thay đổi.
- low: việc định kỳ hoặc hỗ trợ ít khẩn như daily standup, reflection, khảo sát tiến độ chưa có ngày cụ thể.
- Không tự nâng priority lên high chỉ vì có cụm "hôm nay", "tối nay" hoặc "ngày mai"; ưu tiên bản chất nghiệp vụ ở ba quy tắc trên.

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

def _calibrate_priority(content: str, model_priority: Any) -> str:
    """Apply the product's deterministic business-priority policy."""
    lower = (content or "").lower()

    high_markers = [
        "đính chính", "dời", "đổi phòng", "gia hạn", "cập nhật lại",
        "thay vì", "checkpoint 1", "willing users",
        "form khảo sát trải nghiệm",
    ]
    low_markers = [
        "mỗi ngày", "daily standup", "reflection", "khảo sát tiến độ",
    ]
    medium_markers = [
        "lab", "spec", "quiz", "slide", "video demo", "đọc tài liệu",
        "guidebook", "toolkit",
    ]

    if any(marker in lower for marker in high_markers):
        return "high"
    if any(marker in lower for marker in low_markers):
        return "low"
    if any(marker in lower for marker in medium_markers):
        return "medium"
    return model_priority if model_priority in {"high", "medium", "low"} else "medium"

def _expand_multiple_deadline_items(
    items: list[dict], source_map: dict[str, dict], current_time_iso: str
) -> list[dict]:
    """Split a combined LLM item when the source has distinct named deadlines."""
    grouped: dict[str, list[dict]] = {}
    for item in items:
        grouped.setdefault(str(item.get("source_message_id", "")), []).append(item)

    expanded: list[dict] = []
    change_markers = ["đính chính", "gia hạn", "chuyển từ", "thay vì", "cập nhật lại"]
    pair_pattern = re.compile(
        r"\b((?:CP|Checkpoint|Lab|Quiz|Task)\s*\d+)\b[^,.;]{0,100}?\b(\d{1,2}):(\d{2})\b",
        flags=re.I,
    )

    for sid, source_items in grouped.items():
        content = str(source_map.get(sid, {}).get("content", ""))
        lower = content.lower()
        pairs = pair_pattern.findall(content)
        unique_pairs = list(dict.fromkeys((label.strip(), int(hour), int(minute)) for label, hour, minute in pairs))

        if (
            len(unique_pairs) <= 1
            or len(source_items) >= len(unique_pairs)
            or any(marker in lower for marker in change_markers)
        ):
            expanded.extend(source_items)
            continue

        template = source_items[0]
        base_deadline = str(template.get("deadline_iso") or "")
        source_date = re.search(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b", content)
        current_dt = datetime.fromisoformat(current_time_iso.replace("Z", "+00:00"))

        for label, hour, minute in unique_pairs:
            split_item = dict(template)
            split_item["title"] = f"Hạn nộp {label}"
            split_item["type"] = "deadline"
            split_item["action_required"] = True
            split_item["reason"] = f"{label} có deadline riêng lúc {hour:02d}:{minute:02d}."

            if re.search(r"T\d{2}:\d{2}", base_deadline):
                split_item["deadline_iso"] = re.sub(
                    r"T\d{2}:\d{2}", f"T{hour:02d}:{minute:02d}", base_deadline, count=1
                )
            elif source_date:
                day = int(source_date.group(1))
                month = int(source_date.group(2))
                year_text = source_date.group(3)
                year = int(year_text) if year_text else current_dt.year
                if year < 100:
                    year += 2000
                split_item["deadline_iso"] = datetime(
                    year, month, day, hour, minute, tzinfo=current_dt.tzinfo
                ).isoformat()
            else:
                split_item["deadline_iso"] = None

            expanded.append(split_item)

    return expanded

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
        max_tokens=4000,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
    )
    raw_response_text = resp.choices[0].message.content or "{}"

    # CP3: Thiết lập cơ chế ghi vết (logging) cho prompt đầu vào và phản hồi thô của mô hình
    try:
        from pathlib import Path
        from datetime import datetime
        log_file = Path(__file__).resolve().parent.parent / "eval" / "ai_traces.log"
        with open(log_file, "a", encoding="utf-8") as lf:
            lf.write(f"=== [AI TRACE - {datetime.now().isoformat()}] ===\n")
            lf.write(f"MODEL: {settings.ai_model}\n")
            lf.write(f"INPUT PAYLOAD:\n{json.dumps(payload, ensure_ascii=False, indent=2)}\n")
            lf.write(f"RAW LLM RESPONSE:\n{raw_response_text}\n")
            lf.write("=" * 60 + "\n\n")
    except Exception as e:
        print(f"[WARN] Không thể ghi log ai_traces: {e}")

    data = _extract_json(raw_response_text)
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

        # Heuristic calibration for confidence score
        try:
            raw_conf = float(item.get("confidence") if item.get("confidence") is not None else 1.0)
        except (ValueError, TypeError):
            raw_conf = 1.0

        content_lower = str(src.get("content", "")).lower()
        ambiguous_time_markers = ["chưa rõ", "tối nay", "chiều nay", "sáng nay", "ngày mai", "mai ", "tuần này"]
        has_ambiguous_time = any(kw in content_lower for kw in ambiguous_time_markers)
        has_specific_time = bool(re.search(r"\b\d{1,2}(?::\d{2}|h\d{0,2}|\s*giờ)\b", content_lower))

        if has_ambiguous_time and not has_specific_time:
            # Ambiguous deadline without specific hour (e.g. 'tối nay', 'ngày mai')
            # Spec Đường 2: không bịa giờ, hạ confidence xuống 0.70 để hiển thị nhãn cảnh báo
            item["deadline_iso"] = None
            raw_conf = min(raw_conf, 0.70)
        elif any(k in content_lower for k in ["nếu", "dự phòng"]):
            raw_conf = min(raw_conf, 0.85)

        item["priority"] = _calibrate_priority(
            str(src.get("content", "")), item.get("priority")
        )
        item["confidence"] = round(max(0.0, min(1.0, raw_conf)), 2)
        safe_items.append(item)

    data["items"] = _expand_multiple_deadline_items(
        safe_items, source_map, current_time_iso
    )
    return data
