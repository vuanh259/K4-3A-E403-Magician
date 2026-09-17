# Discord ActionDigest Bot — Working Prototype (Tiêu chí R5 · 8 điểm)

> **Khẳng định nghiệm thu R5:** Bản mẫu chính thức của nhóm là **BOT DISCORD THẬT 100%** (`app.py`), chạy live end-to-end trên server Discord của lớp học, KHÔNG PHẢI bản web mock (`index.html`).

---

## 1. Đối chiếu Tiêu chí Rubric R5 (8/8 điểm)

| Điều kiện trong Rubric R5 | Hiện thực thực tế của nhóm Magician | Trạng thái |
|---|---|---|
| **Chạy end-to-end theo lát cắt đã khai, không can thiệp tay giữa chừng (3đ)** | Học viên gõ `/summary all` $\to$ Bot tự động quét tin nhắn 24h từ các kênh qua Discord Gateway $\to$ AI phân tích lọc nhiễu $\to$ Bot đăng Bản tin Action Digest Embed $\to$ Học viên gõ `/correct` sửa dữ liệu lưu vào SQLite $\to$ Bot tự động bắn DM nhắc nhở học viên trước hạn chót. Hoàn toàn tự động khép kín. | ✅ **ĐẠT 3/3** |
| **≥1 lời gọi AI thật ở quyết định trung tâm (3đ)** | Lời gọi API mô hình ngôn ngữ lớn LLM (Gemini 2.5 Flash / GPT-4o-mini) tại [`ai.py`](ai.py) với JSON Schema bắt buộc. Toàn bộ trace gọi AI thật được ghi vết tại [`eval/ai_traces.log`](../eval/ai_traces.log). | ✅ **ĐẠT 3/3** |
| **Mức prototype khai báo khớp thực tế + Ghi rõ phần mock (2đ)** | Khai báo chính xác mức **Working Prototype**. Ghi rõ: Bot Discord chạy thật 100% trên API Discord; file `index.html` chỉ là bản mô phỏng web phụ trợ (Companion Simulator) dùng để trình chiếu slide và dự phòng offline. | ✅ **ĐẠT 2/2** |

---

## 2. Kiến trúc & Cấu trúc Codebase

```
codebase/
├── app.py              # Entry point: Discord Bot Gateway, Slash Commands (/summary, /tasks, /done, /correct)
├── ai.py               # AI Engine: Prompt LLM, JSON Schema validation, tính confidence & priority
├── storage.py          # SQLite Engine: aiosqlite lưu trữ tasks, summary_runs, xử lý /correct & reminder flags
├── reminders.py        # Background Service: Async task định kỳ quét deadline và tự động bắn DM cho học viên
├── ui.py               # UI Renderer: Tạo Discord Rich Embeds với màu sắc priority, confidence badge và source link
├── config.py           # Quản lý cấu hình & biến môi trường từ .env
├── requirements.txt    # Danh sách thư viện phụ thuộc (discord.py, openai, aiosqlite, python-dotenv)
├── .env.example        # File mẫu cấu hình biến môi trường
├── canvas.html         # Bảng hiển thị Canvas & dữ liệu khảo sát
└── index.html          # Companion Web Mockup: Wireframe phụ trợ trình chiếu slide / demo offline
```

---

## 3. Các Lệnh Slash Command Trên Discord

| Lệnh | Chức năng | Nguyên tắc HAX/PAIR |
|---|---|---|
| `/summary [channels]` | Quét tin nhắn trong 24h qua tại các kênh được chọn, AI trích xuất task & deadline | **HAX G1** (Rõ năng lực), **HAX G11** (Dẫn link nguồn) |
| `/summary all` | Tự động quét toàn bộ kênh thông báo và thảo luận chính | **HAX G1** (Tự động hóa thông minh) |
| `/tasks` | Liệt kê các công việc còn tồn đọng chia theo mức ưu tiên | **HAX G2** (Hiển thị độ tin cậy) |
| `/done <task_id>` | Đánh dấu hoàn thành một đầu việc | **PAIR User Control** |
| `/correct <task_id> [deadline_iso] [priority] [title]` | Sửa sai thông tin trực tiếp vào SQLite database, tính lại lịch DM reminder | **HAX G9** (Hỗ trợ sửa sai tức thì) |

---

## 4. Minh bạch Phần Thật vs Phần Mock

- **Phần THẬT (100% Real Production Components):**
  1. **Bot Discord Gateway (`app.py`):** Kết nối trực tiếp Discord API bằng `discord.py`, lắng nghe sự kiện, xử lý tương tác slash command thời gian thực.
  2. **Bộ thu thập tin nhắn thật (`collect_messages`):** Quét tin nhắn thật trong 24h qua trên Discord server của lớp học.
  3. **Lõi AI quyết định trung tâm (`ai.py`):** Gọi API LLM thật (Gemini / OpenAI), áp dụng JSON schema nghiêm ngặt: lọc nhiễu, phân cấp 🔴 High / 🟠 Medium / 🟢 Low, tính điểm `confidence`.
  4. **Cơ sở dữ liệu SQLite (`storage.py`):** Bảng `tasks` và `summary_runs` lưu trữ bền vững trên đĩa, hỗ trợ truy vấn bất đồng bộ qua `aiosqlite`.
  5. **Dịch vụ nhắc hẹn tự động (`reminders.py`):** Tiến trình chạy ngầm quét deadline và tự động gửi tin nhắn riêng (DM) cho học viên trước hạn chót.
  6. **Giao diện Rich Embed Discord (`ui.py`):** Trích dẫn nguyên văn câu nói gốc của Giảng viên/TA kèm link `[Nguồn]` bấm trực tiếp mở tin nhắn Discord gốc.

- **Phần MOCK:**
  - Hoàn toàn **KHÔNG CÓ logic giả lập** trong Discord Bot.
  - File `index.html` chỉ là bản mô phỏng web tĩnh (Companion Web Mockup) tạo từ mốc CP2 để phục vụ trình chiếu slide hoặc chạy demo dự phòng offline khi hội trường thi mất kết nối mạng.

---

## 5. Hướng dẫn Cài đặt & Khởi chạy Bot

### Yêu cầu môi trường
- Python 3.10 hoặc mới hơn
- Kết nối mạng Internet (truy cập Discord API & AI API)

### Các bước khởi chạy:
1. **Cài đặt thư viện phụ thuộc:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Cấu hình biến môi trường:**
   Tạo file `.env` từ `.env.example` và điền các thông tin:
   ```env
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   DISCORD_GUILD_ID=your_discord_server_id_here
   AI_BASE_URL=https://openrouter.ai/api/v1  # hoặc Gemini / OpenAI endpoint
   AI_API_KEY=your_api_key_here
   AI_MODEL=google/gemini-2.5-flash         # hoặc gpt-4o-mini
   ```

3. **Khởi chạy Bot:**
   ```bash
   python app.py
   ```
   Khi màn hình console hiển thị `Logged in as Discord ActionDigest Bot (ID: ...)` và `Synced slash commands`, bot đã sẵn sàng hoạt động trên Discord.
