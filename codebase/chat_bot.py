"""
Discord Action Digest — CLI Chatbot Tester (CP2 / CP3)
Cho phép tương tác trực tiếp: Người dùng gõ câu lệnh, Bot trích xuất & phản hồi.
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import json
import time

DATABASE_ITEMS = [
    {
        "priority": "P1",
        "title": "Dời Workshop chiều nay sang phòng E403",
        "deadline": "17:30 Hôm nay (16/9)",
        "source": "TA - Minh Hằng (15:30)",
        "quote": "🔔 ĐÍNH CHÍNH LỊCH: Buổi Workshop chiều nay dời từ phòng E402 sang phòng E403 lúc 17:30 nhé mọi người!",
        "status": "ĐÃ XÁC THỰC",
        "is_ambiguous": False
    },
    {
        "priority": "P1",
        "title": "Nộp Checkpoint 1 (Canvas 4 ô + Link Repo GitHub)",
        "deadline": "19:30 Hôm nay (16/9)",
        "source": "Giảng viên Lead Coach (14:15)",
        "quote": "Hạn nộp Checkpoint 1 là 19:30 tối nay ngày 16/9. Đội trưởng nộp link repo GitHub công khai và Canvas 4 ô qua form nhé.",
        "status": "ĐÃ XÁC THỰC",
        "is_ambiguous": False
    },
    {
        "priority": "P2",
        "title": "Nộp bài tập Lab 2 trên VLearn",
        "deadline": "Cần xác nhận lại giờ cụ thể",
        "source": "TA - Quốc Bảo (16:45)",
        "quote": "Bài tập Lab 2 nhớ hoàn thành và nộp trên VLearn vào tối nay nhé các bạn.",
        "status": "⚠️ MỐC GIỜ MẬP MỜ (Không tự bịa 23:59)",
        "is_ambiguous": True
    },
    {
        "priority": "P2",
        "title": "Chốt tài liệu AI Spec (spec.md) tại Checkpoint 4",
        "deadline": "21:00 Ngày 17/9",
        "source": "BTC Hackathon (17:00)",
        "quote": "Hạn chốt tài liệu AI Spec (spec.md) là 21:00 ngày 17/9 tại Checkpoint 4. Sau thời gian này sẽ khoá quality bar.",
        "status": "ĐÃ XÁC THỰC",
        "is_ambiguous": False
    },
    {
        "priority": "P3",
        "title": "Đọc tài liệu PAIR Guidebook và HAX Toolkit",
        "deadline": "Trước giờ học ngày mai 17/9",
        "source": "Giảng viên (16:00)",
        "quote": "Trước buổi học ngày mai, các bạn đọc tài liệu PAIR Guidebook và HAX Toolkit trong thư mục further-reading nhé.",
        "status": "THEO DÕI",
        "is_ambiguous": False
    }
]

def process_user_query(query):
    q = query.lower().strip()
    
    # 1. Check Out of Scope
    if any(k in q for k in ["giải thích", "transformer", "attention", "code", "thuật toán"]):
        return (
            "🤖 [Trợ lý Action Digest - Phản hồi ngoài phạm vi (HAX G1)]\n"
            "---------------------------------------------------\n"
            "Mình là Trợ lý Action Digest chuyên trích xuất Task, Deadline & Lịch đổi từ Discord.\n"
            "Để được giải đáp kiến thức chuyên sâu hoặc hỗ trợ code, bạn vui lòng liên hệ VLearn Tutor hoặc mentor phụ trách nhé!"
        )
    
    # 2. Check ambiguous specific questions (Low confidence)
    if "lab 2" in q:
        return (
            "🤖 [Trợ lý Action Digest - Tra cứu Lab 2 (HAX G2)]\n"
            "---------------------------------------------------\n"
            "📌 Task: Nộp bài tập Lab 2 trên VLearn\n"
            "⏱️ Thời hạn: [⚠️ CẦN XÁC NHẬN LẠI GIỜ]\n"
            "👤 Người thông báo: TA - Quốc Bảo (16:45)\n"
            "💬 Trích dẫn nguyên văn: \"Bài tập Lab 2 nhớ hoàn thành và nộp trên VLearn vào tối nay nhé các bạn.\"\n"
            "💡 Lưu ý an toàn: AI không tự bịa giờ 23:59 vì tin nhắn gốc chỉ nói 'tối nay'. Bạn nên nhắn tin hỏi lại TA để biết mốc giờ chính xác!"
        )

    # 3. Check schedule change queries
    if any(k in q for k in ["đổi", "dời", "phòng", "lịch"]):
        return (
            "🤖 [Trợ lý Action Digest - Thông báo Đổi Lịch Khẩn Cấp (P1)]\n"
            "---------------------------------------------------\n"
            "🔴 [P1 - KHẨN CẤP] Dời Workshop chiều nay sang phòng E403\n"
            "⏱️ Thời gian: 17:30 Hôm nay (16/9)\n"
            "👤 Nguồn: TA - Minh Hằng (15:30)\n"
            "💬 Quote gốc: \"🔔 ĐÍNH CHÍNH LỊCH: Buổi Workshop chiều nay dời từ phòng E402 sang phòng E403 lúc 17:30 nhé mọi người!\"\n"
            "👉 Hành động: Đến phòng E403, không đến E402."
        )

    # 4. Main Query: "tìm cho tôi những vấn đề quan trọng hôm nay" / tổng hợp
    p1_items = [i for i in DATABASE_ITEMS if i['priority'] == 'P1']
    p2_items = [i for i in DATABASE_ITEMS if i['priority'] == 'P2']
    p3_items = [i for i in DATABASE_ITEMS if i['priority'] == 'P3']

    out = []
    out.append("🤖 [BẢN TIN ACTION DIGEST — CÁC VẤN ĐỀ QUAN TRỌNG HÔM NAY]")
    out.append("================================================================")
    out.append(f"Quét thành công kênh #thông-báo · Phát hiện {len(DATABASE_ITEMS)} đầu việc quan trọng:\n")
    
    out.append("🔴 [P1 · KHẨN CẤP - CẦN XỬ LÝ NGAY]")
    for item in p1_items:
        out.append(f"  • {item['title']}")
        out.append(f"    ⏱️ Hạn chót: {item['deadline']}")
        out.append(f"    📌 Nguồn: {item['source']}")
        out.append(f"    💬 \"{item['quote'][:80]}...\"\n")

    out.append("🟡 [P2 · QUAN TRỌNG - BÀI TẬP & DEADLINE]")
    for item in p2_items:
        warn_tag = " [⚠️ Mốc giờ chưa cụ thể]" if item['is_ambiguous'] else ""
        out.append(f"  • {item['title']}{warn_tag}")
        out.append(f"    ⏱️ Hạn chót: {item['deadline']}")
        out.append(f"    📌 Nguồn: {item['source']}\n")

    out.append("🟢 [P3 · THEO DÕI - NHẮC NHỞ]")
    for item in p3_items:
        out.append(f"  • {item['title']} (Hạn: {item['deadline']})\n")

    out.append("================================================================")
    out.append("💡 Ghi chú: Bấm 'Sửa hạn nộp' nếu bạn muốn đính chính hoặc bổ sung.")
    return "\n".join(out)

if __name__ == "__main__":
    print("=== DISCORD ACTION DIGEST CLI BOT (TEST RUNNER) ===")
    print("Thử gõ một câu lệnh, ví dụ:")
    print("  1. 'tìm cho tôi những vấn đề quan trọng hôm nay'")
    print("  2. 'khi nào nộp lab 2?'")
    print("  3. 'có lịch nào bị đổi không?'")
    print("  4. 'giải thích Transformer cho tôi'")
    print("  (Gõ 'exit' để thoát)\n")

    # If argument passed, run directly
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        print(f"Người dùng hỏi: {user_input}\n")
        print(process_user_query(user_input))
    else:
        # Interactive loop
        sample_q = "tìm cho tôi những vấn đề quan trọng hôm nay"
        print(f"[TỰ ĐỘNG CHẠY TEST CÂU HỎI MẪU]: \"{sample_q}\"\n")
        print(process_user_query(sample_q))
