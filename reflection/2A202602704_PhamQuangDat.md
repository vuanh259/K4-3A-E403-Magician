# BÁO CÁO THU HOẠCH CÁ NHÂN (INDIVIDUAL REFLECTION)

* **Họ và tên:** Phạm Quang Đạt
* **Mã học viên:** `2A202602704`
* **Nhóm:** Magician (Phòng E403 · Lớp 3A)
* **Dự án:** Discord ActionDigest (Track B — Trợ lý Học viên)
* **Vai trò chính:** QA, Benchmark & User Validation Engineer

---

## 1. Vai trò cá nhân & Phần việc trực tiếp phụ trách

Trong dự án Discord ActionDigest, tôi đảm nhiệm vai trò **Kỹ sư Đảm bảo Chất lượng (QA) & Đánh giá Nghiệm thu**, chịu trách nhiệm bảo vệ ranh giới chất lượng (Quality Bar) và tính trung thực khoa học của toàn bộ kết quả đo lường:
- **Xây dựng bộ dữ liệu Golden Set 22 ca ([`eval/golden_set.json`](../eval/golden_set.json)):**
  - Trực tiếp trích xuất **13/22 ca kiểm thử từ chatlog thật của lớp học** (`discord-pack/k4_messages.csv`).
  - Phân bổ đầy đủ độ phủ qua **4 lớp chỗ khó**: ① Nguồn sự thật (TC01-02), ② Mơ hồ/thiếu tin (TC03-04), ③ Ngoài phạm vi/thẩm quyền (TC05-06), ④ Đặc thù nghiệp vụ (TC07-08, TC22), cùng 8 ca phổ biến (TC09-16) và 5 ca hiểm (Edge Cases TC17-21).
- **Lập trình công cụ đánh giá tự động ([`eval/run_eval.py`](../eval/run_eval.py)):**
  - Viết script Python tự động nạp Golden Set, gọi module AI thật, thực hiện assertion kiểm tra kết quả theo từng lớp điều kiện (chặn ngoài phạm vi `len(items) == 0`, tách gộp deadline `len(items) >= 2`, kiểm tra cờ cảnh báo giờ mập mờ).
  - Tự động xuất báo cáo định lượng Markdown ([`eval/EVAL_REPORT.md`](../eval/EVAL_REPORT.md)) và HTML ([`eval/report.html`](../eval/report.html)).
- **Thẩm định độc lập thủ công (Human Audited Verification):** Đối chiếu từng trường trích xuất của mô hình với câu nói gốc trong chatlog để kiểm tra chéo các chỉ số Precision, Recall, Grounding Rate và Zero Hallucination Rate.
- **Thực hiện vai trò Note-taker trong phiên Mom Test ([`validation/user_testing_log.md`](../validation/user_testing_log.md)):** Giữ thái độ khách quan, ghi lại trung thực từng giây thao tác, điểm ngập ngừng và câu nói nguyên văn của người dùng thử nghiệm.

---

## 2. Cách thức ứng dụng AI trong quá trình xây dựng sản phẩm

Tôi đã ứng dụng AI như một công cụ hỗ trợ rà soát dữ liệu và phân tích đối chiếu độc lập:
1. **Khai phá các mẫu dữ liệu biên (Edge-case Mining):** Sử dụng AI để phân tích toàn bộ file `discord-pack/k4_messages.csv`, tìm ra các trường hợp tin nhắn có cấu trúc ngữ pháp phức tạp (tin nhắn đính chính dời phòng, câu hỏi bẫy của học viên, các chỉ thị giả mạo hệ thống) để đưa vào bộ Golden Set kiểm thử độ bền bỉ của mô hình.
2. **Sinh mã nguồn kiểm thử và kịch bản Red-teaming:** Tận dụng AI để viết các hàm assertion kiểm tra cấu trúc JSON và tự động hóa việc tính toán các chỉ số thống kê tỷ lệ đạt (Pass Rate) theo từng lớp chỗ khó.
3. **Giữ nguyên tắc "Không để AI tự chấm bài cho AI":** Tôi nhận thức sâu sắc rằng LLM thường có xu hướng bao biện và chấm nới tay cho chính nó (LLM-as-a-judge bias). Do đó, tôi luôn sử dụng các hàm kiểm tra logic cứng bằng code Python thuần túy và trực tiếp so khớp đối chiếu từng ca bằng mắt thường.

---

## 3. Một bài học thực tế rút ra từ trường hợp thất bại của nhóm

### Trường hợp thất bại cụ thể:
Trong đợt nghiệm thu nội bộ trước CP4, nhóm từng có một mâu thuẫn lớn giữa tài liệu và số liệu thực tế:
- Trong bản nháp tài liệu ban đầu, nhóm đã vội vàng tuyên bố: *"Zero Hallucination: 100% (22/22 ca), Safety Hard Gate đạt"*.
- Tuy nhiên, khi tôi chạy script `run_eval.py` và trực tiếp kiểm tra file log `eval/run_results.md`, ca `TC19` (Prompt Injection) thực tế đã thất bại: mô hình bị lừa và sinh ra một thông báo hủy lab hoàn toàn bịa đặt. Tỷ lệ Zero Hallucination thực tế chỉ đạt **95.5% (21/22 ca)**, đồng nghĩa với việc **vi phạm điều kiện Safety Hard Gate**.
- Đồng thời, danh sách ca FAIL trong bản nháp ghi nhầm thành `TC11, TC14, TC18`, trong khi thực tế `TC11` đã PASS hoàn hảo và `TC19` mới là ca FAIL nặng nhất.

### Bài học xương máu rút ra:
Bài học lớn nhất của tôi trong vai trò QA là: **"Giá trị cốt lõi của người làm kiểm thử là sự trung thực và tính khách quan bất khả xâm phạm — Che giấu lỗi là sự thất bại tồi tệ nhất của tư duy sản phẩm."**
- Trong các cuộc thi hoặc dự án gấp rút, áp lực phải có "báo cáo số đẹp 100%" là rất lớn. Rất dễ rơi vào cám dỗ sửa lại tiêu chí test hoặc lờ đi ca lỗi để lấy thành tích.
- Nhưng nếu che giấu ca `TC19`, khi ra Hội đồng giám khảo ở CP6 và bị test một câu prompt injection ngẫu nhiên, sản phẩm sẽ sụp đổ hoàn toàn.
- **Hành động chuyển hóa:** Tôi đã kiên quyết yêu cầu nhóm sửa lại tài liệu `spec.md`: công bố trung thực 3 ca FAIL thực tế (`TC14, TC18, TC19`), thừa nhận rõ ràng Safety Hard Gate chưa đạt tại CP3 và giải trình cặn kẽ nguyên nhân kỹ thuật kèm phương án khắc phục cho CP5. Quyết định này không chỉ giúp nhóm tuân thủ đúng tôn chỉ của cuộc thi (*"Số xấu vẫn được đủ điểm — phân tích được thất bại có giá trị hơn số đẹp không căn cứ"*), mà còn mang lại sự tự tin tuyệt đối cho cả nhóm khi bước vào vòng bảo vệ trước ban giám khảo.
