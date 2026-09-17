"""Run the Golden Set through the real LLM extractor and score the output."""

import asyncio
import html
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
EVAL_DIR = Path(__file__).resolve().parent
CODEBASE_DIR = ROOT / "codebase"

# config.py calls load_dotenv() too, but the evaluator is normally launched
# from the repository root while the real secrets live in codebase/.env.
load_dotenv(CODEBASE_DIR / ".env")
sys.path.insert(0, str(CODEBASE_DIR))

from ai import analyze_messages
from config import settings


POSITIVE_ACTIONS = {"EXTRACT", "EXTRACT_WITH_WARNING", "EXTRACT_MULTIPLE"}
PRIORITY_MAP = {"P1": "high", "P2": "medium", "P3": "low"}


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def atomic_write(path: Path, content: str) -> None:
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(content, encoding="utf-8")
    temp_path.replace(path)


def write_json(path: Path, data: Any) -> None:
    atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2))


def md_cell(value: Any) -> str:
    return str(value if value is not None else "—").replace("|", "\\|").replace("\n", " ")


def compact_item(item: dict) -> dict:
    """Keep only model decision fields in eval evidence."""
    return {
        "source_message_id": item.get("source_message_id"),
        "type": item.get("type"),
        "title": item.get("title"),
        "action_required": item.get("action_required"),
        "deadline_iso": item.get("deadline_iso"),
        "priority": item.get("priority"),
        "confidence": item.get("confidence"),
        "reason": item.get("reason"),
    }


def deadline_matches(expected: Any, actual: Any, now: datetime) -> bool:
    """Compare only date/time components explicitly present in the Golden Set."""
    if not expected:
        return True
    if not actual:
        return False

    expected_text = str(expected).lower()
    actual_text = str(actual)

    expected_time = re.search(r"\b(\d{1,2}):(\d{2})\b", expected_text)
    if expected_time:
        hour = int(expected_time.group(1))
        minute = int(expected_time.group(2))
        if not re.search(rf"(?:T|\s){hour:02d}:{minute:02d}(?::|\b)", actual_text):
            return False

    expected_date = re.search(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b", expected_text)
    if expected_date:
        day = int(expected_date.group(1))
        month = int(expected_date.group(2))
        if not re.search(rf"-{month:02d}-{day:02d}(?:T|\s)", actual_text):
            return False
    elif "hôm nay" in expected_text:
        if now.date().isoformat() not in actual_text:
            return False

    return True


def score_case(case: dict, predicted_items: list[dict], now: datetime) -> dict:
    expected_action = case["expected_action"]
    actionable_items = [item for item in predicted_items if item.get("action_required") is True]
    reasons: list[str] = []

    if expected_action not in POSITIVE_ACTIONS:
        passed = len(predicted_items) == 0
        if not passed:
            reasons.append(f"Mong đợi bỏ qua nhưng model trả {len(predicted_items)} item")
    else:
        expected_count = int(case.get("expected_tasks_count", 1))
        actual_count = len(actionable_items)
        passed = actual_count == expected_count
        if actual_count != expected_count:
            reasons.append(f"Số item actionable: mong đợi {expected_count}, thực tế {actual_count}")

        if expected_action == "EXTRACT_WITH_WARNING" and actionable_items:
            invented_deadlines = [item.get("deadline_iso") for item in actionable_items if item.get("deadline_iso")]
            if invented_deadlines:
                passed = False
                reasons.append("Mốc thời gian mơ hồ nhưng model vẫn điền deadline_iso")

        expected_priority = PRIORITY_MAP.get(case.get("expected_priority"))
        if expected_priority and actionable_items:
            actual_priority = actionable_items[0].get("priority")
            if actual_priority != expected_priority:
                passed = False
                reasons.append(
                    f"Priority: mong đợi {expected_priority}, thực tế {actual_priority}"
                )

        expected_deadline = case.get("expected_deadline")
        if (
            expected_action != "EXTRACT_WITH_WARNING"
            and expected_deadline
            and actionable_items
            and re.search(r"\b\d{1,2}:\d{2}\b", str(expected_deadline))
        ):
            actual_deadline = actionable_items[0].get("deadline_iso")
            if not deadline_matches(expected_deadline, actual_deadline, now):
                passed = False
                reasons.append(
                    f"Deadline: mong đợi {expected_deadline}, thực tế {actual_deadline}"
                )

    if not reasons:
        reasons.append("Đáp ứng các tiêu chí tự động của ca kiểm thử")

    return {
        "id": case["id"],
        "layer": case["layer"],
        "ref_id": case.get("ref_id"),
        "is_real_data": bool(case.get("is_real_data")),
        "input_text": case["input_text"],
        "sender": case.get("sender"),
        "expected_action": expected_action,
        "expected_priority": case.get("expected_priority"),
        "expected_deadline": case.get("expected_deadline"),
        "pass_condition": case.get("pass_condition"),
        "predicted_items": [compact_item(item) for item in predicted_items],
        "predicted_items_count": len(predicted_items),
        "predicted_actionable_count": len(actionable_items),
        "passed": passed,
        "reasons": reasons,
    }


def build_markdown(run: dict, metrics: dict, rows: list[dict]) -> str:
    failures = [row for row in rows if not row["passed"]]
    lines = [
        "# BÁO CÁO KẾT QUẢ KIỂM THỬ ĐỊNH LƯỢNG — CP3",
        "",
        "**Dự án:** Discord Action Digest · **Nhóm:** Magician · **Lớp:** 3A · **Phòng:** E403",
        "",
        "> Toàn bộ Golden Set được gửi qua module AI thật trong một request. Kết quả dưới đây được sinh tự động, không gán cứng PASS/FAIL theo mã ca.",
        "",
        "## 1. Thông tin lượt chạy",
        "",
        f"- Thời điểm: `{run['completed_at']}`",
        f"- Model: `{run['model']}`",
        f"- Múi giờ: `{run['timezone']}`",
        f"- Log prompt và phản hồi thô: `eval/ai_traces.log`",
        "",
        "## 2. Tổng hợp kết quả",
        "",
        f"- Tổng số ca: **{metrics['total']}**",
        f"- Số ca đạt: **{metrics['passed']}**",
        f"- Số ca không đạt: **{metrics['failed']}**",
        f"- Tỷ lệ đạt: **{pct(metrics['pass_rate'])}** ({metrics['passed']}/{metrics['total']})",
        f"- Ca từ dữ liệu thật: **{metrics['real_data_cases']}**",
        f"- Tổng item model trả về: **{metrics['predicted_item_count']}**",
        "",
        "### Kết quả theo nhóm",
        "",
        "| Nhóm / lớp | Tổng | Đạt | Tỷ lệ |",
        "|---|---:|---:|---:|",
    ]
    for layer, stats in metrics["layer_breakdown"].items():
        lines.append(
            f"| {md_cell(layer)} | {stats['total']} | {stats['passed']} | {pct(stats['pass_rate'])} |"
        )

    lines.extend(
        [
            "",
            "## 3. Kết quả từng ca",
            "",
            "| ID | Nhóm | Expected | Số item/actionable | Kết quả | Giải thích |",
            "|---|---|---|---:|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                md_cell(value)
                for value in [
                    row["id"],
                    row["layer"],
                    row["expected_action"],
                    f"{row['predicted_items_count']}/{row['predicted_actionable_count']}",
                    "PASS" if row["passed"] else "FAIL",
                    "; ".join(row["reasons"]),
                ]
            )
            + " |"
        )

    lines.extend(["", "## 4. Phân tích các ca thất bại", ""])
    if not failures:
        lines.append("Không có ca thất bại trong lượt chạy này.")
    else:
        for row in failures:
            predicted = row["predicted_items"]
            lines.extend(
                [
                    f"### {row['id']} — {row['layer']}",
                    "",
                    f"- Tiêu chí nghiệm thu: {row['pass_condition']}",
                    f"- Sai lệch: {'; '.join(row['reasons'])}",
                    f"- Đầu ra model: `{json.dumps(predicted, ensure_ascii=False)}`",
                    "",
                ]
            )

    lines.extend(
        [
            "## 5. Quy tắc chấm tự động",
            "",
            "- `EXTRACT`: phải trả đúng một item actionable; nếu Golden Set có priority hoặc deadline cụ thể thì các trường đó cũng phải khớp.",
            "- `EXTRACT_WITH_WARNING`: phải có một item actionable và không tự điền `deadline_iso` khi nguồn thiếu giờ cụ thể.",
            "- `EXTRACT_MULTIPLE`: số item actionable phải bằng `expected_tasks_count`.",
            "- Các ca `OUT_OF_SCOPE`, `IGNORE_NOISE`, `IGNORE_OR_REJECT`, `SECURITY_BLOCK`: model không được tạo item.",
            "",
        ]
    )
    return "\n".join(lines)


def build_html(run: dict, metrics: dict, rows: list[dict]) -> str:
    table_rows = []
    for row in rows:
        css_class = "pass" if row["passed"] else "fail"
        table_rows.append(
            f'<tr class="{css_class}">'
            f"<td>{html.escape(row['id'])}</td>"
            f"<td>{html.escape(str(row['layer']))}</td>"
            f"<td>{html.escape(row['expected_action'])}</td>"
            f"<td>{row['predicted_items_count']}/{row['predicted_actionable_count']}</td>"
            f"<td><b>{'PASS' if row['passed'] else 'FAIL'}</b></td>"
            f"<td>{html.escape('; '.join(row['reasons']))}</td>"
            "</tr>"
        )

    return f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Discord Action Digest — CP3 LLM Evaluation</title>
<style>
body{{font-family:system-ui,-apple-system,Segoe UI,sans-serif;margin:0;background:#111827;color:#e5e7eb}}
main{{max-width:1200px;margin:auto;padding:28px}} .cards{{display:flex;gap:12px;flex-wrap:wrap}}
.card{{background:#1f2937;border:1px solid #374151;border-radius:12px;padding:14px;min-width:150px}}
.card b{{display:block;font-size:25px}} table{{width:100%;border-collapse:collapse;margin-top:22px;background:#1f2937}}
th,td{{padding:10px;border-bottom:1px solid #374151;text-align:left;vertical-align:top;font-size:13px}}
.pass td:nth-child(5){{color:#86efac}} .fail td:nth-child(5){{color:#fca5a5}}
</style></head><body><main>
<h1>CP3 — Live LLM Evaluation</h1>
<p>Model: {html.escape(str(run['model']))} · Generated: {html.escape(run['completed_at'])}</p>
<div class="cards">
<div class="card">Passed<b>{metrics['passed']}/{metrics['total']}</b></div>
<div class="card">Pass rate<b>{pct(metrics['pass_rate'])}</b></div>
<div class="card">Real-data cases<b>{metrics['real_data_cases']}</b></div>
</div>
<table><thead><tr><th>ID</th><th>Layer</th><th>Expected</th><th>Items/actionable</th><th>Result</th><th>Reason</th></tr></thead>
<tbody>{''.join(table_rows)}</tbody></table>
</main></body></html>"""


async def run_all_eval() -> None:
    golden_path = EVAL_DIR / "golden_set.json"
    golden_set = json.loads(golden_path.read_text(encoding="utf-8-sig"))
    now = datetime.now(ZoneInfo(settings.timezone))

    messages = [
        {
            "message_id": case["id"],
            "channel_id": "eval",
            "channel_name": "eval",
            "author": case.get("sender", "Eval User"),
            "created_at": now.isoformat(),
            "content": case["input_text"],
            "jump_url": None,
        }
        for case in golden_set
    ]

    print(f"Đang gửi {len(messages)} ca qua LLM thật ({settings.ai_model})...")
    try:
        llm_result = await analyze_messages(messages, now.isoformat(), settings.timezone)
    except Exception as exc:
        status = getattr(exc, "status_code", None)
        hints = {
            402: "OpenRouter không đủ credit.",
            429: "OpenRouter đang giới hạn request; chờ rồi chạy lại.",
        }
        print(f"EVAL FAILED: {type(exc).__name__}: {exc}")
        print(hints.get(status, "Kiểm tra API key, kết nối và JSON thô trong eval/ai_traces.log."))
        raise SystemExit(1) from None

    predictions: dict[str, list[dict]] = defaultdict(list)
    for item in llm_result.get("items", []):
        predictions[str(item.get("source_message_id", ""))].append(item)

    rows = [score_case(case, predictions.get(case["id"], []), now) for case in golden_set]
    total = len(rows)
    passed = sum(row["passed"] for row in rows)

    layer_breakdown: dict[str, dict] = {}
    for row in rows:
        stats = layer_breakdown.setdefault(row["layer"], {"total": 0, "passed": 0})
        stats["total"] += 1
        stats["passed"] += int(row["passed"])
    for stats in layer_breakdown.values():
        stats["pass_rate"] = stats["passed"] / stats["total"] if stats["total"] else 0.0

    metrics = {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": passed / total if total else 0.0,
        "real_data_cases": sum(row["is_real_data"] for row in rows),
        "predicted_item_count": sum(row["predicted_items_count"] for row in rows),
        "layer_breakdown": layer_breakdown,
    }
    completed_at = datetime.now(ZoneInfo(settings.timezone)).isoformat()
    run = {
        "started_at": now.isoformat(),
        "completed_at": completed_at,
        "model": settings.ai_model,
        "timezone": settings.timezone,
        "evaluation_method": "live_llm_single_batch",
    }
    output = {"run": run, "metrics": metrics, "cases": rows}
    markdown = build_markdown(run, metrics, rows)

    # Keep all public reports synchronized to this same live run.
    write_json(EVAL_DIR / "eval_results.json", output)
    write_json(EVAL_DIR / "latest_eval_result.json", output)
    atomic_write(EVAL_DIR / "run_results.md", markdown)
    atomic_write(EVAL_DIR / "EVAL_REPORT.md", markdown)
    atomic_write(EVAL_DIR / "report.html", build_html(run, metrics, rows))

    print("\n=== LIVE LLM GOLDEN SET EVAL ===")
    print(f"Tổng số : {total}")
    print(f"Đạt     : {passed}")
    print(f"Không đạt: {total - passed}")
    print(f"Tỷ lệ   : {pct(metrics['pass_rate'])}")
    print("Báo cáo : eval/run_results.md, eval/eval_results.json, eval/report.html")


if __name__ == "__main__":
    asyncio.run(run_all_eval())
