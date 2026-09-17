# BÁO CÁO THU HOẠCH CÁ NHÂN (INDIVIDUAL REFLECTION)

* **Họ và tên:** Trương Việt Anh
* **Mã học viên:** `2A202602444`
* **Nhóm:** Magician (Phòng E403 · Lớp 3A)
* **Dự án:** Discord ActionDigest (Track B — Trợ lý Học viên)
* **Vai trò chính:** Fullstack & Discord Integration Engineer

---

## 1. Vai trò cá nhân & Phần việc trực tiếp phụ trách

Trong đợt Hackathon, tôi chịu trách nhiệm chính về toàn bộ **hạ tầng phần mềm, kết nối Discord Bot thật và xây dựng trải nghiệm người dùng tương tác**:
- **Phát triển Discord Bot thật chạy trực tiếp ([`codebase/app.py`](../codebase/app.py)):** Sử dụng thư viện `discord.py`, tích hợp Slash Command Tree với 4 lệnh chính: `/summary`, `/tasks`, `/done`, `/correct`.
- **Thiết kế cơ sở dữ liệu SQLite ([`codebase/storage.py`](../codebase/storage.py)):** Xây dựng cấu trúc bảng lưu trữ các lần chạy digest, danh sách task cá nhân, trạng thái hoàn thành (`completed`), và cơ chế cập nhật chỉnh sửa đè dữ liệu.
- **Tiến trình nhắc hẹn tự động ([`codebase/reminders.py`](../codebase/reminders.py)):** Xây dựng background task chạy lặp tuần hoàn, tính toán thời gian thực tế theo múi giờ `Asia/Ho_Chi_Minh` và tự động gửi tin nhắn riêng (DM) nhắc nhở trước hạn chót 15 phút.
- **Thiết kế giao diện Discord Rich Embed ([`codebase/ui.py`](../codebase/ui.py)):** Trực quan hóa bản tin tổng hợp theo 3 cấp độ 🔴 High, 🟠 Medium, 🟢 Low, kèm trích dẫn nguyên văn người gửi và tạo link nhảy trực tiếp đến tin nhắn gốc `[Nguồn]({source_url})` (thỏa mãn HAX G11).
- **Xây dựng Companion Mockup Web (`codebase/index.html`):** Thiết kế giao diện mô phỏng 4 kịch bản bấm thử phục vụ slide thuyết trình và phương án dự phòng khi mất mạng.

---

## 2. Cách thức ứng dụng AI trong quá trình xây dựng sản phẩm

Tôi đã ứng dụng AI như một trợ lý lập trình tăng tốc (AI Copilot & Code Architect):
1. **Sinh mã nguồn khung (Boilerplate Generation):** Sử dụng LLM để sinh nhanh cấu trúc Discord bot hiện đại sử dụng Slash Commands (`@bot.tree.command`) và Dropdown Select Menu (`discord.ui.Select`), rút ngắn thời gian thiết lập hạ tầng từ vài tiếng xuống còn 30 phút.
2. **Xử lý bất đồng bộ và kiểm soát luồng dữ liệu:** Dùng AI hỗ trợ giải quyết các bài toán bất đồng bộ phức tạp trong Python (`asyncio`, `aiosqlite`) khi bot phải vừa lắng nghe lệnh người dùng, vừa gọi API AI phân tích, vừa duy trì tiến trình nhắc hẹn nền mà không làm nghẽn Event Loop.
3. **Chuyển hóa tài liệu thiết kế thành code giao diện:** Đưa các mô tả nguyên tắc HAX Toolkit (G1, G2, G9, G11) vào AI để gợi ý cách hiện thực hóa trực tiếp thành các thành phần màu sắc, nhãn cảnh báo và nút bấm trên Embed Discord.

---

## 3. Một bài học thực tế rút ra từ trường hợp thất bại của nhóm

### Trường hợp thất bại cụ thể:
Tại phiên kiểm thử người dùng thực tế theo phương pháp Mom Test ([`validation/user_testing_log.md`](../validation/user_testing_log.md)), bạn Lê Nguyễn Thái Dương (`2A202602383`) đã gặp phải một trải nghiệm cực kỳ ức chế:
- Khi bạn muốn dùng lệnh `/correct` để sửa giờ nộp bài Lab 2, bạn gõ `/correct task_id: 1 deadline_iso: 21:00`.
- Ngay lập tức, bot phản hồi thông báo lỗi vì tham số phức tạp và định dạng ISO rườm rà.
- Bạn Dương bực mình thốt lên: *"Cái lệnh `/correct` này lằng nhằng quá, vừa phải nhớ ID vừa phải gõ một đống tham số. Đang bận làm bài mà bắt ngồi gõ sửa lệnh cho bot thì phiền chết đi được, thà tui tự note ra ngoài cho xong!"*.

### Bài học xương máu rút ra:
Bài học đắt giá nhất đối với một lập trình viên Fullstack như tôi là: **"Tính năng phức tạp trên lý thuyết (Developer Design) có thể là rào cản thao tác tồi tệ trong đời thực (User Friction), và dũng cảm cắt bỏ tính năng thừa là một quyết định sản phẩm đúng đắn."**
- Khi thiết kế `/correct`, tôi nghĩ tính năng này sẽ rất hữu ích cho HAX G9. Nhưng qua kiểm thử thực tế với 5 học viên, mọi người đều đồng loạt phản ánh việc gõ lệnh sửa quá rườm rà và tính ứng dụng thực tế rất thấp. Người dùng không muốn làm "kỹ sư sửa dữ liệu" cho bot.
- **Hành động chuyển hóa (Changelog §9 — 18/9 CP5):** Nhóm đã đi đến quyết định dũng cảm là **xóa bỏ hoàn toàn chức năng `/correct`** để tinh gọn sản phẩm, tập trung tài nguyên vào việc tối ưu AI trích xuất chuẩn xác ngay từ đầu và hiển thị cảnh báo khi mốc giờ mơ hồ. Quyết định này giúp bot trở nên nhẹ nhàng, dễ tiếp cận và đúng với nhu cầu thực tế của học viên.
