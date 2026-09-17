# CP5 — Báo cáo Thử nghiệm Người dùng Thực tế (User Validation Report)
## Discord Action Digest · Nhóm Magician · Phòng E403 · Lớp 3A

---

## 1. Mục tiêu kiểm thử (CP5 Validation Objectives)

Mục tiêu của đợt kiểm thử thực tế tại Checkpoint 5 (CP5) là kiểm chứng năng lực giải quyết vấn đề và tính khả dụng của **Discord Action Digest** trên người dùng thật ngoài nhóm.

Khác với bộ kiểm thử tự động Golden Set (CP3–CP4) tập trung vào đo lường kỹ thuật thuật toán, CP5 tập trung vào **hành vi thực tế (Behavioral Usability)**:
- Người dùng có tự điều khiển được bot bằng `/summary` để nắm bắt thông tin quan trọng trong ngày mà không cần lội đọc từng kênh Discord không?
- Người dùng có hiểu đúng ý nghĩa của cảnh báo độ tin cậy thấp (`Confidence: 0.70 ⚠️`) và việc AI không tự bịa giờ `23:59` không?
- Trải nghiệm thực tế với lệnh `/correct` có thực sự hữu ích hay gây thêm rào cản thao tác (friction)?
- Người dùng có phân biệt được ranh giới giữa bản tin 24h (`/summary`) và danh sách việc cá nhân (`/tasks`), cách đóng task bằng `/done`?
- Action Digest có thực sự cắt giảm thời gian theo dõi thông tin từ **5–10 phút xuống còn 2–3 phút** như mục tiêu của Canvas CP1 không?

---

## 2. Phương pháp kiểm thử (The Mom Test Protocol)

Nhóm áp dụng triệt để nguyên tắc **The Mom Test (Rob Fitzpatrick)** và quy trình kiểm thử người dùng **Stanford CS177**:
1. **Giao nhiệm vụ theo Outcome (Mục tiêu đầu ra):** Không chỉ trỏ màn hình hay mớm nút bấm, để người dùng tự do thao tác.
2. **Im lặng quan sát hành vi:** Người điều phối không cầm chuột, không gõ phím hộ, không giải thích thay bot.
3. **Cứu hộ trung tính:** Nếu người dùng bị kẹt, chỉ dùng các câu gợi mở: *"Bạn cứ nói to suy nghĩ trong đầu ra nhé"*, *"Bạn dự định làm gì tiếp theo?"*.
4. **Tuyệt đối không hỏi câu xã giao:** Cấm hỏi *"Bạn thấy bot có hay không?"*. Thay vào đó, tập trung ghi chép chính xác điểm tắc nghẽn và trích dẫn nguyên văn câu nói lúc họ gặp khó khăn.
5. **Dựa trên hành vi thật để ra quyết định sản phẩm:** Lời nói dối lịch sự bị loại bỏ; chỉ giữ lại những phản hồi có bằng chứng hành vi để điều chỉnh sản phẩm.

---

## 3. Danh sách người dùng tham gia kiểm thử

| STT | Người thử | Mã học viên | Vai trò trong lớp học | Nhóm người dùng |
|:---:|---|:---:|---|:---:|
| 1 | **Lê Nguyễn Thái Dương** | `2A202602383` | Học viên lớp 3A (Nhóm khác) | ✅ Willing User cam kết từ CP1 |
| 2 | **Nguyễn Xuân Khuê** | `2A202602999` | Học viên lớp 3A (Nhóm khác) | ✅ Willing User cam kết từ CP1 |
| 3 | **Nguyễn Minh Lương** | `2A202602488` | Học viên lớp 3A | Người dùng kiểm thử mở rộng |
| 4 | **Nguyễn Duy Phong** | `2A202602655` | Học viên lớp 3A | Người dùng kiểm thử mở rộng |
| 5 | **Nguyễn Quốc Việt** | `2A202602789` | Học viên lớp 3A | Người dùng kiểm thử mở rộng |

* **Thời gian thực hiện:** 14:00 – 16:30 ngày 18/09/2026
* **Địa điểm:** Phòng E403 / Server Discord thực tế của khóa học AI Thực Chiến
* **Điều phối viên (Facilitator):** Nguyễn Vũ Anh (Team Lead)
* **Thư ký ghi chép (Note-taker):** Phạm Quang Đạt (QA Lead)

---

## 4. Bảng tổng hợp nhật ký kiểm thử người dùng (Scaffold User Testing Log)

> Bảng chuẩn hóa đối chiếu trực tiếp giữa hành vi thực tế của 5 người dùng thử nghiệm và các quyết định kỹ thuật được phản ánh trong **`## §9. Changelog`** của tài liệu `spec.md`.

| Người thử | Nhiệm vụ giao | Điểm tắc nghẽn | Trích dẫn nguyên văn | Quyết định xử lý của nhóm |
|---|---|---|---|---|
| **Lê Nguyễn Thái Dương** | Sửa lại mốc giờ nộp bài Lab 2 bị AI hiểu sai hoặc thiếu giờ khi nhận được nhắc việc. | **Thao tác dùng `/correct` quá rườm rà:** Bắt buộc người dùng phải nhớ `task_id`, nhập chuỗi định dạng ISO-8601 dài ngoằng hoặc gõ nhiều tham số phức tạp. Người dùng cảm thấy phiền toái, thà tự nhớ lịch còn hơn mất công gõ lệnh sửa cho bot. | *"Cái lệnh `/correct` này lằng nhằng quá, vừa phải nhớ ID vừa phải gõ một đống tham số. Đang bận làm bài mà bắt ngồi gõ sửa lệnh cho bot thì phiền chết đi được, thà tui tự note ra ngoài cho xong!"* | **Xóa bỏ chức năng `/correct` khỏi sản phẩm (Changelog §9 — 18/9 CP5):** Do nhóm người dùng thử cảm thấy khó dùng, thao tác rườm rà và tính ứng dụng thực tế không cao. Tinh gọn bot, tập trung tối đa vào độ chính xác của khâu trích xuất tự động và cơ chế nhắc hẹn thay vì bắt người dùng làm "kỹ sư sửa dữ liệu". |
| **Nguyễn Xuân Khuê** | Kiểm tra thông tin các bài tập và hạn nộp trong 24 giờ qua từ server Discord lớp học. | **Băn khoăn với thông tin mơ hồ:** Gặp tin nhắn TA thông báo *"nộp lab vào tối nay"*, thấy bot trích xuất task nhưng không có giờ nộp cụ thể (`null`). Khuê lo lắng liệu bot có tự ý gán giờ mặc định `23:59` như các tool khác dẫn đến nộp muộn nếu hạn thật là `21:00`. | *"Thông báo chỉ bảo 'nộp tối nay' mà không ghi mấy giờ, nếu bot tự gán 23:59 như mấy con bot khác là tui toi mạng nếu hạn thật là 21:00. May mà con này nó để mốc giờ trống và hiện cảnh báo chấm than vàng."* | **Giữ cơ chế cảnh báo cho thông tin mơ hồ thay vì tự suy diễn deadline (Changelog §9 — 18/9 CP5):** Với tin nhắn như *"nộp tối nay"*, hệ thống kiên quyết để `deadline_iso: null` và hiển thị nhãn `Confidence: 0.70 ⚠️ (Mốc giờ cần xác nhận lại)`, tuyệt đối không tự bịa giờ `23:59` để bảo vệ an toàn cho học viên (Zero Hallucination). |
| **Nguyễn Minh Lương** | Khám phá và sử dụng hai lệnh `/summary` và `/tasks` để kiểm tra công việc cần làm. | **Nhầm lẫn ranh giới tính năng:** Người dùng không phân biệt được mục đích của `/summary` và `/tasks`, tưởng rằng hai lệnh này trả về cùng một danh sách dữ liệu nên cảm thấy thừa thãi. | *"Ủa `/summary` với `/tasks` khác gì nhau ta? Tưởng gõ cái nào cũng ra danh sách việc cần làm chứ sao lại chia ra hai lệnh làm gì cho rối mắt người dùng?"* | **Làm rõ vai trò độc lập giữa `/summary` và `/tasks` (Changelog §9 — 18/9 CP5):** Định hình rõ mental model trong hướng dẫn và phản hồi bot: `/summary` là bản tin tổng hợp sự kiện quan trọng trong 24 giờ của kênh (để đọc lướt), còn `/tasks` là sổ tay cá nhân chỉ chứa các việc chưa hoàn thành (để theo dõi làm bài). |
| **Nguyễn Duy Phong** | Đánh dấu một bài tập đã làm xong bằng lệnh `/done` và kiểm tra lại trạng thái. | **Hiểu sai cơ chế đồng bộ giao diện:** Sau khi gõ `/done task_id: 12`, Phong kéo chuột lên xem lại bản tin `/summary` cũ trong kênh chung, thấy thẻ bài tập vẫn còn màu đỏ nguyên vẹn, liền nghĩ rằng bot bị lỗi không ghi nhận kết quả. | *"Ủa mình gõ `/done` bot báo thành công rồi mà sao kéo lên cái tin tổng hợp lúc nãy nó vẫn hiện task đó màu đỏ lè vậy? Tưởng nó phải tự xóa mất tiêu luôn chứ?"* | **Làm rõ cơ chế hoạt động của `/done` (Changelog §9 — 18/9 CP5):** Giải thích rõ `/done` là đóng task khỏi danh sách theo dõi cá nhân (`/tasks`), không xóa tin nhắn lịch sử trong `/summary` vì `/summary` là nhật ký thông tin 24 giờ của kênh chung cho cả lớp cùng xem. |
| **Nguyễn Quốc Việt** | Đọc bản tin Action Digest và kiểm tra thông tin thông báo dời phòng học buổi chiều. | **Áp lực tâm lý phải kiểm tra lại nguồn:** Thấy mỗi thẻ đều có link `[Xem message gốc]`, Việt tưởng rằng quy trình bắt buộc là phải bấm vào từng link để đọc lại tin nhắn gốc trên Discord, làm mất đi ý nghĩa tiết kiệm thời gian của bản tin. | *"Cái link [Xem message gốc] này có bắt buộc phải bấm vào từng cái để check lại không? Nếu cái nào cũng phải bấm mở Discord ra đọc lại thì dùng bot tóm tắt làm gì nữa, thà lướt chat từ đầu cho nhanh!"* | **Làm rõ vai trò của link `Nguồn` chỉ là Safety Net (Changelog §9 — 18/9 CP5):** Hướng dẫn rõ ràng rằng link nguồn chỉ đóng vai trò bảo chứng an toàn khi cần kiểm chứng (với task có confidence thấp hoặc tin đổi lịch khẩn cấp), người dùng không cần và không bắt buộc phải mở cho mọi item trong luồng bình thường. |

---

## 5. Chi tiết 5 phiên quan sát hành vi người dùng (Detailed Observation Logs)

### 5.1. Phiên 1: Lê Nguyễn Thái Dương (Willing User 1)
- **Thiết bị:** Discord Desktop Client trên MacOS.
- **Diễn biến thao tác:**
  - `00:00 - 00:30`: Gõ lệnh `/summary`, chọn kênh `#thong-bao-chung` và `#bai-tap`. Bot phản hồi bản tin Embed rất nhanh.
  - `00:30 - 01:45`: Nhìn thấy task nhắc hẹn cuộc họp lúc 14:00 bị sai giờ (thực tế họp lúc 22:00). Dương cố gắng tìm cách sửa.
  - `01:45 - 03:30`: Gõ lệnh `/correct`. Form hiện ra hàng loạt tham số (`task_id`, `deadline_iso`, `priority`, `title`). Dương bối rối vì không biết phải nhập format ISO ra sao, gõ thử `22:00` bị bot báo lỗi validation, sau đó phải đọc hướng dẫn để gõ chuỗi ngày giờ đầy đủ.
  - `03:30 - 04:00`: Dương hoàn thành việc sửa nhưng tỏ thái độ cực kỳ không hài lòng với trải nghiệm gõ lệnh này.
- **Nhận định của nhóm:** Tính năng `/correct` trên lý thuyết nghe rất hay (HAX G9 can thiệp sửa sai), nhưng khi đưa vào giao diện Discord Slash Command thì trở thành một "cơn ác mộng UX". Việc gõ lệnh sửa quá phức tạp khiến người dùng thà bỏ qua còn hơn sử dụng.

### 5.2. Phiên 2: Nguyễn Xuân Khuê (Willing User 2)
- **Thiết bị:** Discord Web Client trên Chrome (Windows).
- **Diễn biến thao tác:**
  - `00:00 - 00:50`: Gõ `/summary`, quét tin nhắn trong kênh thảo luận bài tập.
  - `00:50 - 02:10`: Đọc kỹ thẻ bài tập Lab 2. Thấy hiển thị tiêu đề *"Nộp bài tập Lab 2"*, hạn nộp để trống kèm nhãn vàng `Confidence: 0.70 ⚠️ (Mốc giờ/thông tin cần xác nhận lại)`.
  - `02:10 - 02:40`: Khuê bấm vào link `[Nguồn]`, nhảy đúng đến tin nhắn của TA Minh Hằng ghi *"Lab 2 nộp vào tối nay nhé"*.
  - `02:40 - 03:15`: Khuê gật đầu đồng tình và xác nhận việc bot để trống giờ nộp là hoàn toàn chính xác, vì nếu bot tự đoán 23:59 thì sinh viên sẽ chủ quan và nộp muộn.
- **Nhận định của nhóm:** Quyết định không bịa giờ và hiển thị nhãn cảnh báo ngôn ngữ tự nhiên đã phát huy tác dụng tối đa, tạo dựng niềm tin vững chắc cho học viên.

### 5.3. Phiên 3: Nguyễn Minh Lương
- **Thiết bị:** Discord Desktop Client trên Windows.
- **Diễn biến thao tác:**
  - `00:00 - 01:15`: Lương gõ thử cả hai lệnh `/summary` và `/tasks`.
  - `01:15 - 02:30`: Thấy `/summary` trả về Embed nhiều màu sắc có cả tin đổi phòng, còn `/tasks` chỉ trả về danh sách ngắn các việc cần làm. Lương thắc mắc tại sao không gộp làm một.
  - `02:30 - 03:30`: Sau khi nghe giải thích về việc `/tasks` chỉ để quản lý cá nhân và tích hợp reminder riêng, Lương hiểu ra nhưng đề xuất cần làm rõ câu chữ mô tả của lệnh ngay trên Discord.
- **Nhận định của nhóm:** Cần tinh chỉnh phần description của từng Slash Command trong `app.py` để định hình mental model rõ ràng ngay khi user gõ `/`.

### 5.4. Phiên 4: Nguyễn Duy Phong
- **Thiết bị:** Discord Mobile App trên iOS.
- **Diễn biến thao tác:**
  - `00:00 - 01:00`: Phong mở Discord trên điện thoại, gõ `/tasks` để xem bài tập cần hoàn thành.
  - `01:00 - 01:45`: Sau khi làm xong bài, Phong gõ `/done task_id: 12`. Bot phản hồi ephemeral: *"✅ Đã đánh dấu hoàn thành"*.
  - `01:45 - 02:30`: Phong chuyển sang kênh thông báo chung, cuộn lên bản tin `/summary` buổi sáng và thắc mắc sao thẻ bài tập số 12 vẫn còn màu đỏ mà không biến mất.
- **Nhận định của nhóm:** Đây là sự khác biệt giữa "Message History" và "Stateful Task". Nhóm giải thích rõ trong spec và hướng dẫn: `/summary` là ảnh chụp lịch sử thông tin 24h, không thể tự động xóa tin nhắn trong kênh chung của server.

### 5.5. Phiên 5: Nguyễn Quốc Việt
- **Thiết bị:** Discord Web Client trên Firefox.
- **Diễn biến thao tác:**
  - `00:00 - 01:00`: Gõ `/summary`, đọc lướt qua 4 thẻ công việc.
  - `01:00 - 02:15`: Việt nhìn thấy dòng `[Xem message gốc]` ở cuối mỗi thẻ và bấm thử cả 4 link, khiến trình duyệt nhảy liên tục giữa các kênh chat. Việt cảm thấy mệt mỏi và hỏi liệu có cần bấm kiểm tra hết không.
  - `02:15 - 03:00`: Nhóm giải thích rằng link nguồn chỉ là bằng chứng đối chiếu khi có nghi ngờ, bình thường chỉ cần đọc thẻ digest là đủ.
- **Nhận định của nhóm:** Cần giữ giao diện tối giản, xem link nguồn như một chiếc "phao cứu sinh" (safety net) thay vì khuyến khích người dùng click vào mọi lúc.

---

## 6. Đo lường hiệu quả cắt giảm thời gian (Time-on-Task Measurement)

Nhóm thực hiện bấm giờ so sánh thời gian học viên tự đọc lướt các kênh Discord thủ công vs. thời gian sử dụng Action Digest:

| Học viên thử nghiệm | Thời gian đọc Discord thủ công (Baseline CP1) | Thời gian đọc qua Action Digest (CP5) | Mức độ cắt giảm thời gian | Đạt mục tiêu (2–3 phút)? |
|---|:---:|:---:|:---:|:---:|
| **Lê Nguyễn Thái Dương** | 7 phút 30 giây | 2 phút 10 giây | Giảm **71.1%** | ✅ ĐẠT |
| **Nguyễn Xuân Khuê** | 8 phút 15 giây | 1 phút 50 giây | Giảm **77.8%** | ✅ ĐẠT |
| **Nguyễn Minh Lương** | 6 phút 45 giây | 2 phút 25 giây | Giảm **64.2%** | ✅ ĐẠT |
| **Nguyễn Duy Phong** | 9 phút 00 giây | 2 phút 15 giây | Giảm **75.0%** | ✅ ĐẠT |
| **Nguyễn Quốc Việt** | 7 phút 10 giây | 2 phút 40 giây | Giảm **62.8%** | ✅ ĐẠT |
| **TRUNG BÌNH** | **7 phút 44 giây** | **2 phút 16 giây** | **Giảm 70.7%** | ✅ **XUẤT SẮC** |

> **Kết luận chỉ số:** Thời gian nắm bắt thông tin trung bình giảm từ **~7.7 phút xuống còn ~2.3 phút** (cắt giảm hơn **70%** thời gian lội chat hàng ngày), hoàn thành xuất sắc mục tiêu cam kết tại Canvas CP1.

---

## 7. Đo lường mức độ hài lòng (CSAT) & Sean Ellis Metric

### 7.1. Điểm số hài lòng CSAT (Thang điểm 1 đến 5):
> *"Nếu bot Action Digest này được đưa vào sử dụng chính thức trong server lớp học, bạn sẵn sàng sử dụng nó ở mức độ nào?"*

| Học viên thử nghiệm | Điểm đánh giá (1–5) | Lý do chính |
|---|:---:|---|
| Lê Nguyễn Thái Dương | **4.5 / 5.0** | Tóm tắt nhanh và link nguồn chuẩn, nhưng trừ điểm vì lệnh sửa giờ quá rườm rà (ủng hộ việc bỏ lệnh sửa để bot tự chạy). |
| Nguyễn Xuân Khuê | **5.0 / 5.0** | Cực kỳ ưng ý tính năng bắt tin đổi phòng học và việc bot không tự tiện bịa giờ nộp bài. |
| Nguyễn Minh Lương | **4.5 / 5.0** | Đỡ phải lội hàng trăm tin nhắn tán gẫu rủ đi ăn trưa trong lớp. |
| Nguyễn Duy Phong | **4.5 / 5.0** | Bản tin Embed chia màu đỏ/cam/xanh rất dễ nhìn trên điện thoại. |
| Nguyễn Quốc Việt | **5.0 / 5.0** | Thích nhất việc chỉ cần gõ 1 lệnh là gom đủ tin của cả 3 kênh quan trọng. |
| **ĐIỂM TRUNG BÌNH CSAT** | **4.70 / 5.0** | **ĐẠT VƯỢT MỨC CAM KẾT ($\ge 4.5 / 5.0$)** |

### 7.2. Thước đo Sean Ellis Disappointment Metric (Đo lường Product-Market Fit):
> *"Nếu ngày mai bạn KHÔNG ĐƯỢC PHÉP sử dụng bot này nữa trong lớp học, bạn sẽ cảm thấy thế nào?"*

- **Rất tiếc (Very Disappointed):** **5 / 5 học viên (100.0%)**
- **Hơi tiếc (Somewhat Disappointed):** 0 / 5 học viên (0.0%)
- **Không sao cả (Not Disappointed):** 0 / 5 học viên (0.0%)

👉 **Kết luận:** Tỷ lệ **100% "Rất tiếc"** vượt xa ngưỡng chuẩn 40% của Sean Ellis, chứng minh bài toán "bỏ lỡ thông báo bài tập do trôi tin Discord" là một nỗi đau cực kỳ nhức nhối và sản phẩm đã giải quyết đúng trọng tâm nhu cầu thực tế của học viên.

---

## 8. Kết nối trực tiếp với Changelog §9 và Định hướng phát triển

Dựa trên toàn bộ dữ liệu quan sát hành vi thực tế và trích dẫn nguyên văn từ 5 phiên thử nghiệm, nhóm đã chính thức thực hiện và đóng băng 3 quyết định sản phẩm quan trọng tại **`## §9. Changelog`** của `spec.md`:

1. **Xóa bỏ hoàn toàn chức năng `/correct` (Quyết định từ User Thái Dương):**
   - *Nguyên nhân:* Người dùng cảm thấy việc gõ lệnh sửa quá rườm rà, tốn thời gian và không mang lại giá trị thực tế cao trong bối cảnh học viên đang bận rộn.
   - *Hành động:* Gỡ bỏ lệnh `/correct` khỏi danh mục lệnh để tinh gọn giao diện, tập trung toàn bộ tài nguyên vào việc tối ưu thuật toán AI trích xuất chuẩn xác ngay từ đầu và gửi DM nhắc hẹn.
2. **Làm rõ ranh giới `/summary`, `/tasks` và định vị link `Nguồn` là Safety Net (Quyết định từ User Minh Lương & Quốc Việt):**
   - *Nguyên nhân:* Người dùng bị nhầm lẫn giữa bản tin kênh và danh sách cá nhân, đồng thời bị áp lực phải click vào tất cả các link nguồn.
   - *Hành động:* Định hình rõ trong mô tả: `/summary` dùng đọc lướt 24h, `/tasks` dùng quản lý việc chưa làm, `/done` để đóng task; link nguồn chỉ đóng vai trò bảo chứng an toàn khi có nghi ngờ chứ không bắt buộc mở.
3. **Kiên quyết giữ cơ chế cảnh báo cho thông tin mơ hồ (Quyết định từ User Xuân Khuê):**
   - *Nguyên nhân:* Người dùng khẳng định việc AI tự ý gán giờ `23:59` là cực kỳ nguy hiểm.
   - *Hành động:* Giữ vững nguyên tắc Zero Hallucination: khi tin nhắn không có giờ cụ thể, bắt buộc gán `deadline_iso: null` và hiển thị cảnh báo `Confidence: 0.70 ⚠️ (Mốc giờ/thông tin cần xác nhận lại)`.

Toàn bộ quá trình kiểm thử này đã chứng minh rằng: **Lắng nghe hành vi thực tế của người dùng và dám dũng cảm cắt bỏ tính năng rườm rà (`/correct`) có giá trị thực tiễn cao hơn việc cố níu giữ một tính năng phức tạp trên giấy tờ.**