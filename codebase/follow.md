# Luồng chạy dự án Discord Action Digest

Dưới đây là luồng chạy theo cột từ trên xuống, bám sát code hiện tại và có thể dùng trực tiếp để chuẩn bị demo.

## 1. Luồng tổng thể của hệ thống

```text
┌──────────────────────────────────────────┐
│ 1. Bot được khởi động bằng python app.py │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Bot đăng nhập Discord                    │
│ Đồng bộ các slash command vào server     │
│ Khởi động dịch vụ kiểm tra reminder      │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Người dùng thao tác trong Discord        │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Các command có thể sử dụng:              │
│                                          │
│ /summary                                 │
│ /tasks                                   │
│ /correct                                 │
│ /done                                    │
│ /test_reminder                           │
└──────────────────────────────────────────┘
```

## 2. Luồng chính `/summary`

Đây nên là luồng demo chính.

```text
┌──────────────────────────────────────────┐
│ Người dùng nhập /summary                 │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Bot kiểm tra vị trí sử dụng command      │
└──────────────────────────────────────────┘
                    ↓
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
   Dùng trong DM         Dùng trong server
          │                   │
          ▼                   ▼
 Bot thông báo:       Bot hiển thị bảng chọn
 "Hãy dùng /summary   channel ở chế độ riêng tư
 trong server"        chỉ người dùng nhìn thấy
                              ↓
┌──────────────────────────────────────────┐
│ Người dùng chọn một trong hai cách:      │
│                                          │
│ 1. Tick từ 1 đến 10 channel              │
│ 2. Bấm "Quét tất cả channel khả dụng"    │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Bot kiểm tra quyền trên từng channel:    │
│                                          │
│ • View Channel                           │
│ • Read Message History                   │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Bot đọc tin nhắn trong 24 giờ gần nhất   │
│                                          │
│ Tối đa 40 message mỗi channel            │
│ Bỏ qua message do bot gửi                │
│ Bỏ qua message không có nội dung         │
│ Sắp xếp message từ cũ đến mới            │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Có tìm thấy message hợp lệ không?        │
└──────────────────────────────────────────┘
                    ↓
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
       Không có              Có message
          │                   │
          ▼                   ▼
 Bot thông báo:       Bot gửi các message sang AI
 "Không tìm thấy      kèm theo:
 message trong        • Thời gian hiện tại
 24 giờ gần nhất"     • Múi giờ Việt Nam
                      • ID, tác giả, channel
                      • Nội dung và link nguồn
                              ↓
┌──────────────────────────────────────────┐
│ AI phân tích message                     │
│                                          │
│ • Phát hiện bài tập/task                 │
│ • Phát hiện deadline                     │
│ • Phát hiện lịch học/cuộc họp            │
│ • Phát hiện thay đổi lịch/phòng          │
│ • Loại bỏ tán gẫu và nội dung nhiễu      │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ AI trả về JSON gồm:                      │
│                                          │
│ • source_message_id                      │
│ • type                                   │
│ • title                                  │
│ • action_required                        │
│ • deadline_iso                           │
│ • priority                               │
│ • confidence                             │
│ • reason                                 │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Hệ thống kiểm chứng nguồn                │
│                                          │
│ source_message_id có tồn tại trong       │
│ danh sách message ban đầu không?         │
└──────────────────────────────────────────┘
                    ↓
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
  Không tồn tại          Có tồn tại
          │                   │
          ▼                   ▼
 Loại bỏ kết quả      Lấy lại thông tin nguồn
 vì AI có thể đã      từ dữ liệu Discord thật:
 bịa nguồn            • Channel
                      • Tác giả
                      • Nội dung
                      • Link message
                              ↓
┌──────────────────────────────────────────┐
│ Lọc các item có thể hành động            │
│                                          │
│ • assignment                             │
│ • deadline                               │
│ • meeting                                │
│ • schedule_change                        │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Lưu task vào SQLite                      │
│                                          │
│ • Người sở hữu task                      │
│ • Tiêu đề                                │
│ • Priority                               │
│ • Deadline                               │
│ • Nguồn                                  │
│ • Trạng thái: open                       │
│ • Reminder chưa gửi                      │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Lưu lịch sử lần chạy summary             │
│                                          │
│ • Người chạy                             │
│ • Server                                 │
│ • Các channel                            │
│ • Số message đã đọc                      │
│ • Số task trích xuất                     │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Bot tạo Discord Embed                    │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Kết quả được gửi công khai vào channel   │
│ nơi người dùng chạy /summary             │
└──────────────────────────────────────────┘
```

## 3. Nội dung kết quả `/summary`

Mỗi task trong Embed dự kiến có:

```text
🔴/🟠/🟢 Loại task · Tiêu đề

Task ID: 3
Deadline: 2026-09-17T21:00:00+07:00
Lý do: Đây là deadline bắt buộc cần hoàn thành.

Nguồn: #general · Tên người gửi
> Nội dung message gốc

Confidence: 0.95
```

Phân loại mức ưu tiên:

```text
🔴 HIGH   → Khẩn cấp hoặc deadline gần
🟠 MEDIUM → Quan trọng nhưng chưa quá gấp
🟢 LOW    → Cần theo dõi
```

Nếu AI không tìm thấy việc có đủ căn cứ:

```text
Không có việc quan trọng rõ ràng.

AI không tìm thấy task/deadline/thay đổi lịch
có đủ căn cứ.
```

## 4. Luồng `/tasks`

```text
┌──────────────────────────────────────────┐
│ Người dùng nhập /tasks                   │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Bot lấy các task của chính người dùng    │
│ có trạng thái status = open              │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Sắp xếp theo:                            │
│                                          │
│ 1. Priority: high → medium → low         │
│ 2. Task có deadline trước                │
│ 3. Deadline gần hơn trước                │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Bot trả về danh sách task riêng tư       │
│ Chỉ người chạy command nhìn thấy         │
└──────────────────────────────────────────┘
```

Ví dụ:

```text
/tasks
```

Kết quả:

```text
🗂️ Việc đang theo dõi

🔴 #3 · Nộp AI Spec
Loại: assignment
Deadline: 2026-09-17T21:00:00+07:00
Nguồn: #general
```

## 5. Luồng `/correct`

Dùng khi AI trích xuất sai.

```text
┌──────────────────────────────────────────┐
│ Người dùng nhập /correct                 │
│                                          │
│ • task_id bắt buộc                       │
│ • deadline_iso tùy chọn                  │
│ • priority tùy chọn                      │
│ • title tùy chọn                         │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Bot kiểm tra task có thuộc người dùng    │
│ đang sửa hay không                       │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Nếu có priority, kiểm tra giá trị:       │
│ high / medium / low                      │
└──────────────────────────────────────────┘
                    ↓
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
     Không hợp lệ          Hợp lệ
          │                   │
          ▼                   ▼
 Thông báo lỗi       Cập nhật task trong SQLite
                              ↓
                     Reset reminder_sent = 0
                              ↓
                     Bot thông báo:
                     "Đã cập nhật"
```

Ví dụ:

```text
/correct
task_id: 3
deadline_iso: 2026-09-17T22:00:00+07:00
priority: high
title: Nộp bản AI Spec hoàn chỉnh
```

Kết quả dự kiến:

```text
✏️ Đã cập nhật.
Reminder sẽ được tính lại nếu deadline thay đổi.
```

## 6. Luồng `/done`

```text
┌──────────────────────────────────────────┐
│ Người dùng nhập /done task_id:<ID>       │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Bot tìm task theo:                       │
│ • Task ID                                │
│ • User ID                                │
│ • Trạng thái open                        │
└──────────────────────────────────────────┘
                    ↓
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
 Không tìm thấy          Tìm thấy task
          │                   │
          ▼                   ▼
 "Không tìm thấy      Chuyển status thành done
 task của bạn"                   ↓
                       "Đã đánh dấu hoàn thành"
```

Ví dụ:

```text
/done task_id:3
```

Task đã hoàn thành sẽ không còn xuất hiện trong `/tasks` và không được gửi reminder.

## 7. Luồng reminder tự động

Luồng này chạy nền, không cần người dùng nhập command.

```text
┌──────────────────────────────────────────┐
│ Bot kiểm tra database mỗi 20 giây        │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Tìm task thỏa mãn:                       │
│                                          │
│ • status = open                          │
│ • reminder_sent = 0                      │
│ • Có deadline                            │
│ • Deadline còn tối đa 30 phút            │
│ • Deadline chưa qua                      │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Bot tìm Discord user sở hữu task         │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Gửi tin nhắn DM riêng                    │
│                                          │
│ • Tiêu đề task                           │
│ • Deadline                               │
│ • Channel và tác giả nguồn               │
│ • Link message gốc                       │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Đánh dấu reminder_sent = 1               │
│ để tránh gửi lặp                         │
└──────────────────────────────────────────┘
```

## 8. Luồng `/test_reminder`

Dùng để demo nhanh mà không phải chờ deadline thật.

```text
┌──────────────────────────────────────────┐
│ Người dùng nhập /test_reminder           │
│ seconds: 3–60 giây                       │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Bot thông báo riêng tư:                  │
│ "Bot sẽ DM sau X giây"                   │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Bot chờ X giây                           │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ Bot gửi DM reminder mẫu cho người dùng   │
└──────────────────────────────────────────┘
```

Ví dụ:

```text
/test_reminder seconds:6
```

## 9. Kịch bản demo đề xuất

```text
1. Mở channel #general có 3–4 message giả lập
                    ↓
2. Chạy /summary
                    ↓
3. Chọn #general
                    ↓
4. Cho khán giả xem bot quét message
                    ↓
5. Hiển thị Action Digest có nguồn trích dẫn
                    ↓
6. Chạy /tasks để xem task đã được lưu
                    ↓
7. Chạy /correct để sửa một deadline
                    ↓
8. Chạy lại /tasks để chứng minh dữ liệu đã đổi
                    ↓
9. Chạy /test_reminder seconds:6
                    ↓
10. Mở DM để cho thấy reminder
                    ↓
11. Chạy /done với một Task ID
                    ↓
12. Chạy lại /tasks để chứng minh task đã hoàn thành
```

Điểm cần nói rõ khi demo: `/summary all` không phải command thật của bot hiện tại. Người dùng chạy `/summary`, sau đó chọn channel hoặc bấm nút **Quét tất cả channel khả dụng**.
