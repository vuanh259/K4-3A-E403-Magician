# 🎯 CANVAS CHECKPOINT 1 — MINI HACKATHON AI (BATCH 04)

**Đội thi:** Magician · **Lớp:** 3A · **Phòng:** E403  
**Track:** Track B — Trợ lý Học viên (Discord)  
**Tên lát cắt:** Discord Action Digest (Trích xuất Task, Deadline & Thay đổi lịch)  
**Đội trưởng:** Nguyễn Vũ Anh (Mã HV: `2A202602502`)  
**Repo:** [https://github.com/vuanh259/K4-3A-E403-Magician](https://github.com/vuanh259/K4-3A-E403-Magician)

---

| 🟩 **01 · NGƯỜI DÙNG & NỖI ĐAU** | 🟦 **02 · BẰNG CHỨNG BAN ĐẦU** |
|---|---|
| **Học viên & TA muốn nắm bắt kịp thời việc quan trọng**<br><br>• **Job executor:** Học viên khóa học AI và TA quản lý kênh Discord hàng ngày.<br>• **Core JTBD:** Nắm bắt kịp thời, không bỏ sót các đầu việc cần làm (task), hạn nộp bài (deadline) và các thông báo dời lịch/đổi phòng.<br>• **Problem statement (Pain):** Kênh Discord có lưu lượng tin nhắn thảo luận quá lớn; thông báo quan trọng và đính chính lịch bị trôi. Học viên mất 10–20 phút/ngày cuộn tìm tin, dễ quên deadline hoặc đến nhầm giờ học. | **Khảo sát thực tế ($n = 30$) & Mining dữ liệu**<br><br>• **Khảo sát thực tế ($n = 30$ học viên Batch 4):**<br>  - **50.0% (15/30)** học viên xác nhận từng bỏ lỡ hoặc phát hiện muộn thông tin quan trọng trên Discord.<br>  - **96.7% (29/30)** học viên mong muốn có công cụ tự động trích xuất Task, Deadline, Lịch đổi.<br>• **Quote nguyên văn:**<br>  - *"Do có quá nhiều tin nhắn mình đã để trôi thông tin quan trọng mà giảng viên gửi"*<br>  - *"Suýt quên hoàn thành daily standup vì quá nhiều channel để check"*<br>  - *"Quên mất lịch workshop do tắt thông báo"*<br>• **Mining data (`data/discord-pack/`):** 1.092 tin nhắn thực tế có nhiều lịch đính chính; 4 bản tin bot hiện tại bị cắt cụt, chèn chuỗi lỗi và thiếu hẳn phân cấp ưu tiên Task/Deadline. |
| 🟨 **03 · LÁT CẮT & AUTOMATION** | 🟧 **04 · NGƯỜI THỬ & PHÂN CÔNG** |
| **Một luồng tin nhắn, một danh sách hành động rõ ràng**<br><br>• **Lát cắt một câu:** Từ luồng tin nhắn Discord trong ngày → AI tự động lọc bỏ tin tán gẫu, trích xuất danh sách Task · Deadline · Thay đổi lịch và phân loại 3 mức ưu tiên (P1 · P2 · P3) kèm trích dẫn gốc → Học viên mở ra 30 giây là nắm trọn việc cần làm.<br>• **3 mức ưu tiên:**<br>  - 🔴 **P1 (Khẩn cấp):** Đổi lịch/phòng, deadline trong 24h.<br>  - 🟡 **P2 (Quan trọng):** Task bài tập mới, deadline > 24h.<br>  - 🟢 **P3 (Theo dõi):** Thông báo chung, nhắc nhở định kỳ.<br>• **Automation (Conditional / Augment):** AI chỉ trích xuất có căn cứ nguồn gốc; với tin nhắn mốc giờ mập mờ ("hạn tối nay"), AI gắn cờ `[⚠️ Cần xác nhận lại]` chứ tuyệt đối không tự bịa giờ để tránh cost-of-error. | **Có người thử (≥2 người), có người chịu trách nhiệm**<br><br>• **Willing users dự kiến (2 người ngoài nhóm cho CP5):**<br>  1. **Lê Nguyễn Thái Dương** — Mã HV: `2A202602383`<br>  2. **Nguyễn Xuân Khuê** — Mã HV: `2A202602999`<br><br>• **Phân công 4 thành viên nhóm:**<br>  - **Nguyễn Vũ Anh (2A202602502):** Đội trưởng · Spec & Bằng chứng khảo sát.<br>  - **Nguyễn Thành Duy (2A202602804):** AI & Prompt Engineering · Logic phân cấp P1/P2/P3.<br>  - **Trương Việt Anh (2A202602444):** Fullstack & Discord Integration · Giao diện Digest.<br>  - **Phạm Quang Đạt (2A202602704):** QA & Eval · Xây dựng Golden Set 20 case & đo lường. |

---

*Tài liệu thuộc khuôn khổ Mini Hackathon AI Batch 04 · Checkpoint 1 (16/9/2026)*
