# MINI HACKATHON AI — CHECKPOINT 1
## VÍ DỤ THỰC TẾ · CANVAS CP1
**Hướng B · Trợ lý Học viên (Discord)** — Discord Action Digest (Trích xuất Task, Deadline & Thay đổi lịch)  
*Nhóm: Magician · Lớp: 3A · Phòng: E403 · Đội trưởng: Nguyễn Vũ Anh (2A202602502)*  
*Repo công khai: [https://github.com/vuanh259/K4-3A-E403-Magician](https://github.com/vuanh259/K4-3A-E403-Magician)*

---

### 01 · NGƯỜI DÙNG & NỖI ĐAU
**Học viên & TA muốn nắm bắt kịp thời việc quan trọng**
- **Job:** học viên và TA theo dõi nhiều channel Discord hàng ngày để biết việc cần làm, bài tập cần nộp, lịch học và phòng học.
- **Pain:** kênh Discord có lưu lượng tin nhắn lớn; thông báo quan trọng và đính chính lịch bị trôi lẫn trong hàng trăm tin nhắn thảo luận. Học viên mất 10–20 phút/ngày cuộn tìm tin, dễ quên deadline hoặc đến nhầm giờ học.
> *(Không chứa chữ "AI" trong phát biểu nỗi đau)*

---

### 02 · BẰNG CHỨNG BAN ĐẦU
**Khảo sát thực tế (n = 30) & Mining dữ liệu được phép dùng**
- **Khảo sát thực tế ($n = 30$ học viên Batch 4):**
  - **50.0% (15/30)** học viên xác nhận từng bỏ lỡ hoặc phát hiện muộn tin quan trọng.
  - **96.7% (29/30)** mong muốn công cụ tự động tổng hợp task/deadline/lịch thay đổi.
- **Quote nguyên văn:**
  - *"Do có quá nhiều tin nhắn mình đã để trôi thông tin quan trọng mà giảng viên gửi"*
  - *"Suýt quên hoàn thành daily standup vì quá nhiều channel để check"*
  - *"Bỏ lỡ workshop 1 và 2 do có quá nhiều kênh liên lạc"*
- **Mining pack (`data/discord-pack` 1.092 tin):** Bản tin bot hiện có bị cắt cụt, chèn chuỗi lỗi và hoàn toàn thiếu phân cấp ưu tiên Task/Deadline.
> *(Không copy số liệu, snippet hay mã nguồn thật ra ngoài data/)*

---

### 03 · LÁT CẮT & AUTOMATION
**Một luồng tin nhắn, một danh sách hành động rõ ràng**
`🔴 P1 KHẨN CẤP` · `🟡 P2 QUAN TRỌNG` · `🟢 P3 THEO DÕI`

- **Lát cắt:** Từ luồng tin nhắn Discord trong ngày: AI tự động lọc bỏ tin tán gẫu, trích xuất Task · Deadline · Đổi lịch và phân thành 3 mức ưu tiên kèm trích dẫn gốc để học viên mở ra 30 giây là nắm trọn việc.
- **Conditional:** trích xuất khi có nguồn chắc chắn; gắn nhãn `[⚠️ Cần xác nhận lại]` khi thời gian mập mờ; từ chối và tag TA khi ngoài phạm vi.

---

### 04 · NGƯỜI THỬ & PHÂN CÔNG
**Có người thử, có người chịu trách nhiệm**
- **Willing users dự kiến:** mời test 2 người ngoài nhóm (cam kết thử nghiệm ở CP5):
  1. **Lê Nguyễn Thái Dương** (Mã HV: `2A202602383`)
  2. **Nguyễn Xuân Khuê** (Mã HV: `2A202602999`)
- **4 vai trò:**
  - **Vũ Anh:** Spec & Evidence (Khảo sát $n=30$)
  - **Thành Duy:** AI & Prompt Engineering (P1/P2/P3)
  - **Việt Anh:** Fullstack & Discord Integration
  - **Quang Đạt:** QA & Eval (Golden Set 20 case)
> *(Đầy đủ 2 willing users khai báo từ CP1 để lấy trọn 8 điểm R6)*

---
*Checkpoint 1: Canvas đã điền · Nhóm Magician · Lớp 3A · Phòng E403*
