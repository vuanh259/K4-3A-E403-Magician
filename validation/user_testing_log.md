# User Testing Log — CP5

## 1. Mục tiêu kiểm thử

Mục tiêu của đợt kiểm thử CP5 là đánh giá khả năng sử dụng thực tế của **Discord Action Digest** với người dùng ngoài nhóm.

Nhóm tập trung quan sát các nội dung sau:

- Người dùng có hiểu cách gọi `/summary` hay không.
- Người dùng có hiểu các loại thông báo `DEADLINE`, `ASSIGNMENT`, `MEETING`, `SCHEDULE_CHANGE` hay không.
- Người dùng có hiểu ý nghĩa của chỉ số Confidence hay không.
- Người dùng có biết kiểm tra lại message nguồn hay không.
- Người dùng có sử dụng được `/correct` và `/done` hay không.
- Người dùng có phân biệt được `/summary` và `/tasks` hay không.

---

## 2. Danh sách người dùng thử nghiệm

| STT | Người thử | Vai trò | Thuộc willing users CP1 |
|---|---|---|---|
| 1 | **Lê Nguyễn Thái Dương** | Học viên khóa AI | Có |
| 2 | **Nguyễn Xuân Khuê** | Học viên khóa AI | Có |
| 3 | **Trần Minh Khôi** | Học viên khóa AI | Không |
| 4 | **Phạm Gia Huy** | Học viên khóa AI | Không |
| 5 | **Lê Hoàng Nam** | Học viên khóa AI | Không |

---

## 3. Nhiệm vụ giao cho người dùng

Mỗi người dùng được yêu cầu thực hiện các nhiệm vụ sau:

1. Dùng `/summary` để tìm các thông báo quan trọng trong 24 giờ gần nhất.
2. Xác định một task có deadline cụ thể.
3. Xác định một task có thông tin thời gian chưa rõ.
4. Mở message nguồn để kiểm tra lại kết quả AI.
5. Dùng `/correct` để chỉnh sửa một task.
6. Dùng `/done` để đánh dấu một task đã hoàn thành.

---

## 4. Kết quả quan sát

| Người thử | Nhiệm vụ giao | Điểm tắc nghẽn | Quote nguyên văn | Quyết định xử lý của nhóm |
|---|---|---|---|---|
| **Lê Nguyễn Thái Dương** | Dùng `/summary` để tìm deadline quan trọng | Chưa hiểu ngay ý nghĩa của chỉ số Confidence | **“Confidence 0.70 này nghĩa là bot chắc khoảng 70% đúng không?”** | Giữ chỉ số Confidence nhưng bổ sung cảnh báo bằng ngôn ngữ tự nhiên như **“Mốc giờ/thông tin cần xác nhận lại”** khi độ tin cậy thấp. |
| **Nguyễn Xuân Khuê** | Mở message nguồn để kiểm chứng kết quả AI | Ban đầu chỉ đọc nội dung AI mà chưa chú ý link nguồn | **“À, bấm vào nguồn là nó đưa về đúng tin nhắn Discord gốc luôn à?”** | Tiếp tục hiển thị link message nguồn rõ ràng trên mỗi item để người dùng dễ kiểm chứng. |
| **Vũ Đình Thư** | Tìm task có thời gian mập mờ | Không hiểu tại sao bot không tự hiện giờ deadline khi message chỉ nói “tối nay” | **“Nó nói tối nay rồi thì sao bot không hiện luôn giờ nộp?”** | Giữ nguyên nguyên tắc không tự bịa giờ. Với các message chỉ có “tối nay”, “mai”, “tuần này”, hệ thống gắn cảnh báo thay vì tự suy đoán giờ. |
| **Ngô Thế Khanh** | Dùng `/correct` sửa một item | Không biết Task ID cần lấy ở đâu | **“Task ID lấy ở đâu để sửa vậy?”** | Hiển thị `Task ID` rõ trên từng item và bổ sung hướng dẫn cú pháp `/correct`. |
| **Đỗ Tiến Anh** | Dùng `/done` đánh dấu task hoàn thành | Nghĩ `/done` sẽ làm task biến mất khỏi `/summary` | **“Ủa sao bấm done rồi mà trong summary vẫn còn task này?”** | Làm rõ rằng `/done` chỉ thay đổi trạng thái task trong `/tasks`, còn `/summary` vẫn hiển thị thông báo nguồn trong cửa sổ 24 giờ. |

---

## 5. Các vấn đề chính phát hiện được

### 5.1. Confidence chưa dễ hiểu với người dùng mới

Một số người dùng chưa hiểu ngay ý nghĩa của các giá trị như `0.70`, `0.96`.

**Quyết định:**  
Giữ chỉ số Confidence để đảm bảo tính minh bạch, đồng thời bổ sung cảnh báo dễ hiểu khi thông tin chưa chắc chắn:

`⚠️ Mốc giờ/thông tin cần xác nhận lại`

---

### 5.2. Người dùng có xu hướng tin kết quả AI trước khi kiểm tra nguồn

Khi bản summary trình bày rõ ràng, người dùng dễ đọc kết quả trực tiếp mà bỏ qua message gốc.

**Quyết định:**  
Mỗi item tiếp tục hiển thị:

- channel nguồn,
- tác giả,
- message gốc,
- link quay lại message trên Discord.

---

### 5.3. Thời gian tương đối dễ gây hiểu nhầm

Các cụm từ như:

- “tối nay”,
- “mai”,
- “tuần này”

không cung cấp đủ căn cứ để xác định chính xác giờ deadline.

**Quyết định:**  
Bot không tự gán các mốc giờ như `23:59`. Nếu thiếu giờ cụ thể, hệ thống giữ nguyên thông tin từ nguồn và gắn cảnh báo.

---

### 5.4. Cú pháp `/correct` chưa dễ khám phá

Một số người dùng chưa biết Task ID nằm ở đâu hoặc cách sử dụng lệnh sửa.

**Quyết định:**  
Hiển thị Task ID trực tiếp trên mỗi item và bổ sung hướng dẫn rõ hơn cho `/correct`.

---

### 5.5. Người dùng chưa phân biệt rõ `/summary` và `/tasks`

Một số người dùng nghĩ rằng khi gọi `/done`, item sẽ biến mất hoàn toàn khỏi hệ thống.

**Quyết định:**

- `/summary`: hiển thị các thông báo quan trọng có nguồn nằm trong cửa sổ 24 giờ.
- `/tasks`: hiển thị các task chưa hoàn thành.
- `/done`: chỉ thay đổi trạng thái task, không xóa thông báo nguồn khỏi `/summary`.

---

## 6. Thay đổi sản phẩm sau User Testing

Sau quá trình kiểm thử với người dùng ngoài nhóm, nhóm thực hiện các điều chỉnh sau:

1. Cải thiện cách hiển thị Confidence bằng cảnh báo ngôn ngữ tự nhiên.
2. Làm rõ link message nguồn để người dùng dễ kiểm chứng kết quả AI.
3. Không tự suy diễn deadline khi thiếu mốc giờ cụ thể.
4. Hiển thị Task ID rõ hơn để hỗ trợ `/correct`.
5. Làm rõ sự khác biệt giữa `/summary`, `/tasks` và `/done`.

---

## 7. Kết luận Validation

Qua kiểm thử với **5 người dùng ngoài nhóm**, người dùng có thể hoàn thành các luồng chính của sản phẩm gồm:

- gọi `/summary`,
- đọc Action Digest,
- kiểm tra message nguồn,
- chỉnh sửa task bằng `/correct`,
- đánh dấu task hoàn thành bằng `/done`.

Các điểm gây khó hiểu chủ yếu liên quan tới cách diễn giải Confidence, khả năng tìm Task ID và sự khác biệt giữa bản tổng hợp thông báo với trạng thái công việc.

Nhóm tiếp tục giữ kiến trúc **Conditional / Augment**, trong đó AI hỗ trợ trích xuất và phân loại thông tin nhưng người dùng vẫn có quyền kiểm tra nguồn và chỉnh sửa kết quả cuối cùng.