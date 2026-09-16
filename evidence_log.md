# NHẬT KÝ BẰNG CHỨNG & DỮ LIỆU KHẢO SÁT (EVIDENCE LOG) — CP1

Tài liệu ghi nhận toàn bộ dữ liệu khảo sát thực tế và khai phá dữ liệu phục vụ thẩm định đề tài Mini Hackathon AI Batch 04 (Lớp 3A · Phòng E403 · Nhóm Magician).

---

## 1. Dữ liệu khảo sát thực tế (Đạt Chuẩn A)
- **Phương pháp:** Khảo sát học viên qua biểu mẫu Google Forms về trải nghiệm theo dõi thông tin học tập trên Discord.
- **Quy mô mẫu:** $n = 30$ học viên (vượt chuẩn tối thiểu 20 người ngoài nhóm).
- **Tỷ lệ xác nhận nỗi đau:** **50.0% (15/30)** học viên xác nhận từng bỏ lỡ hoặc phát hiện muộn thông tin quan trọng trên Discord (vượt chuẩn tối thiểu 50%).
- **Tỷ lệ mong muốn giải pháp:** **96.7% (29/30)** học viên bày tỏ mong muốn có một công cụ tự động tổng hợp task, deadline, thay đổi lịch từ Discord.

### Các số liệu định lượng chi tiết:
- **Số channel Discord phải theo dõi:**
  - 1–2 channel: 6.7% (2/30)
  - 3–5 channel: 46.7% (14/30)
  - 6–10 channel: 43.3% (13/30)
  - Trên 10 channel: 3.3% (1/30)
- **Tần suất kiểm tra Discord trong ngày:**
  - Trên 7 lần/ngày: 50.0% (15/30)
  - 5–7 lần/ngày: 26.7% (8/30)
  - 3–4 lần/ngày: 16.7% (5/30)
  - 1–2 lần/ngày: 6.6% (2/30)
- **Thời gian tiêu tốn mỗi ngày để lọc tin nhắn:**
  - 10–20 phút: 43.3% (13/30)
  - 5–10 phút: 36.7% (11/30)
  - Dưới 5 phút: 13.3% (4/30)
  - Trên 20 phút: 6.7% (2/30)
- **Khó khăn lớn nhất khi theo dõi:**
  - "Có quá nhiều tin nhắn" và "Tin quan trọng dễ bị trôi": 83.3% lựa chọn.
  - "Phải kiểm tra quá nhiều channel": 73.3% lựa chọn.
  - "Khó phân biệt tin nào cần làm ngay (Actionable) vs tin thảo luận": 56.7% lựa chọn.

### Trích dẫn câu trả lời nguyên văn (5 Quotes thực tế):
1. *"Do có quá nhiều tin nhắn mình đã để trôi thông tin quan trọng mà giảng viên gửi"* (Học viên phản hồi #4)
2. *"Suýt quên hoàn thành daily standup vì quá nhiều channel để check"* (Học viên phản hồi #8)
3. *"Bỏ lỡ workshop 1 và 2 do có quá nhiều kênh liên lạc"* (Học viên phản hồi #6)
4. *"Quên mất lịch workshop do tắt thông báo"* (Học viên phản hồi #5)
5. *"Không để ý task"* (Học viên phản hồi #9)

---

## 2. Khai phá dữ liệu có sẵn (`discord-pack/`) (Đạt Chuẩn B)
- **Quy mô tập tin:** 1.092 tin nhắn (779 tin từ học viên, 313 tin từ bot và ban tổ chức) giai đoạn 12–14/09 khoá 4.
- **Phân tích bản tin bot hiện tại:**
  - Có 4 bản tin tổng hợp hàng ngày do bot hiện tại tự động đăng.
  - **Lỗi nhận diện:** Bản tin chỉ liệt kê chung chung "học viên đang hỏi gì" dưới dạng văn bản cắt cụt; chèn chuỗi lỗi kỹ thuật "nguồn tham chiếu" vào giữa câu.
  - **Lỗ hổng cốt lõi:** Hoàn toàn thiếu tính năng trích xuất Task (việc cần làm), không trích xuất được Deadline chính xác và không xếp thứ tự ưu tiên cho các thông báo khẩn cấp (như thay đổi phòng học, dời giờ học).
