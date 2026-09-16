# MINI HACKATHON AI — CHECKPOINT 1
## BẢN CHỮA CANVAS CHUẨN 4 Ô — NHÓM MAGICIAN (LỚP 3A · PHÒNG E403)
**Track B · Trợ lý Học viên (Discord)** — Đề tài: Discord Action Digest  
*Đội trưởng: Nguyễn Vũ Anh (2A202602502) · Link Repo: https://github.com/vuanh259/K4-3A-E403-Magician*

> **Ý tưởng ban đầu (TRƯỚC khi gọt):** Trợ lý Discord đọc/tổng hợp tin nhắn và chỉ ra và nhắc những thông tin quan trọng: task, deadline, lịch thay đổi và mức độ ưu tiên (quá rộng, ôm đồm).  
> **CÙNG Ý TƯỞNG ĐÓ, VIẾT LẠI CHO ĐÚNG THÀNH 4 Ô:**

---

### 1 · PAIN (Ai · Đang làm gì · Vướng đâu · Hậu quả gì)
Học viên khóa AI Thực Chiến · mỗi ngày phải theo dõi 3–10 channel Discord để cập nhật bài tập Lab, thời hạn nộp bài và lịch học · phải lướt đọc thủ công hàng trăm tin nhắn thảo luận và hỏi đáp vụn vặt · mất 10–20 phút mỗi ngày, và 50% từng bị trễ hạn nộp bài tập hoặc đến nhầm phòng học do tin thông báo bị trôi.  
*(Tuyệt đối không chứa chữ "AI" trong phát biểu nỗi đau).*

---

### 2 · BẰNG CHỨNG (Chuẩn A Khảo sát + Chuẩn B Mining dữ liệu)
- **Đường A (Khảo sát):** Hỏi 30 học viên trong lớp ngoài nhóm — 15 người (50.0%) xác nhận từng bỏ lỡ hoặc phát hiện muộn ít nhất một thông tin quan trọng trên Discord; 29/30 người (96.7%) muốn có công cụ tự động tổng hợp. Log đủ 30 câu trả lời trong `evidence_log.md`, kèm 5 câu nguyên văn:
  1. *"Do có quá nhiều tin nhắn mình đã để trôi thông tin quan trọng mà giảng viên gửi"*
  2. *"Suýt quên hoàn thành daily standup vì quá nhiều channel để check"*
  3. *"Bỏ lỡ workshop 1 và 2 do có quá nhiều kênh liên lạc"*
  4. *"Quên mất lịch workshop do tắt thông báo"*
  5. *"Không để ý task"*
- **Đường B (Mining data):** 1.092 tin trong `data/discord-pack/`: 4 bản tin bot hiện tại bị cắt cụt, chèn lỗi "nguồn tham chiếu" và 0% bản tin trích xuất được Actionable Task & Deadline.

---

### 3 · IMPACT & QUYẾT ĐỊNH CHỌN (Bảng 3 ứng viên)
Ba ứng viên: (1) Trích xuất Task, Deadline & Đổi lịch (Action Digest) · (2) Bot phát hiện học viên stuck chủ động gửi DM · (3) Q&A bài học trên Discord.  
- **CHỌN Action Digest:** ~1.000 học viên + 20 TA × 3–5 lần/ngày × 10–20 phút lọc tin. Chi phí sai sót cao nếu bịa deadline → giải quyết bằng Conditional + Source-first citation.  
- **LOẠI gợi ý gửi DM:** Xâm phạm riêng tư, gây phiền toái; **LOẠI Q&A:** Trùng VLearn Tutor, cần RAG toàn bộ bài giảng không khả thi trong 47.5h.

---

### 4 · LÁT CẮT (MỘT CÂU: 1 user · 1 việc · 1 quyết định AI · 1 kết quả)
Một học viên khóa AI Thực Chiến · dán hoặc chọn một luồng tin nhắn Discord trong ngày · AI quyết định tin này có chứa Task, Deadline hoặc Đổi lịch hay không (phân loại P1/P2/P3) · trả về Thẻ công việc gồm tiêu đề, thời hạn và độ ưu tiên kèm trích dẫn nguyên văn câu gốc từ TA/Giảng viên (hoặc gắn cờ `[⚠️ Cần xác nhận lại]` nếu thời gian mập mờ).

---

> 💡 **Ghi chú quan trọng:** Năm việc còn lại (Q&A bài học, bot tự DM học viên, trả lời điểm danh, sinh bài tập mới, gửi tin tự động) không mất đi — chúng xuống mục **"Non-goals / Để sau"** trong `spec.md`. Ghi ra đó vẫn được tính là nhóm đã cân nhắc kỹ lưỡng.

---
**Cam kết triển khai & Người thử nghiệm:**
- **Mức tự động hóa:** Conditional / Augment (Con người là người quyết định cuối cùng; AI chỉ trích xuất có căn cứ).
- **2 Willing Users (Cam kết thử nghiệm tại CP5):**
  1. Lê Nguyễn Thái Dương (Mã HV: `2A202602383`)
  2. Nguyễn Xuân Khuê (Mã HV: `2A202602999`)
- **Phân công nhóm:** Nguyễn Vũ Anh (Đội trưởng - Spec & Evidence) · Nguyễn Thành Duy (AI & Prompt) · Trương Việt Anh (Fullstack & Discord) · Phạm Quang Đạt (QA & Golden Set).
