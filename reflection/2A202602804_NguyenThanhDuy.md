# BÁO CÁO THU HOẠCH CÁ NHÂN (INDIVIDUAL REFLECTION)

* **Họ và tên:** Nguyễn Thành Duy
* **Mã học viên:** `2A202602804`
* **Nhóm:** Magician (Phòng E403 · Lớp 3A)
* **Dự án:** Discord ActionDigest (Track B — Trợ lý Học viên)
* **Vai trò chính:** AI & Prompt Engineer

---

## 1. Vai trò cá nhân & Phần việc trực tiếp phụ trách

Trong dự án Discord ActionDigest, tôi trực tiếp phụ trách toàn bộ **kiến trúc Prompting, thiết kế tương tác với Large Language Model (LLM) và cơ chế chống ảo giác (Anti-hallucination)**:
- **Xây dựng System Prompt trung tâm ([`codebase/ai.py`](../codebase/ai.py)):** Định nghĩa rõ các phân loại nghiệp vụ cần bóc tách (`assignment`, `deadline`, `meeting`, `schedule_change`, `info`) và các nhóm nội dung bắt buộc phải bỏ qua (câu hỏi học viên, việc riêng, than thở, tán gẫu).
- **Chuẩn hóa đầu ra JSON Schema (Structured Output):** Ép buộc LLM luôn trả về mảng `items` có cấu trúc nghiêm ngặt gồm `source_message_id`, `type`, `title`, `deadline_iso`, `priority`, `confidence` và `reason` giải trình căn cứ.
- **Thiết kế cơ chế chống bịa giờ (Zero Hallucination Gate):** Xây dựng quy tắc ràng buộc mốc thời gian: chỉ cho phép điền `deadline_iso` khi tin nhắn gốc có mốc giờ cụ thể rõ ràng; nếu tin nhắn mơ hồ ("tối nay", "tuần này", "mai nộp"), bắt buộc LLM phải đặt `deadline_iso: null` và hạ điểm `confidence < 0.80` để giao diện bot cảnh báo người dùng.
- **Xử lý đặc thù nghiệp vụ lớp học (Domain Taxonomy):** Thiết lập logic nhận diện các từ khóa đính chính (`đổi`, `dời`, `chuyển`, `hủy`), tự động trích xuất thông tin mới nhất và giữ lại dấu vết phòng cũ để cảnh báo học viên.

---

## 2. Cách thức ứng dụng AI trong quá trình xây dựng sản phẩm

Tôi đã ứng dụng AI theo phương pháp tiếp cận kỹ thuật chuyên sâu (Prompt Engineering & Tool-assisted Development):
1. **A/B Testing Prompt & Few-shot Prompting:** Sử dụng LLM để thử nghiệm các biến thể System Prompt khác nhau, đánh giá phản ứng của mô hình khi tiếp nhận các mẫu tin nhắn thực tế từ `discord-pack/`.
2. **Kỹ thuật Delimited Guardrails:** Áp dụng các kỹ thuật phân tách vùng chỉ thị (Instruction) và vùng dữ liệu (Data) để hướng dẫn mô hình không bị nhầm lẫn giữa cấu trúc lệnh và nội dung hội thoại tự do của lớp học.
3. **Phát triển mã nguồn với AI Pair-programming:** Sử dụng AI để hỗ trợ viết code bất đồng bộ với thư viện `AsyncOpenAI`, tối ưu hóa việc phân tích chuỗi JSON trả về bằng regex fallback nhằm đảm bảo hệ thống không bao giờ bị crash khi LLM trả về format chưa hoàn hảo.

---

## 3. Một bài học thực tế rút ra từ trường hợp thất bại của nhóm

### Trường hợp thất bại cụ thể:
Tại đợt chạy benchmark 22 ca của Golden Set, tôi đã gặp 2 ca thất bại kỹ thuật rất điển hình:
1. **Ca `TC18` (Cắt cụt tin nhắn gộp nhiều deadline):** Tin nhắn *"Mọi người lưu ý 2 mốc quan trọng: CP1 nộp lúc 19:30 tối nay 16/9, còn CP2 nộp lúc 21:00 cùng ngày"*. Mô hình chỉ trích xuất được 1 mốc duy nhất (CP1 19:30) và bỏ sót hoàn toàn mốc thứ hai (CP2 21:00).
2. **Ca `TC14` (Bỏ sót việc đọc tài liệu):** Tin nhắn của GV *"Trước buổi học ngày mai, các bạn đọc tài liệu PAIR Guidebook..."*. Mô hình bỏ qua và không tạo task.

### Bài học xương máu rút ra:
Bài học kỹ thuật sâu sắc nhất mà tôi rút ra được là: **"Prompting quá tập trung vào một tập từ khóa hẹp sẽ tạo ra thiên kiến mù lòa (Keyword Bias), còn parsing tham lam (Greedy Parsing) sẽ luôn làm rơi rụng thông tin trong các câu đa mệnh đề."**
- Ở ca `TC14`, trong quá trình cố gắng giảm false positive (chống tin rác), tôi đã dặn LLM quá kỹ về các từ khóa nộp bài (`lab`, `quiz`, `spec`), vô tình khiến AI coi các yêu cầu đọc tài liệu chuẩn bị trước giờ học là tin nhắn giao tiếp thông thường.
- Ở ca `TC18`, LLM tự thỏa mãn ngay khi tìm thấy mốc thời gian đầu tiên trong câu và đóng gói thành 1 object JSON mà không quét tiếp các vế câu phía sau.
- **Hành động chuyển hóa:** Tôi nhận ra không thể giải quyết bài toán phức tạp chỉ bằng vài dòng mô tả chung chung. Tôi đã bổ sung ví dụ Few-shot phân rã đệ quy câu ghép thành nhiều object độc lập trong mảng `items`, đồng thời mở rộng danh mục `assignment` bao gồm cả `pre-class preparation`. Bài học này đã thay đổi hoàn toàn tư duy của tôi: **chất lượng của AI không nằm ở mô hình to hay nhỏ, mà nằm ở độ tỉ mỉ và chặt chẽ của các quy tắc biên (Edge-case boundary rules) do kỹ sư prompt thiết kế**.
