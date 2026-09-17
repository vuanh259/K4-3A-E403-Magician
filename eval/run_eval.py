import asyncio
import html
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "codebase"))

from dotenv import load_dotenv
load_dotenv(ROOT / "codebase" / ".env")

from ai import analyze_messages
from config import settings

def div(a,b): return a/b if b else 0.0

def pct(x): return f"{x*100:.1f}%"

async def main():
    cases = json.loads((Path(__file__).parent / "golden_set.json").read_text(encoding="utf-8-sig"))
    now = datetime.now(ZoneInfo(settings.timezone))

    PRIORITY_MAP = {
        "P1": "high", "HIGH": "high", "high": "high",
        "P2": "medium", "MEDIUM": "medium", "medium": "medium",
        "P3": "low", "LOW": "low", "low": "low",
    }

    messages = [{
        "message_id": c["id"],
        "channel_id": "eval",
        "channel_name": "eval",
        "author": c.get("sender", "Eval User"),
        "created_at": now.isoformat(),
        "content": c.get("input_text") or c.get("message") or "",
        "jump_url": None,
    } for c in cases]

    result = await analyze_messages(messages, now.isoformat(), settings.timezone)
    preds = {str(x.get("source_message_id")): x for x in result.get("items", [])}

    tp=fp=fn=tn=0
    type_ok=type_n=0
    priority_ok=priority_n=0
    deadline_ok=deadline_n=0
    grounded=0
    pred_count=len(result.get("items", []))
    rows=[]

    valid_ids={c["id"] for c in cases}
    hallucinated_sources=[sid for sid in preds.keys() if sid not in valid_ids]

    for c in cases:
        p = preds.get(c["id"])
        pred_actionable = bool(p and p.get("action_required") is True)
        
        gold_actionable = c.get("expected_actionable")
        if gold_actionable is None:
            gold_actionable = (c.get("expected_action") == "EXTRACT")
        gold = bool(gold_actionable)

        if gold and pred_actionable: tp+=1
        elif not gold and pred_actionable: fp+=1
        elif gold and not pred_actionable: fn+=1
        else: tn+=1

        if p and str(p.get("source_message_id")) == c["id"]:
            grounded += 1

        raw_priority = c.get("expected_priority")
        gold_priority = PRIORITY_MAP.get(str(raw_priority).upper(), raw_priority)
        
        gold_has_deadline = c.get("expected_has_deadline")
        if gold_has_deadline is None:
            gold_has_deadline = bool(c.get("expected_deadline"))

        gold_type = c.get("expected_type")

        if gold and pred_actionable:
            if gold_type:
                type_n += 1
                type_ok += int(p.get("type") == gold_type)

            if gold_priority:
                priority_n += 1
                priority_ok += int(p.get("priority") == gold_priority)

            deadline_n += 1
            pred_has_deadline = bool(p.get("deadline_iso"))
            deadline_ok += int(pred_has_deadline == gold_has_deadline)

        rows.append({
            "id": c["id"],
            "message": c.get("input_text") or c.get("message") or "",
            "gold_actionable": gold,
            "pred_actionable": pred_actionable,
            "gold_type": gold_type,
            "pred_type": p.get("type") if p else None,
            "gold_priority": gold_priority,
            "pred_priority": p.get("priority") if p else None,
            "gold_has_deadline": gold_has_deadline,
            "pred_has_deadline": bool(p.get("deadline_iso")) if p else False,
        })

    precision=div(tp,tp+fp)
    recall=div(tp,tp+fn)
    f1=div(2*precision*recall,precision+recall)
    accuracy=div(tp+tn,len(cases))
    type_acc=div(type_ok,type_n)
    priority_acc=div(priority_ok,priority_n)
    deadline_acc=div(deadline_ok,deadline_n)
    grounding_rate=div(grounded,max(pred_count,1))
    hallucination_rate=div(len(hallucinated_sources),max(pred_count,1))

    metrics={
        "sample_count":len(cases),
        "tp":tp,"fp":fp,"fn":fn,"tn":tn,
        "accuracy":accuracy,
        "precision":precision,
        "recall":recall,
        "f1":f1,
        "type_accuracy":type_acc,
        "priority_accuracy":priority_acc,
        "deadline_presence_accuracy":deadline_acc,
        "grounding_rate":grounding_rate,
        "hallucinated_source_rate":hallucination_rate,
    }

    out={"metrics":metrics,"cases":rows}
    out_json=Path(__file__).parent/"latest_eval_result.json"
    out_json.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")

    # Human-readable HTML report
    cards = [
        ("Sample count", str(metrics["sample_count"])),
        ("Recall", pct(recall)),
        ("Precision", pct(precision)),
        ("F1", pct(f1)),
        ("Accuracy", pct(accuracy)),
        ("Type accuracy", pct(type_acc)),
        ("Priority accuracy", pct(priority_acc)),
        ("Deadline extraction", pct(deadline_acc)),
        ("Grounding rate", pct(grounding_rate)),
        ("Hallucinated source", pct(hallucination_rate)),
    ]

    table_rows=[]
    for r in rows:
        ok = r["gold_actionable"] == r["pred_actionable"]
        table_rows.append(
            "<tr>"
            f"<td>{html.escape(r['id'])}</td>"
            f"<td>{html.escape(r['message'])}</td>"
            f"<td>{r['gold_actionable']}</td>"
            f"<td>{r['pred_actionable']}</td>"
            f"<td>{html.escape(str(r['gold_type']))}</td>"
            f"<td>{html.escape(str(r['pred_type']))}</td>"
            f"<td>{'PASS' if ok else 'FAIL'}</td>"
            "</tr>"
        )

    report = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Discord Assistant — Eval Report</title>
<style>
body{{font-family:system-ui,-apple-system,Segoe UI,sans-serif;margin:0;background:#111827;color:#e5e7eb}}
main{{max-width:1200px;margin:auto;padding:28px}}
h1{{margin-top:0}} .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}}
.card{{background:#1f2937;border:1px solid #374151;border-radius:14px;padding:16px}}
.card b{{display:block;font-size:26px;margin-top:6px}}
.small{{color:#9ca3af;font-size:13px}}
table{{width:100%;border-collapse:collapse;margin-top:22px;background:#1f2937}}
th,td{{border-bottom:1px solid #374151;padding:10px;text-align:left;font-size:13px;vertical-align:top}}
th{{color:#c7d2fe;position:sticky;top:0;background:#1f2937}}
.wrap{{overflow:auto;max-height:650px;border:1px solid #374151;border-radius:12px}}
</style></head><body><main>
<h1>AI Discord Assistant — Evaluation</h1>
<p class="small">Generated: {html.escape(datetime.now().isoformat())}</p>
<div class="grid">
{''.join(f'<div class="card"><span class="small">{html.escape(k)}</span><b>{html.escape(v)}</b></div>' for k,v in cards)}
</div>
<div class="wrap"><table><thead><tr><th>ID</th><th>Message</th><th>Gold actionable</th><th>Pred actionable</th><th>Gold type</th><th>Pred type</th><th>Result</th></tr></thead>
<tbody>{''.join(table_rows)}</tbody></table></div>
</main></body></html>"""

    report_path=Path(__file__).parent/"report.html"
    report_path.write_text(report,encoding="utf-8")

    print("\n=== AI DISCORD ASSISTANT EVAL ===")
    for k,v in cards:
        print(f"{k:24}: {v}")
    print("\nSaved:")
    print("-", out_json)
    print("-", report_path)

if __name__=="__main__":
    asyncio.run(main())
