import argparse
import asyncio
import html
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
EVAL_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT / "codebase"))

from dotenv import load_dotenv

load_dotenv(ROOT / "codebase" / ".env")

from ai import analyze_messages
from config import settings


PRIORITY_MAP = {
    "P1": "high",
    "HIGH": "high",
    "high": "high",
    "P2": "medium",
    "MEDIUM": "medium",
    "medium": "medium",
    "P3": "low",
    "LOW": "low",
    "low": "low",
}


def div(a: int | float, b: int | float) -> float:
    return a / b if b else 0.0


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def atomic_write(path: Path, content: str) -> None:
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(content, encoding="utf-8")
    temp_path.replace(path)


def write_json(path: Path, data: Any) -> None:
    atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2))


def next_run_number() -> int:
    run_numbers = []
    for path in EVAL_DIR.glob("run_*_raw.json"):
        match = re.fullmatch(r"run_(\d+)_raw\.json", path.name)
        if match:
            run_numbers.append(int(match.group(1)))
    return max(run_numbers, default=0) + 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the CP3 Golden Set evaluation.")
    parser.add_argument(
        "--run-number",
        type=int,
        default=next_run_number(),
        help="Run number used in evidence filenames (default: next unused number).",
    )
    args = parser.parse_args()
    if args.run_number < 1:
        parser.error("--run-number must be at least 1")
    return args


def preserve_run_one_reports() -> None:
    """Archive legacy canonical Run 1 reports before writing a later run."""
    mappings = {
        EVAL_DIR / "latest_eval_result.json": EVAL_DIR / "run_1_eval_result.json",
        EVAL_DIR / "report.html": EVAL_DIR / "run_1_report.html",
        EVAL_DIR / "run_results.md": EVAL_DIR / "run_1_results.md",
    }
    for source, archive in mappings.items():
        if source.exists() and not archive.exists():
            atomic_write(archive, source.read_text(encoding="utf-8"))


def normalize_iso(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None


def iso_equal(actual: Any, expected: Any) -> bool:
    actual_dt = normalize_iso(actual)
    expected_dt = normalize_iso(expected)
    if actual_dt is None or expected_dt is None:
        return False
    try:
        return actual_dt == expected_dt
    except TypeError:
        # A timezone-aware timestamp must not silently match a naive timestamp.
        return False


def md_cell(value: Any) -> str:
    return str(value if value is not None else "—").replace("|", "\\|").replace("\n", " ")


def classify_failure(reasons: list[str]) -> str:
    joined = " ".join(reasons)
    if "không tạo item" in joined:
        return "Bỏ sót hành động (false negative)"
    if "không mong đợi" in joined or "Số item" in joined:
        return "Trích xuất thừa hoặc sai phạm vi"
    if "Sai type" in joined:
        return "Phân loại nghiệp vụ chưa đúng"
    if "Sai trạng thái deadline" in joined or "Sai deadline:" in joined:
        return "Hiểu hoặc chuẩn hóa thời gian chưa đúng"
    if "Sai priority" in joined:
        return "Xếp mức ưu tiên chưa đúng"
    return "Đầu ra chưa khớp tiêu chí nghiệm thu"


def score_cases(cases: list[dict], result: dict, trace: dict) -> tuple[dict, list[dict]]:
    items = result.get("items", [])
    predictions: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        predictions[str(item.get("source_message_id", ""))].append(item)

    raw_items = trace.get("parsed_response_before_grounding", {}).get("items", [])
    if not isinstance(raw_items, list):
        raw_items = []
    valid_ids = {str(case["id"]) for case in cases}
    hallucinated_sources = [
        str(item.get("source_message_id", ""))
        for item in raw_items
        if str(item.get("source_message_id", "")) not in valid_ids
    ]

    tp = fp = fn = tn = 0
    type_ok = priority_ok = deadline_presence_ok = 0
    type_n = priority_n = deadline_presence_n = 0
    exact_deadline_ok = exact_deadline_n = 0
    title_ok = title_n = 0
    rows: list[dict] = []

    for case in cases:
        case_id = str(case["id"])
        predicted_items = predictions.get(case_id, [])
        actionable_items = [item for item in predicted_items if item.get("action_required") is True]
        candidate = actionable_items[0] if actionable_items else (predicted_items[0] if predicted_items else None)

        gold_actionable = bool(case.get("expected_actionable"))
        pred_actionable = bool(actionable_items)
        expected_count = int(case.get("expected_items_count", 1 if gold_actionable else 0))
        actual_count = len(predicted_items)

        if gold_actionable and pred_actionable:
            tp += 1
        elif not gold_actionable and pred_actionable:
            fp += 1
        elif gold_actionable and not pred_actionable:
            fn += 1
        else:
            tn += 1

        gold_type = case.get("expected_type")
        raw_priority = case.get("expected_priority")
        gold_priority = PRIORITY_MAP.get(str(raw_priority).upper(), raw_priority) if raw_priority else None
        gold_has_deadline = case.get("expected_has_deadline")
        if gold_has_deadline is None:
            gold_has_deadline = bool(case.get("expected_deadline"))
        gold_has_deadline = bool(gold_has_deadline)
        expected_deadline = case.get("expected_deadline")
        expected_keywords = [str(value) for value in case.get("expected_title_keywords", [])]

        pred_type = candidate.get("type") if candidate else None
        pred_priority = candidate.get("priority") if candidate else None
        pred_deadline = candidate.get("deadline_iso") if candidate else None
        pred_has_deadline = bool(pred_deadline)
        pred_title = str(candidate.get("title", "")) if candidate else ""
        pred_confidence = candidate.get("confidence") if candidate else None

        count_match = actual_count == expected_count
        actionable_match = pred_actionable == gold_actionable
        type_match = not gold_type or pred_type == gold_type
        priority_match = not gold_priority or pred_priority == gold_priority
        deadline_presence_match = pred_has_deadline == gold_has_deadline
        exact_deadline_match = not expected_deadline or iso_equal(pred_deadline, expected_deadline)
        missing_keywords = [keyword for keyword in expected_keywords if keyword.casefold() not in pred_title.casefold()]
        title_match = not missing_keywords

        if gold_actionable:
            if gold_type:
                type_n += 1
                type_ok += int(type_match)
            if gold_priority:
                priority_n += 1
                priority_ok += int(priority_match)
            deadline_presence_n += 1
            deadline_presence_ok += int(deadline_presence_match)
            if expected_deadline:
                exact_deadline_n += 1
                exact_deadline_ok += int(exact_deadline_match)
            if expected_keywords:
                title_n += 1
                title_ok += int(title_match)

        reasons: list[str] = []
        if not count_match:
            reasons.append(f"Số item: mong đợi {expected_count}, thực tế {actual_count}")
        if not actionable_match:
            if gold_actionable:
                reasons.append("Model không tạo item actionable")
            else:
                reasons.append("Model tạo item actionable không mong đợi")
        if gold_actionable and not type_match:
            reasons.append(f"Sai type: mong đợi {gold_type}, thực tế {pred_type}")
        if gold_actionable and not priority_match:
            reasons.append(f"Sai priority: mong đợi {gold_priority}, thực tế {pred_priority}")
        if gold_actionable and not deadline_presence_match:
            reasons.append(
                f"Sai trạng thái deadline: mong đợi {gold_has_deadline}, thực tế {pred_has_deadline}"
            )
        if gold_actionable and not exact_deadline_match:
            reasons.append(f"Sai deadline: mong đợi {expected_deadline}, thực tế {pred_deadline}")
        diagnostic_warnings: list[str] = []
        if gold_actionable and not title_match:
            diagnostic_warnings.append(
                "Tiêu đề chưa chứa từ khóa tham chiếu: " + ", ".join(missing_keywords)
            )

        case_pass = all(
            [
                count_match,
                actionable_match,
                type_match,
                priority_match,
                deadline_presence_match,
                exact_deadline_match,
            ]
        )
        rows.append(
            {
                "id": case_id,
                "case_group": case.get("case_group"),
                "layer": case.get("layer"),
                "scenario": case.get("scenario"),
                "message": case.get("input_text") or case.get("message") or "",
                "expected_actionable": gold_actionable,
                "predicted_actionable": pred_actionable,
                "expected_items_count": expected_count,
                "predicted_items_count": actual_count,
                "expected_type": gold_type,
                "predicted_type": pred_type,
                "expected_priority": gold_priority,
                "predicted_priority": pred_priority,
                "expected_has_deadline": gold_has_deadline,
                "predicted_has_deadline": pred_has_deadline,
                "expected_deadline": expected_deadline,
                "predicted_deadline": pred_deadline,
                "expected_title_keywords": expected_keywords,
                "predicted_title": pred_title or None,
                "predicted_confidence": pred_confidence,
                "documented_pass_criteria": case.get("pass_criteria", []),
                "checks": {
                    "count": count_match,
                    "actionable": actionable_match,
                    "type": type_match,
                    "priority": priority_match,
                    "deadline_presence": deadline_presence_match,
                    "exact_deadline": exact_deadline_match,
                    "title_keywords": title_match,
                },
                "result": "PASS" if case_pass else "FAIL",
                "failure_reasons": reasons,
                "diagnostic_warnings": diagnostic_warnings,
                "failure_category": None if case_pass else classify_failure(reasons),
            }
        )

    passed = sum(row["result"] == "PASS" for row in rows)
    precision = div(tp, tp + fp)
    recall = div(tp, tp + fn)
    metrics = {
        "sample_count": len(cases),
        "passed": passed,
        "failed": len(cases) - passed,
        "pass_rate": div(passed, len(cases)),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "actionability_accuracy": div(tp + tn, len(cases)),
        "precision": precision,
        "recall": recall,
        "f1": div(2 * precision * recall, precision + recall),
        "type_accuracy": div(type_ok, type_n),
        "priority_accuracy": div(priority_ok, priority_n),
        "deadline_presence_accuracy": div(deadline_presence_ok, deadline_presence_n),
        "exact_deadline_accuracy": div(exact_deadline_ok, exact_deadline_n),
        "title_keyword_coverage": div(title_ok, title_n),
        "raw_model_item_count": len(raw_items),
        "grounded_item_count": len(raw_items) - len(hallucinated_sources),
        "grounding_rate": div(len(raw_items) - len(hallucinated_sources), len(raw_items)),
        "hallucinated_source_count": len(hallucinated_sources),
        "hallucinated_source_rate": div(len(hallucinated_sources), len(raw_items)),
        "hallucinated_source_ids": hallucinated_sources,
    }
    return metrics, rows


def build_markdown(run_info: dict, metrics: dict, rows: list[dict]) -> str:
    failures = [row for row in rows if row["result"] == "FAIL"]
    category_counts = Counter(row["failure_category"] for row in failures)
    lines = [
        f"# CP3 — Kết quả đánh giá Run {run_info['run_number']}",
        "",
        "> Đây là kết quả thực nghiệm do `eval/run_eval.py` sinh tự động từ lời gọi AI thật. Không chỉnh tay số PASS/FAIL.",
        "",
        "## Thông tin lượt chạy",
        "",
        f"- Thời điểm: `{run_info['completed_at']}`",
        f"- Model yêu cầu: `{md_cell(run_info['requested_model'])}`",
        f"- Model phản hồi: `{md_cell(run_info.get('response_model'))}`",
        f"- Múi giờ: `{md_cell(run_info['timezone'])}`",
        f"- Golden Set: `{metrics['sample_count']}` ca",
        f"- Log prompt và phản hồi thô: `eval/{run_info['raw_log_name']}`",
        "",
        "## Kết quả chính",
        "",
        f"- Đạt: **{metrics['passed']}/{metrics['sample_count']}** ca",
        f"- Không đạt: **{metrics['failed']}/{metrics['sample_count']}** ca",
        f"- Tỷ lệ đạt: **{pct(metrics['pass_rate'])}**",
        "",
        "| Chỉ số | Kết quả |",
        "|---|---:|",
        f"| Actionability accuracy | {pct(metrics['actionability_accuracy'])} |",
        f"| Precision | {pct(metrics['precision'])} |",
        f"| Recall | {pct(metrics['recall'])} |",
        f"| F1 | {pct(metrics['f1'])} |",
        f"| Type accuracy | {pct(metrics['type_accuracy'])} |",
        f"| Priority accuracy | {pct(metrics['priority_accuracy'])} |",
        f"| Deadline presence accuracy | {pct(metrics['deadline_presence_accuracy'])} |",
        f"| Exact deadline accuracy | {pct(metrics['exact_deadline_accuracy'])} |",
        f"| Title keyword coverage (tham khảo) | {pct(metrics['title_keyword_coverage'])} |",
        f"| Grounding rate trước khi lọc | {pct(metrics['grounding_rate'])} |",
        f"| Source ID bịa | {metrics['hallucinated_source_count']} |",
        "",
        "## Kết quả từng ca",
        "",
        "| ID | Nhóm | Kịch bản | Số item (E/A) | Type (E/A) | Deadline (E/A) | Kết quả | Nguyên nhân |",
        "|---|---|---|---:|---|---|---|---|",
    ]
    for row in rows:
        deadline_expected = row["expected_deadline"] or str(row["expected_has_deadline"])
        deadline_actual = row["predicted_deadline"] or str(row["predicted_has_deadline"])
        reason = "; ".join(row["failure_reasons"])
        if not reason and row["diagnostic_warnings"]:
            reason = "PASS; lưu ý: " + "; ".join(row["diagnostic_warnings"])
        if not reason:
            reason = "Đáp ứng toàn bộ tiêu chí tự động"
        lines.append(
            "| "
            + " | ".join(
                md_cell(value)
                for value in [
                    row["id"],
                    row["case_group"],
                    row["scenario"],
                    f"{row['expected_items_count']}/{row['predicted_items_count']}",
                    f"{row['expected_type'] or '—'}/{row['predicted_type'] or '—'}",
                    f"{deadline_expected}/{deadline_actual}",
                    row["result"],
                    reason,
                ]
            )
            + " |"
        )

    lines.extend(["", "## Phân tích các ca sai lệch", ""])
    if not failures:
        lines.append("Không có ca thất bại trong lượt chạy này.")
    else:
        lines.extend(["### Tổng hợp nhóm nguyên nhân", ""])
        for category, count in category_counts.most_common():
            lines.append(f"- {category}: {count} ca")
        lines.extend(["", "### Chi tiết", ""])
        for row in failures:
            lines.extend(
                [
                    f"#### {row['id']} — {row['scenario']}",
                    "",
                    f"- Nhóm nguyên nhân: {row['failure_category']}",
                    f"- Đầu ra dự kiến: count={row['expected_items_count']}, type={row['expected_type']}, priority={row['expected_priority']}, deadline={row['expected_deadline'] or row['expected_has_deadline']}.",
                    f"- Đầu ra thực tế: count={row['predicted_items_count']}, type={row['predicted_type']}, priority={row['predicted_priority']}, deadline={row['predicted_deadline'] or row['predicted_has_deadline']}.",
                    f"- Sai lệch: {'; '.join(row['failure_reasons'])}.",
                    "",
                ]
            )

    lines.extend(
        [
            "## Cách xác định PASS/FAIL",
            "",
            "Một ca chỉ PASS khi đồng thời đúng: số item, actionable, type, priority, có/không có deadline và deadline chính xác nếu Golden Set có mốc cụ thể. Với ca không actionable, model phải không tạo item nào.",
            "",
            "Từ khóa tiêu đề chỉ là chỉ số chẩn đoán vì model có thể diễn đạt đúng bằng từ đồng nghĩa; chúng không tự động làm một ca FAIL. Các tiêu chí mô tả tự do trong `pass_criteria` vẫn được lưu trong JSON để nhóm đối chiếu khi giải thích demo. Số liệu không che giấu các ca lỗi; lỗi kỹ thuật như HTTP 402/429 hoặc JSON không hợp lệ được ghi vào raw log của lượt chạy và không ghi đè báo cáo thành công gần nhất.",
            "",
        ]
    )
    return "\n".join(lines)


def build_html(run_info: dict, metrics: dict, rows: list[dict]) -> str:
    cards = [
        ("Passed", f"{metrics['passed']}/{metrics['sample_count']}"),
        ("Pass rate", pct(metrics["pass_rate"])),
        ("Precision", pct(metrics["precision"])),
        ("Recall", pct(metrics["recall"])),
        ("F1", pct(metrics["f1"])),
        ("Type accuracy", pct(metrics["type_accuracy"])),
        ("Priority accuracy", pct(metrics["priority_accuracy"])),
        ("Exact deadline", pct(metrics["exact_deadline_accuracy"])),
        ("Grounding", pct(metrics["grounding_rate"])),
    ]
    table_rows = []
    for row in rows:
        reason = "; ".join(row["failure_reasons"])
        if not reason and row["diagnostic_warnings"]:
            reason = "PASS; lưu ý: " + "; ".join(row["diagnostic_warnings"])
        if not reason:
            reason = "Đáp ứng toàn bộ tiêu chí"
        css_class = "pass" if row["result"] == "PASS" else "fail"
        table_rows.append(
            f'<tr class="{css_class}">'
            f"<td>{html.escape(row['id'])}</td>"
            f"<td>{html.escape(str(row['scenario']))}</td>"
            f"<td>{row['expected_items_count']}/{row['predicted_items_count']}</td>"
            f"<td>{html.escape(str(row['expected_type']))}/{html.escape(str(row['predicted_type']))}</td>"
            f"<td>{html.escape(str(row['expected_deadline'] or row['expected_has_deadline']))}/"
            f"{html.escape(str(row['predicted_deadline'] or row['predicted_has_deadline']))}</td>"
            f"<td><b>{row['result']}</b></td>"
            f"<td>{html.escape(reason)}</td>"
            "</tr>"
        )

    return f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Discord Assistant — CP3 Eval Run {run_info['run_number']}</title>
<style>
body{{font-family:system-ui,-apple-system,Segoe UI,sans-serif;margin:0;background:#111827;color:#e5e7eb}}
main{{max-width:1280px;margin:auto;padding:28px}} h1{{margin-top:0}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:12px}}
.card{{background:#1f2937;border:1px solid #374151;border-radius:14px;padding:16px}}
.card b{{display:block;font-size:26px;margin-top:6px}} .small{{color:#9ca3af;font-size:13px}}
table{{width:100%;border-collapse:collapse;background:#1f2937}}
th,td{{border-bottom:1px solid #374151;padding:10px;text-align:left;font-size:13px;vertical-align:top}}
th{{color:#c7d2fe;position:sticky;top:0;background:#1f2937}}
.wrap{{overflow:auto;max-height:680px;margin-top:22px;border:1px solid #374151;border-radius:12px}}
.pass td:nth-child(6){{color:#86efac}} .fail td:nth-child(6){{color:#fca5a5}}
</style></head><body><main>
<h1>AI Discord Assistant — CP3 Evaluation Run {run_info['run_number']}</h1>
<p class="small">Generated: {html.escape(run_info['completed_at'])} · Model: {html.escape(str(run_info['requested_model']))}</p>
<div class="grid">{''.join(f'<div class="card"><span class="small">{html.escape(k)}</span><b>{html.escape(v)}</b></div>' for k, v in cards)}</div>
<div class="wrap"><table><thead><tr><th>ID</th><th>Scenario</th><th>Count E/A</th><th>Type E/A</th><th>Deadline E/A</th><th>Result</th><th>Reason</th></tr></thead>
<tbody>{''.join(table_rows)}</tbody></table></div>
</main></body></html>"""


async def main() -> None:
    args = parse_args()
    run_number = args.run_number
    run_name = f"CP3 Run {run_number}"
    raw_log_path = EVAL_DIR / f"run_{run_number}_raw.json"
    if raw_log_path.exists():
        raise SystemExit(
            f"Refusing to overwrite {raw_log_path.name}. "
            "Omit --run-number to use the next unused number."
        )
    if run_number > 1:
        preserve_run_one_reports()

    cases = json.loads((EVAL_DIR / "golden_set.json").read_text(encoding="utf-8-sig"))
    now = datetime.now(ZoneInfo(settings.timezone))
    trace: dict[str, Any] = {
        "run_name": run_name,
        "run_number": run_number,
        "started_at": now.isoformat(),
        "status": "running",
    }
    messages = [
        {
            "message_id": case["id"],
            "channel_id": "eval",
            "channel_name": "eval",
            "author": case.get("sender", "Eval User"),
            "created_at": now.isoformat(),
            "content": case.get("input_text") or case.get("message") or "",
            "jump_url": None,
        }
        for case in cases
    ]

    try:
        result = await analyze_messages(messages, now.isoformat(), settings.timezone, trace=trace)
    except Exception as exc:
        trace.update(
            {
                "status": "failed",
                "completed_at": datetime.now(ZoneInfo(settings.timezone)).isoformat(),
                "error": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                    "http_status": getattr(exc, "status_code", None),
                },
            }
        )
        write_json(raw_log_path, trace)
        status = trace["error"]["http_status"]
        hint = {
            402: "OpenRouter không đủ credit. Nạp credit rồi chạy lại.",
            429: "OpenRouter đang giới hạn request. Chờ rồi chạy lại; SDK cũng tự retry lỗi tạm thời.",
        }.get(status, "Kiểm tra error và raw response trong log; có thể model trả JSON không hợp lệ.")
        print(f"EVAL FAILED: {type(exc).__name__}: {exc}")
        print(hint)
        print("Raw/error log:", raw_log_path)
        raise SystemExit(1) from None

    completed_at = datetime.now(ZoneInfo(settings.timezone)).isoformat()
    metrics, rows = score_cases(cases, result, trace)
    run_info = {
        "run_name": run_name,
        "run_number": run_number,
        "started_at": trace["started_at"],
        "completed_at": completed_at,
        "requested_model": settings.ai_model,
        "response_model": trace.get("response", {}).get("model"),
        "timezone": settings.timezone,
        "raw_log_name": raw_log_path.name,
    }
    trace.update({"status": "success", "completed_at": completed_at, "metrics": metrics})

    output = {"run": run_info, "metrics": metrics, "cases": rows}
    out_json = EVAL_DIR / "latest_eval_result.json"
    report_path = EVAL_DIR / "report.html"
    markdown_path = EVAL_DIR / "run_results.md"
    versioned_json = EVAL_DIR / f"run_{run_number}_eval_result.json"
    versioned_report = EVAL_DIR / f"run_{run_number}_report.html"
    versioned_markdown = EVAL_DIR / f"run_{run_number}_results.md"

    # Write raw evidence first. Reports are replaced only after a complete API
    # response and a successful scoring pass.
    write_json(raw_log_path, trace)
    write_json(versioned_json, output)
    atomic_write(versioned_report, build_html(run_info, metrics, rows))
    atomic_write(versioned_markdown, build_markdown(run_info, metrics, rows))
    write_json(out_json, output)
    atomic_write(report_path, build_html(run_info, metrics, rows))
    atomic_write(markdown_path, build_markdown(run_info, metrics, rows))

    print(f"\n=== AI DISCORD ASSISTANT — CP3 RUN {run_number} ===")
    print(f"Passed                  : {metrics['passed']}/{metrics['sample_count']}")
    print(f"Failed                  : {metrics['failed']}/{metrics['sample_count']}")
    print(f"Pass rate               : {pct(metrics['pass_rate'])}")
    print(f"Actionability accuracy  : {pct(metrics['actionability_accuracy'])}")
    print(f"Exact deadline accuracy : {pct(metrics['exact_deadline_accuracy'])}")
    print(f"Grounding rate          : {pct(metrics['grounding_rate'])}")
    print("\nSaved:")
    for path in [
        raw_log_path,
        versioned_json,
        versioned_report,
        versioned_markdown,
        out_json,
        report_path,
        markdown_path,
    ]:
        print("-", path)


if __name__ == "__main__":
    asyncio.run(main())
