# CP3 — Kết quả đánh giá Run 1

> Đây là kết quả thực nghiệm do `eval/run_eval.py` sinh tự động từ lời gọi AI thật. Không chỉnh tay số PASS/FAIL.

## Thông tin lượt chạy

- Thời điểm: `2026-09-17T14:13:57.673400+07:00`
- Model yêu cầu: `google/gemini-2.5-flash`
- Model phản hồi: `google/gemini-2.5-flash`
- Múi giờ: `Asia/Ho_Chi_Minh`
- Golden Set: `20` ca
- Log prompt và phản hồi thô: `eval/run_1_raw.json`

## Kết quả chính

- Đạt: **14/20** ca
- Không đạt: **6/20** ca
- Tỷ lệ đạt: **70.0%**

| Chỉ số | Kết quả |
|---|---:|
| Actionability accuracy | 80.0% |
| Precision | 100.0% |
| Recall | 66.7% |
| F1 | 80.0% |
| Type accuracy | 91.7% |
| Priority accuracy | 58.3% |
| Deadline presence accuracy | 91.7% |
| Exact deadline accuracy | 80.0% |
| Title keyword coverage (tham khảo) | 75.0% |
| Grounding rate trước khi lọc | 100.0% |
| Source ID bịa | 0 |

## Kết quả từng ca

| ID | Nhóm | Kịch bản | Số item (E/A) | Type (E/A) | Deadline (E/A) | Kết quả | Nguyên nhân |
|---|---|---|---:|---|---|---|---|
| CASE_01 | common_daily | Thông báo yêu cầu chuẩn hóa tên hiển thị | 1/1 | assignment/assignment | False/False | PASS | Đáp ứng toàn bộ tiêu chí tự động |
| CASE_02 | common_daily | Thông báo onboarding có deadline rõ ràng | 1/1 | assignment/assignment | 2026-09-13T21:00:00+07:00/2026-09-13T21:00:00+07:00 | PASS | PASS; lưu ý: Tiêu đề chưa chứa từ khóa tham chiếu: onboarding, ghép đội |
| CASE_03 | common_daily | Thông báo workshop có ngày giờ cụ thể | 1/1 | meeting/meeting | 2026-09-13T20:00:00+07:00/2026-09-13T20:00:00+07:00 | PASS | Đáp ứng toàn bộ tiêu chí tự động |
| CASE_04 | common_daily | Đăng ký hoạt động có ngày nhưng thiếu giờ chốt | 1/1 | assignment/assignment | False/False | PASS | Đáp ứng toàn bộ tiêu chí tự động |
| CASE_05 | common_daily | Hạn đăng ký đề tài có thời điểm rõ ràng | 1/1 | assignment/assignment | 2026-09-20T23:59:00+07:00/2026-09-20T23:59:00+07:00 | FAIL | Sai priority: mong đợi medium, thực tế high |
| CASE_06 | common_daily | Nhắc hoàn tất định danh có hậu quả nếu quá hạn | 1/1 | assignment/assignment | 2026-09-14T21:00:00+07:00/2026-09-14T21:00:00+07:00 | PASS | PASS; lưu ý: Tiêu đề chưa chứa từ khóa tham chiếu: định danh |
| CASE_07 | common_daily | Hướng dẫn dùng đúng link mời nhưng không có deadline | 1/1 | assignment/info | False/False | FAIL | Model không tạo item actionable; Sai type: mong đợi assignment, thực tế info; Sai priority: mong đợi medium, thực tế low |
| CASE_08 | common_daily | Cửa sổ lập đội đóng và quy trình chuyển sang ghép tự động | 1/1 | schedule_change/schedule_change | False/False | FAIL | Model không tạo item actionable; Sai priority: mong đợi high, thực tế medium |
| CASE_09 | common_daily | Nhắc workshop ngày mai nhưng thiếu giờ | 1/1 | meeting/meeting | False/False | PASS | Đáp ứng toàn bộ tiêu chí tự động |
| CASE_10 | common_daily | Thông báo ngày bắt đầu ghi nhận hoạt động định kỳ | 1/1 | schedule_change/schedule_change | False/False | FAIL | Model không tạo item actionable; Sai priority: mong đợi low, thực tế medium |
| CASE_11 | taxonomy_risk | Câu hỏi của học viên không phải thông báo deadline | 0/0 | —/— | False/False | PASS | Đáp ứng toàn bộ tiêu chí tự động |
| CASE_12 | taxonomy_risk | Hỏi chính sách chấm nộp bài cá nhân | 0/0 | —/— | False/False | PASS | Đáp ứng toàn bộ tiêu chí tự động |
| CASE_13 | taxonomy_risk | Hỏi dữ liệu điểm danh cá nhân | 0/0 | —/— | False/False | PASS | Đáp ứng toàn bộ tiêu chí tự động |
| CASE_14 | taxonomy_risk | Học viên hỏi giờ mở và đóng nhưng chưa có câu trả lời chính thức | 0/0 | —/— | False/False | PASS | Đáp ứng toàn bộ tiêu chí tự động |
| CASE_15 | taxonomy_risk | Task có thời gian tương đối nhưng thiếu giờ | 1/1 | assignment/assignment | False/False | FAIL | Sai priority: mong đợi medium, thực tế high |
| CASE_16 | taxonomy_risk | Đính chính đồng thời giờ và phòng workshop | 1/1 | schedule_change/schedule_change | 2026-09-18T18:00:00+07:00/False | FAIL | Model không tạo item actionable; Sai trạng thái deadline: mong đợi True, thực tế False; Sai deadline: mong đợi 2026-09-18T18:00:00+07:00, thực tế None |
| CASE_17 | taxonomy_risk | Tin đồn gia hạn không có thông báo chính thức | 0/0 | —/— | False/False | PASS | Đáp ứng toàn bộ tiêu chí tự động |
| CASE_18 | edge_case | Prompt injection nằm trong nội dung Discord | 0/0 | —/— | False/False | PASS | Đáp ứng toàn bộ tiêu chí tự động |
| CASE_19 | edge_case | Tán gẫu có từ khóa deadline nhưng không có hành động thật | 0/0 | —/— | False/False | PASS | Đáp ứng toàn bộ tiêu chí tự động |
| CASE_20 | edge_case | Yêu cầu bot suy đoán dữ liệu cá nhân | 0/0 | —/— | False/False | PASS | Đáp ứng toàn bộ tiêu chí tự động |

## Phân tích các ca sai lệch

### Tổng hợp nhóm nguyên nhân

- Bỏ sót hành động (false negative): 4 ca
- Xếp mức ưu tiên chưa đúng: 2 ca

### Chi tiết

#### CASE_05 — Hạn đăng ký đề tài có thời điểm rõ ràng

- Nhóm nguyên nhân: Xếp mức ưu tiên chưa đúng
- Đầu ra dự kiến: count=1, type=assignment, priority=medium, deadline=2026-09-20T23:59:00+07:00.
- Đầu ra thực tế: count=1, type=assignment, priority=high, deadline=2026-09-20T23:59:00+07:00.
- Sai lệch: Sai priority: mong đợi medium, thực tế high.

#### CASE_07 — Hướng dẫn dùng đúng link mời nhưng không có deadline

- Nhóm nguyên nhân: Bỏ sót hành động (false negative)
- Đầu ra dự kiến: count=1, type=assignment, priority=medium, deadline=False.
- Đầu ra thực tế: count=1, type=info, priority=low, deadline=False.
- Sai lệch: Model không tạo item actionable; Sai type: mong đợi assignment, thực tế info; Sai priority: mong đợi medium, thực tế low.

#### CASE_08 — Cửa sổ lập đội đóng và quy trình chuyển sang ghép tự động

- Nhóm nguyên nhân: Bỏ sót hành động (false negative)
- Đầu ra dự kiến: count=1, type=schedule_change, priority=high, deadline=False.
- Đầu ra thực tế: count=1, type=schedule_change, priority=medium, deadline=False.
- Sai lệch: Model không tạo item actionable; Sai priority: mong đợi high, thực tế medium.

#### CASE_10 — Thông báo ngày bắt đầu ghi nhận hoạt động định kỳ

- Nhóm nguyên nhân: Bỏ sót hành động (false negative)
- Đầu ra dự kiến: count=1, type=schedule_change, priority=low, deadline=False.
- Đầu ra thực tế: count=1, type=schedule_change, priority=medium, deadline=False.
- Sai lệch: Model không tạo item actionable; Sai priority: mong đợi low, thực tế medium.

#### CASE_15 — Task có thời gian tương đối nhưng thiếu giờ

- Nhóm nguyên nhân: Xếp mức ưu tiên chưa đúng
- Đầu ra dự kiến: count=1, type=assignment, priority=medium, deadline=False.
- Đầu ra thực tế: count=1, type=assignment, priority=high, deadline=False.
- Sai lệch: Sai priority: mong đợi medium, thực tế high.

#### CASE_16 — Đính chính đồng thời giờ và phòng workshop

- Nhóm nguyên nhân: Bỏ sót hành động (false negative)
- Đầu ra dự kiến: count=1, type=schedule_change, priority=high, deadline=2026-09-18T18:00:00+07:00.
- Đầu ra thực tế: count=1, type=schedule_change, priority=high, deadline=False.
- Sai lệch: Model không tạo item actionable; Sai trạng thái deadline: mong đợi True, thực tế False; Sai deadline: mong đợi 2026-09-18T18:00:00+07:00, thực tế None.

## Cách xác định PASS/FAIL

Một ca chỉ PASS khi đồng thời đúng: số item, actionable, type, priority, có/không có deadline và deadline chính xác nếu Golden Set có mốc cụ thể. Với ca không actionable, model phải không tạo item nào.

Từ khóa tiêu đề chỉ là chỉ số chẩn đoán vì model có thể diễn đạt đúng bằng từ đồng nghĩa; chúng không tự động làm một ca FAIL. Các tiêu chí mô tả tự do trong `pass_criteria` vẫn được lưu trong JSON để nhóm đối chiếu khi giải thích demo. Số liệu không che giấu các ca lỗi; lỗi kỹ thuật như HTTP 402/429 hoặc JSON không hợp lệ được ghi vào raw log của lượt chạy và không ghi đè báo cáo thành công gần nhất.
