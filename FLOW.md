# SƠ ĐỒ LUỒNG TRẢI NGHIỆM NGƯỜI DÙNG (USER FLOW DIAGRAM) — CP2
**Dự án:** Discord Action Digest · **Nhóm:** Magician · **Phòng:** E403  
**Bản mẫu tương tác:** `codebase/index.html` (Mô phỏng Trợ lý Discord Bot Simulator)

---

## 1. Sơ đồ Luồng Trải Nghiệm Tương Tác (User Flowchart)

```mermaid
flowchart TD
    Start([Học viên mở giao diện Discord / Trợ lý Action Digest]) --> InputChoice{Học viên đưa ra yêu cầu}
    
    InputChoice -- "Gõ câu lệnh tự do / Chọn prompt: 'tìm cho tôi những vấn đề quan trọng hôm nay'" --> Router[AI Query & Intent Router]
    InputChoice -- "Hỏi về task mập mờ: 'khi nào nộp lab 2?'" --> Router
    InputChoice -- "Hỏi đổi lịch: 'có lịch nào bị đổi không?'" --> Router
    InputChoice -- "Hỏi ngoài phạm vi: 'giải thích Transformer'" --> Router

    Router --> IntentCheck{Phân loại câu hỏi}

    %% Nhánh 1: Ngoài phạm vi
    IntentCheck -- "Hỏi lý thuyết / Giải thích code / Điểm danh [HAX G1]" --> OutOfScope[Từ chối lịch sự: Nêu rõ chỉ hỗ trợ Task/Lịch, hướng dẫn gặp VLearn Tutor]
    
    %% Nhánh 2: Quét tin tức thông báo
    IntentCheck -- "Yêu cầu tổng hợp / Tra cứu thông tin" --> DataScan[Đọc luồng tin nhắn từ kênh thông báo]
    
    DataScan --> PreFilter[Bộ lọc tiền xử lý: Loại bỏ tin rác, tán gẫu cafe, sticker]
    
    PreFilter --> ExtractEngine[AI Extractor Engine: Bóc tách Task, Deadline, Người gửi & Trích dẫn gốc]

    ExtractEngine --> ConfidenceCheck{Kiểm tra độ tin cậy mốc thời gian}
    
    %% Nhánh Low-confidence
    ConfidenceCheck -- "Mốc giờ mơ hồ: 'tối nay', 'mai' [HAX G2]" --> FlagAmbiguous[Gắn nhãn: ⚠️ Mốc giờ chưa cụ thể\nGiữ nguyên quote gốc, tuyệt đối không bịa 23:59]
    
    %% Nhánh Happy path
    ConfidenceCheck -- "Mốc giờ chính xác: ngày, giờ rõ ràng" --> ConfirmTime[Xác thực mốc thời gian chính thức]
    
    FlagAmbiguous --> PrioritySort{Phân loại mức độ ưu tiên}
    ConfirmTime --> PrioritySort
    
    PrioritySort -- "Dời lịch học/phòng học HOẶC Deadline < 24h" --> P1[🔴 P1 · KHẨN CẤP]
    PrioritySort -- "Task bài tập mới / Deadline > 24h" --> P2[🟡 P2 · QUAN TRỌNG]
    PrioritySort -- "Nhắc nhở định kỳ / Tài liệu đọc trước" --> P3[🟢 P3 · THEO DÕI]
    
    P1 --> RenderDigest[Render Bản Tin Discord Embed Card]
    P2 --> RenderDigest
    P3 --> RenderDigest
    
    OutOfScope --> RenderChat([Hiển thị tin nhắn trả lời trong khung Chat])
    RenderDigest --> RenderChat
    
    RenderChat --> UserInteraction{Học viên xem kết quả & tương tác}
    
    UserInteraction -- "Hài lòng với thông tin" --> EndOk([Hoàn thành tra cứu trong 30 giây])
    UserInteraction -- "Phát hiện sai lệch hoặc muốn đính chính [HAX G9]" --> OpenCorrection[Bấm nút 'Sửa hạn nộp' -> Mở Modal sửa trực tiếp]
    
    OpenCorrection --> SaveCorrection[Cập nhật lại thẻ hiển thị & Tự động ghi log vào validation/corrections.log]
    SaveCorrection --> EndOk
```

---

## 2. Bốn Kịch Bản Trải Nghiệm Thể Hiện Trên Bản Mẫu `codebase/index.html`

| Kịch bản | Thao tác trên `index.html` | Hành vi hệ thống & Nguyên tắc áp dụng |
|---|---|---|
| **1. Đường thuận lợi (Happy path)** | Nhập: *"tìm cho tôi những vấn đề quan trọng hôm nay"* hoặc bấm nút gợi ý 1 | AI quét luồng tin, trích xuất đầy đủ 4 thẻ việc thuộc P1, P2, P3. Mỗi thẻ có mốc giờ, người thông báo và trích dẫn gốc (**HAX G11**). |
| **2. Đường thiếu tự tin (Low-confidence)** | Nhập: *"khi nào nộp lab 2?"* hoặc bấm nút gợi ý 2 | AI phát hiện tin nhắn của TA chỉ nói "nộp vào tối nay" $\to$ Không tự bịa 23:59, gắn nhãn vàng cảnh báo `[⚠️ Mốc giờ chưa cụ thể]` (**HAX G2**). |
| **3. Đường ngoài phạm vi (Failure / Out-of-scope)** | Nhập: *"giải thích thuật toán Transformer cho tôi"* hoặc bấm nút gợi ý 4 | AI từ chối hữu ích: Giải thích rõ bot chỉ quản lý task/lịch, hướng dẫn học viên liên hệ VLearn Tutor (**HAX G1**). |
| **4. Cơ chế can thiệp sửa đổi (Correction path)** | Bấm nút *"Sửa hạn nộp"* trên bất kỳ thẻ công việc nào | Mở modal popup cho phép học viên trực tiếp chỉnh sửa tiêu đề task, mốc deadline, và đổi mức ưu tiên P1/P2/P3 (**HAX G9**). |

---

## 3. Khớp Nối Kỹ Thuật Với Đề Bài (Rubric CP2)
- **Mức Prototype:** Bản mẫu tương tác (Clickable prototype) chạy trực tiếp trên file HTML tĩnh `codebase/index.html`, không phụ thuộc backend phức tạp, tải ngay lập tức.
- **Tính thông suốt:** Luồng từ đầu vào (Chat input) $\to$ Xử lý kịch bản $\to$ Đầu ra (Embed card) $\to$ Tương tác sửa đổi hoạt động mượt mà, không có ngõ cụt.
- **Minh chứng kiểm tra:** Có thể bấm thử trực tiếp trên trình duyệt hoặc chạy file kiểm thử dòng lệnh `codebase/chat_bot.py`.
