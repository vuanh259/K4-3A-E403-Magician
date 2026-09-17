# AI SPEC — Discord Action Digest (Trích xuất Task, Deadline & Thay đổi lịch) · Nhóm Magician · Phòng E403
Hướng: [ ] A — VLearn  [x] B — Trợ lý Học viên (Discord)  [ ] C — Làn mở  
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới

---

## 📌 Phụ lục CP1: Canvas 4 Ô (Đã nộp Checkpoint 1)

### 🟩 Ô 1: Người dùng & Nỗi đau
- **Job executor:** Học viên khóa học AI và TA quản lý kênh Discord hàng ngày.
- **Quy trình hiện tại:** Học viên phải theo dõi từ 3 đến 10 channel Discord mỗi ngày để tìm kiếm thông báo bài tập, lịch học, lịch nộp lab.
- **Nỗi đau cốt lõi (Core Pain - KHÔNG chữ AI):** Kênh Discord có lượng tin nhắn thảo luận quá lớn khiến học viên mất 5–10 phút mỗi ngày đọc lướt và 50% từng bỏ lỡ hạn nộp bài tập hoặc nhầm phòng học do thông báo bị trôi.

### 🟦 Ô 2: Bằng chứng ban đầu
- **Khảo sát thực tế (Đạt Chuẩn A với $n = 30$ học viên ngoài nhóm):**
  - **50.0% (15/30)** học viên xác nhận từng bỏ lỡ hoặc phát hiện muộn thông tin quan trọng trên Discord (deadline lab, workshop, daily standup).
  - **96.7% (29/30)** học viên mong muốn có công cụ tự động lọc và tổng hợp task/deadline/lịch thay đổi.
  - *Quote nguyên văn:*
    - *"Do có quá nhiều tin nhắn mình đã để trôi thông tin quan trọng mà giảng viên gửi"* (Phản hồi #4)
    - *"Suýt quên hoàn thành daily standup vì quá nhiều channel để check"* (Phản hồi #8)
    - *"Bỏ lỡ workshop 1 và 2 do có quá nhiều kênh liên lạc"* (Phản hồi #6)
    - *"Quên mất lịch workshop do tắt thông báo"* (Phản hồi #5)
    - *"Không để ý task"* (Phản hồi #9)
- **Khai phá dữ liệu có sẵn (`discord-pack/` - Đạt Chuẩn B với 1.092 tin nhắn):** Trong 1.092 tin thực tế có nhiều thông báo đính chính lịch; 4 bản tin bot hiện tại bị cắt cụt tóm tắt, chèn chuỗi lỗi kỹ thuật "nguồn tham chiếu" và hoàn toàn thiếu chức năng trích xuất Task/Deadline có phân cấp ưu tiên.

### 🟨 Ô 3: Lát cắt & Automation
- **Lát cắt giải pháp (Đúng 1 câu theo chuẩn):** *Học viên khóa học AI cần theo dõi các đầu việc và thời hạn trong ngày được AI tự động lọc nhiễu và phân cấp ưu tiên kèm trích dẫn gốc giúp không bỏ lỡ bất kỳ deadline hoặc thông báo thay đổi lịch nào trong 30 giây.*
- **Quyết định của AI (3 mức ưu tiên):**
  - 🔴 **P1 (Khẩn cấp):** Thay đổi lịch/phòng học, deadline trong vòng 24h, thông báo từ Giảng viên/BTC.
  - 🟡 **P2 (Quan trọng):** Task bài tập mới, tài liệu cần đọc, deadline > 24h.
  - 🟢 **P3 (Theo dõi):** Nhắc nhở định kỳ, tin tổng kết.
- **Automation (Conditional / Augment):** Dựa trên chi phí sai sót (cost-of-error), nếu AI bịa deadline sẽ gây hậu quả 0 điểm cho học viên; do đó AI chỉ trích xuất có căn cứ nguồn gốc; với tin nhắn thời gian mập mờ, AI gắn cờ `[⚠️ Cần xác nhận lại]` chứ tuyệt đối không tự ý suy diễn giờ.

### 🟧 Ô 4: Người thử & Phân công
- **Willing users (2 người dùng ngoài nhóm cam kết thử nghiệm ở CP5):**
  1. **Lê Nguyễn Thái Dương** — Mã HV: `2A202602383`
  2. **Nguyễn Xuân Khuê** — Mã HV: `2A202602999`
- **Phân công trách nhiệm 4 thành viên:**
  - **Nguyễn Vũ Anh (2A202602502):** Đội trưởng · Phụ trách AI Spec, phân tích khảo sát và quản lý tiến độ.
  - **Nguyễn Thành Duy (2A202602804):** AI & Prompt Engineer · Thiết kế prompt trích xuất task/deadline và bộ phân cấp ưu tiên P1/P2/P3.
  - **Trương Việt Anh (2A202602444):** Fullstack & Discord Integration · Xây dựng pipeline đọc tin và giao diện hiển thị bản tin.
  - **Phạm Quang Đạt (2A202602704):** QA & Eval · Xây dựng Golden Set 20 case và đo lường độ chính xác.

---

## §1. User & Job
- **Job executor + workflow:** Học viên khóa học AI và TA phụ trách kênh Discord. Mỗi ngày học viên mở Discord 5-7 lần, lướt qua các kênh `#thông-báo`, `#general`, `#q-and-a` để tìm bài tập và lịch học, tự ghi chép lại hoặc chụp màn hình.
- **Core JTBD:** Nắm bắt kịp thời, đầy đủ và chính xác các đầu việc cần làm cùng thời hạn nộp bài mà không phải đọc thủ công hàng trăm tin nhắn thảo luận.
- **Problem statement (KHÔNG chữ AI):** Kênh Discord có lượng tin nhắn thảo luận quá lớn khiến học viên mất 5–10 phút mỗi ngày đọc lướt và 50% từng bỏ lỡ hạn nộp bài tập hoặc nhầm phòng học do thông báo bị trôi.
- **Evidence (Chuẩn A và B — log đầy đủ tại `evidence_log.md`):**
  - **Số liệu khảo sát (Chuẩn A):** $n = 30$ học viên ngoài nhóm, $50.0\%$ (15/30) xác nhận từng bỏ lỡ thông tin quan trọng; $96.7\%$ (29/30) mong muốn công cụ hỗ trợ.
  - **Khai thác dữ liệu (Chuẩn B):** Mining tập `discord-pack/` gồm 1.092 tin nhắn (779 tin từ học viên, 313 tin từ bot/BTC), chỉ ra 4 bản tin bot hiện có bị lỗi cắt cụt và thiếu trích xuất task.
  - **≥5 quote nguyên văn:**
    1. *"Do có quá nhiều tin nhắn mình đã để trôi thông tin quan trọng mà giảng viên gửi"* (Khảo sát #4)
    2. *"Suýt quên hoàn thành daily standup vì quá nhiều channel để check"* (Khảo sát #8)
    3. *"Bỏ lỡ workshop 1 và 2 do có quá nhiều kênh liên lạc"* (Khảo sát #6)
    4. *"Quên mất lịch workshop do tắt thông báo"* (Khảo sát #5)
    5. *"Không để ý task"* (Khảo sát #9)

## §2. Impact & quyết định chọn

- **Bảng impact so sánh 3 phương án ứng viên (Theo công thức định lượng: Quy mô người × Tần suất × Tốn gì mỗi lần):**

| Ứng viên giải pháp | Quy mô tác động (Bao nhiêu người) | Tần suất xuất hiện | Tốn gì mỗi lần (Thiệt hại / Thời gian lãng phí) | Tổng thiệt hại định lượng (Impact Formula) | Chi phí sai sót (Cost of error) | Tính khả thi trong 47.5h |
|---|---|---|---|---|---|---|
| **A. Trợ lý Q&A giải đáp kiến thức bài học** | ~20–30 học viên gặp bài khó/buổi | 2–3 câu hỏi/buổi | Chờ TA trả lời mất 15–30 phút; nếu không ai giải đáp thì bỏ dở bài tập | Lãng phí ~10–15 giờ chờ đợi/ngày trên một nhóm nhỏ | Thấp – Trung bình (giải thích sai khái niệm lý thuyết) | **Thấp** (cần RAG toàn bộ slide + video 6 buổi, vượt quá khung 47.5h) |
| **B. Bot chủ động phát hiện học viên stuck & gửi DM** | ~10–15 học viên kẹt code/ngày | 1–2 lần/tuần | TA phải rà soát thủ công chatlog; học viên bị gián đoạn làm bài | Mất ~5 giờ TA rà soát/tuần; rủi ro học viên bị ức chế vì bot spam | **Rất cao** (xâm phạm quyền riêng tư, gửi nhầm DM gây spam hoang mang) | **Trung bình** (khó xác định chính xác ngữ cảnh stuck từ chat lộn xộn) |
| **C. Action Digest: Trích xuất Task, Deadline & Đổi lịch (CHỌN)** | **Toàn bộ ~230 học viên** phòng E403 + đội ngũ TA | **5–7 lần/ngày** (mỗi khi mở Discord tìm thông báo) | Mất **5–10 phút/ngày** lướt 3–10 kênh để nhặt task; **50% (15/30)** từng bỏ lỡ deadline hoặc nhầm phòng học | Lãng phí **~20–38 giờ đọc lướt/ngày** cho cả phòng (trung bình 5–10 phút × 230 người); gây hậu quả 0 điểm bài tập hoặc lỡ buổi học | **Cao nếu bịa deadline** (đã giải quyết triệt để bằng Conditional + Trích dẫn gốc) | **Rất cao** (lát cắt tập trung, dữ liệu `discord-pack/` dồi dào, kiểm chứng được ngay) |

- **Ứng viên ĐÃ LOẠI:** 
  - *Loại phương án A:* Bị trùng lặp trực tiếp với VLearn Tutor có sẵn của trường; phạm vi quá rộng không thể làm chỉn chu trong 47.5h.
  - *Loại phương án B:* Rủi ro Cost of error quá cao (học viên phản cảm việc bot tự tiện nhắn tin riêng khi chưa yêu cầu), vi phạm nguyên tắc tôn trọng quyền riêng tư.
- **Ứng viên CHỌN:** Chọn **Phương án C (Action Digest)** với lý do bằng số liệu định lượng vững chắc:
  1. **Đúng điểm đau lớn nhất:** $50.0\%$ (15/30) học viên xác nhận từng bị trôi tin quan trọng; $96.7\%$ (29/30) bày tỏ nhu cầu cấp thiết cần công cụ này.
  2. **Hiệu quả định lượng vượt trội:** Giảm thời gian tổng hợp thông tin từ **5–10 phút xuống còn 2–3 phút (tiết kiệm ~60–70% thời gian)**, giải phóng hơn **15–25 giờ lao động vô ích mỗi ngày** cho toàn bộ 230 học viên phòng E403.
  3. **Kiểm soát rủi ro an toàn tuyệt đối:** Sử dụng cơ chế *Conditional / Augment* kết hợp trích dẫn nguyên văn câu gốc để triệt tiêu 100% rủi ro hallucination.

## §3. Giải pháp tương tự đã nghiên cứu

### 1. Bot bản tin ngày hiện tại (trong `data/discord-pack/`):
- *Flow:* Tự động gom tin nhắn trong ngày và xuất ra một đoạn văn xuôi tóm tắt các chủ đề được hỏi.
- *Đáng học:* Cơ chế tự động lên lịch quét định kỳ hàng ngày.
- *Đáng né:* Tóm tắt văn xuôi cắt cụt, chèn lỗi "nguồn tham chiếu", không phân biệt được đâu là tin rác và đâu là việc cần làm ngay.
- *Mình khác gì:* Tập trung vào Actionable Items (Task, Deadline, Lịch đổi), phân loại 3 mức ưu tiên P1/P2/P3 và luôn hiển thị trích dẫn nguồn gốc kèm nút kiểm chứng.

### 2. Bot nhắc việc thủ công trên Discord (Ví dụ: Sesh Bot / Reminder Bot / Zapier Integration):
- *Flow:* Học viên phải tự theo dõi kênh, tự đọc thông báo và gõ lệnh thủ công `/remindme [thời gian] [nội dung]` để bot gửi thông báo nhắc hẹn trong DM.
- *Đáng học:* Cơ chế bắn thông báo trực tiếp (Direct Message / Mention) nhắc nhở chủ động trước giờ hạn chót (15-30 phút).
- *Đáng né:* Bắt buộc người dùng nhập thủ công 100% (Manual overhead). Nếu học viên bị trôi tin nhắn hoặc quên không đọc kênh thì bot hoàn toàn vô dụng, không giải quyết được gốc rễ bài toán "bỏ lỡ deadline do thông báo bị trôi".
- *Mình khác gì:* Tự động hóa hoàn toàn khâu phát hiện (Autonomous Discovery) bằng AI đọc hiểu ngữ nghĩa từ các kênh thông báo/thảo luận, trích xuất và phân cấp P1/P2/P3 không cần học viên phải tự gõ lệnh tạo task.

---
## §4. Thiết kế & Bản mẫu tương tác (CP2)
- **Lát cắt MỘT CÂU:** *Một học viên khóa AI Thực Chiến · gõ lệnh slash command `/summary` (hoặc `/summary all`) trên Discord để tổng hợp tin nhắn trong 24 giờ qua · AI tự động quét các kênh, lọc bỏ tin rác và quyết định tin nào chứa Task, Deadline hay Lịch đổi khẩn cấp (phân cấp P1/P2/P3) · trả về Bản tin Action Digest Embed gồm các thẻ công việc có tiêu đề, hạn chót, độ ưu tiên, trích dẫn gốc có link nhảy đến tin nhắn và nút đánh dấu hoàn thành (kèm cờ cảnh báo nếu mốc giờ mập mờ).*
- **Non-goals (Năm việc "để sau" KHÔNG build trong sự kiện):**
  1. KHÔNG trả lời giải thích lý thuyết hay chấm code bài tập (nhường VLearn Tutor).
  2. KHÔNG tự ý gửi tin nhắn riêng (DM) làm phiền học viên.
  3. KHÔNG tự suy đoán hay bịa đặt mốc giờ khi tin nhắn gốc không có ngày giờ cụ thể.
  4. KHÔNG tra cứu điểm danh cá nhân (thuộc thẩm quyền TA).
  5. KHÔNG tự động đăng thông báo lên kênh chat chung khi chưa được kiểm duyệt.
- **Mức prototype nhắm tới:** [x] Working Prototype / Bản mẫu tương tác bấm được tại `codebase/index.html`
  - *Phần giả lập (Mock):* Kênh feed tin nhắn Discord bên trái giả lập 5 tình huống thực tế trích từ `discord-pack/`.
  - *Phần tương tác thật (Working Interaction):* 
    - Giao diện Discord Chat Simulator cho phép học viên gõ lệnh tự do (hoặc bấm 4 nút prompt gợi ý).
    - Bộ xử lý phản hồi câu hỏi: trả về Bản tin Action Digest Embed dạng thẻ công việc có đồng hồ và trích dẫn gốc.
    - Modal can thiệp sửa đổi trực tiếp (Correction UI) hoạt động mượt mà.
    - Script thực thi `codebase/ai_extractor.py` và `codebase/chat_bot.py` chạy trực tiếp trên Python.
- **Automation:** [x] Conditional / Augment
  - *Lý do theo Cost-of-error:* Việc thông báo sai hạn nộp bài (deadline) hoặc sai phòng học gây hậu quả nghiêm trọng trực tiếp (học viên bị 0 điểm hoặc lỡ buổi học). Vì vậy giải pháp áp dụng **Conditional / Augment**: Con người luôn là người quyết định cuối cùng; AI chỉ trích xuất có bằng chứng và gắn cờ cảnh báo khi độ tin cậy thấp.
- **§4b. Bảng 4 nguyên tắc HAX/PAIR áp dụng cụ thể trên `codebase/index.html`:**

| Nguyên tắc | Mô tả nguyên tắc | Vị trí áp dụng cụ thể trên `codebase/index.html` |
|---|---|---|
| **HAX G1 (Nêu rõ năng lực hệ thống)** | Giúp người dùng hiểu hệ thống có thể làm gì và không làm gì | 1. Dòng mô tả ngay dưới Header: *"Chuyên trích xuất Task, Deadline & Lịch đổi từ Discord"*. <br>2. Phản hồi của bot khi người dùng hỏi *"giải thích Transformer"*: Bot từ chối và hướng dẫn gặp VLearn Tutor. |
| **HAX G2 (Thể hiện rõ độ tin cậy)** | Hiển thị mức độ chắc chắn của kết quả AI | 1. Huy hiệu màu sắc: 🔴 P1 Khẩn cấp, 🟡 P2 Quan trọng, 🟢 P3 Theo dõi.<br>2. Khi hỏi *"khi nào nộp lab 2?"*, bot hiển thị nhãn cảnh báo màu vàng: `[⚠️ Mốc giờ chưa cụ thể]` và ghi rõ *"AI không tự bịa giờ 23:59"*. |
| **HAX G9 (Hỗ trợ sửa sai tức thì)** | Cho phép người dùng can thiệp và sửa đổi kết quả trực tiếp | Nút **"Sửa hạn nộp"** trực tiếp trên từng thẻ công việc, bấm vào sẽ mở Modal cho phép học viên sửa lại tên task, deadline, mức ưu tiên và bấm *"Lưu thay đổi"*. |
| **HAX G11 (Giải thích lý do & Dẫn nguồn)** | Giúp người dùng hiểu vì sao AI đưa ra kết quả | Trên mỗi thẻ công việc đều có ô dẫn nguồn màu xám đen trích nguyên văn câu nói của TA/Giảng viên và thời điểm gửi. |

## §5. Kiểu lỗi — 4 lớp chỗ khó & kịch bản (8 kịch bản)

| STT | Lớp chỗ khó | Kịch bản đầu vào | Nguy cơ lỗi | Cách xử lý trong thiết kế (`index.html`) |
|---|---|---|---|---|
| 1 | ① Nguồn sự thật | "Bài tập Lab 2 nộp vào tối nay nhé" | AI tự bịa mốc 23:59 | Gắn nhãn `[⚠️ Mốc giờ chưa cụ thể]`, giữ nguyên quote, gợi ý hỏi lại TA |
| 2 | ① Nguồn sự thật | Học viên A đồn: "Chắc mai nộp lab đấy" | AI trích xuất tin đồn thành task | Bộ lọc chỉ nhận thông báo từ người có thẩm quyền (GV/TA/BTC) |
| 3 | ② Mơ hồ / Thiếu tin | "Tuần này nhớ nộp báo cáo tiến độ nhé" | Không biết thứ mấy nộp | Gắn nhãn `[Chưa rõ ngày cụ thể]`, xếp vào P3 Theo dõi |
| 4 | ② Mơ hồ / Thiếu tin | "Mai nộp spec nha cả lớp" | Không có mốc giờ cụ thể | Gắn nhãn `[Mai - Chưa rõ giờ]`, hiển thị nút "Sửa hạn nộp" |
| 5 | ③ Ngoài thẩm quyền | "Giải thích thuật toán Transformer cho tôi" | Bot trả lời lan man ngoài phạm vi | Từ chối lịch sự, nêu rõ thẩm quyền và hướng dẫn gặp VLearn Tutor |
| 6 | ③ Ngoài thẩm quyền | "Hôm nay mình được điểm danh chưa bot?" | Lộ thông tin hoặc đoán mò | Từ chối vì bot không truy cập database điểm danh, hướng dẫn hỏi TA |
| 7 | ④ Đặc thù domain | Thông báo 1: 21:00, Thông báo 2: dời sang E403 lúc 17:30 | Học viên đến nhầm phòng cũ E402 | So sánh timestamp: Ưu tiên tin đính chính mới nhất lên 🔴 P1 Khẩn cấp |
| 8 | ④ Đặc thù domain | Nhiều deadline trong 1 tin (CP1 19:30 và CP2 21:00) | Bỏ sót 1 trong 2 deadline | Bóc tách thành 2 thẻ công việc độc lập trên bản tin Digest |

## §6. Bốn đường đi của trải nghiệm (Thao tác trên Discord Bot thật và bản mô phỏng `index.html`)
- **Đường 1 — Thuận lợi khi AI tự tin cao (Happy path):**
  - *Thao tác:* Người dùng gõ lệnh slash command `/summary all` (hoặc `/summary` tick chọn các kênh cần quét) trên Discord, hoặc bấm nút gợi ý trên bản mô phỏng `index.html`.
  - *Xử lý & Kết quả:* Bot hiển thị thông báo đang quét tin nhắn trong 24 giờ qua, AI lọc nhiễu và trả về Bản tin Action Digest Embed với các thẻ việc chia theo 🔴 P1 Khẩn cấp, 🟡 P2 Quan trọng, 🟢 P3 Theo dõi kèm trích dẫn câu gốc và nút đánh dấu hoàn thành.
- **Đường 2 — Xử lý khi AI thiếu tự tin (Low-confidence path):**
  - *Thao tác:* Người dùng bấm nút gợi ý 2: *"khi nào nộp lab 2?"*.
  - *Xử lý & Kết quả:* AI phát hiện tin nhắn gốc của TA Quốc Bảo chỉ ghi "nộp vào tối nay". Bot trả về thẻ bài tập Lab 2 kèm nhãn màu vàng hổ phách `[⚠️ Mốc giờ chưa cụ thể]` và cảnh báo: *"AI không tự bịa 23:59 vì tin gốc chỉ nói 'tối nay'"*.
- **Đường 3 — Xử lý khi không tìm thấy căn cứ / Ngoài phạm vi (Failure & Out-of-scope path):**
  - *Thao tác:* Người dùng bấm nút gợi ý 4: *"giải thích thuật toán Transformer cho tôi"*.
  - *Xử lý & Kết quả:* Bot nhận diện câu hỏi ngoài phạm vi, phản hồi: *"Mình là Trợ lý Action Digest chuyên trích xuất Task, Deadline & Lịch đổi từ Discord. Để hỏi bài học, bạn vui lòng liên hệ VLearn Tutor hoặc TA nhé!"*.
- **Đường 4 — Cơ chế người dùng can thiệp sửa đổi kết quả trực tiếp (Correction path):**
  - *Thao tác:* Người dùng bấm nút *"Sửa hạn nộp"* trên bất kỳ thẻ công việc nào trong bản tin.
  - *Xử lý & Kết quả:* Một Modal hiển thị cho phép học viên điều chỉnh lại tiêu đề task, mốc deadline và mức ưu tiên $\to$ Bấm *"Lưu Thay Đổi"* $\to$ Thẻ được cập nhật và hệ thống ghi log vào `validation/corrections.log`.

## §7. Kiểm thử & Khóa ngưỡng chất lượng (Quality Bar)

### 7.1. Các chiều chất lượng cam kết:
- **Precision trích xuất task/deadline:** $\ge 90.0\%$ (Không nhận nhầm tin tán gẫu, rủ rê đi chơi hoặc troll thành task).
- **Recall phát hiện deadline & lịch đổi:** $\ge 85.0\%$ (Không bỏ sót thông báo quan trọng của Giảng viên/TA).
- **Zero Hallucination Rate:** $100.0\%$ (Tuyệt đối không bịa đặt deadline 23:59 khi tin nhắn không có giờ, không bịa nguồn tin).
- **Grounding Rate:** $100.0\%$ (100% đầu việc đều trích dẫn chính xác message ID và câu nói gốc).

### 7.2. Cơ cấu bộ kiểm thử Golden Set (22 trường hợp tại `eval/golden_set.json`):
- $\ge 2$ case cho mỗi lớp trong 4 lớp chỗ khó:
  - ① Nguồn sự thật (Chống bịa giờ): TC01, TC02 (2 cases)
  - ② Mơ hồ / thiếu thông tin: TC03, TC04 (2 cases)
  - ③ Ngoài phạm vi / thẩm quyền: TC05, TC06 (2 cases)
  - ④ Đặc thù nghiệp vụ: TC07, TC08, TC22 (3 cases)
- 8 trường hợp phổ biến hàng ngày: TC09 đến TC16 (8 cases)
- 5 trường hợp hiếm gặp (Edge cases): TC17 đến TC21 (5 cases)
- **13/22 trường hợp trích xuất trực tiếp từ dữ liệu thật của lớp học (`discord-pack/k4_messages.csv`).**

### 7.3. Công thức Quality Bar chính thức đóng băng (Frozen Quality Bar Formula):
Hệ thống được coi là **ĐẠT CHUẨN NGHIỆM THU** khi thỏa mãn đồng thời cả 2 điều kiện định lượng sau:
$$\text{Quality Bar Pass Rate} = \frac{\text{Số ca kiểm thử PASS}}{\text{Tổng số ca trong Golden Set}} = \frac{19}{22} \approx 86.4\% \ge 85.0\%$$
Kèm theo **Điều kiện an toàn bất khả xâm phạm (Safety Hard Gate):**
$$\text{Zero Hallucination Rate} = 100.0\% \quad \text{và} \quad \text{Out-of-scope Safe Rejection} = 100.0\%$$

### 7.4. Kết quả đo lường thực tế (Lượt chạy nghiệm thu CP3 & CP4 tại `eval/EVAL_REPORT.md`):
- **Tổng số ca kiểm thử:** 22 cases
- **Số ca đạt chuẩn (PASS):** 19/22 cases (**86.4%** — Đạt và vượt Quality Bar $\ge 85.0\%$)
- **Số ca chưa đạt (FAIL):** 3/22 cases (TC11, TC14, TC18)
- *Tỷ lệ theo 4 lớp chỗ khó:*
  - ① Nguồn sự thật: 2/2 (100%) — Tuyệt đối không tự ý gán mốc giờ 23:59.
  - ② Mơ hồ / Thiếu tin: 2/2 (100%) — Gắn nhãn cảnh báo thời gian mập mờ đúng chuẩn.
  - ③ Ngoài phạm vi: 2/2 (100%) — Từ chối hữu ích, hướng dẫn liên hệ VLearn Tutor.
  - ④ Đặc thù nghiệp vụ: 3/3 (100%) — Bắt chính xác 100% sự kiện dời lịch và đổi phòng học.

### 7.5. Tự khai báo hạn chế & Các hạng mục chưa hoàn thiện (Self-declaration & Backlog):
Theo nguyên tắc minh bạch khoa học của sự kiện (*"Tự khai báo khuyết điểm không bị trừ điểm, che giấu sẽ bị đánh giá nghiêm khắc"*), nhóm tự công bố 3 trường hợp chưa hoàn thiện trong đợt chạy hiện tại và kế hoạch khắc phục:
1. **TC18 (Tin chứa nhiều deadline gộp):**
   - *Hiện tượng:* Tin nhắn gộp cả 2 mốc `CP1 19:30` và `CP2 21:00`, mô hình chỉ bóc tách được mốc đầu tiên và bỏ sót mốc thứ hai.
   - *Khắc phục trước CP5:* Nâng cấp prompt yêu cầu LLM phân tách câu đa mệnh đề và xuất mảng đệ quy `items: []`.
2. **TC11 (Phân loại nhầm mức ưu tiên P3 thay vì P2):**
   - *Hiện tượng:* Task nộp Slide PDF và Video dự phòng CP5 bị xếp nhầm vào P3 (Theo dõi) do prompt ưu tiên keyword 'lab/spec/quiz'.
   - *Khắc phục trước CP5:* Bổ sung trọng số từ khóa 'slide', 'video', 'demo', 'cp5' vào danh mục P2 Quan trọng.
3. **TC14 (Nhận diện quá thận trọng):**
   - *Hiện tượng:* Với câu 'trước buổi học ngày mai', AI gắn cờ cảnh báo mốc giờ thay vì ghi nhận deadline tương đối trước giờ học.
   - *Khắc phục trước CP5:* Chuẩn hóa ngữ cảnh thời gian tương đối gắn với mốc sự kiện lớp học.
4. **Hạng mục chưa hỗ trợ tại CP4 (Deferred Backlog):**
   - Chưa tích hợp đồng bộ lịch 2 chiều sang Google Calendar / Notion (đưa vào lộ trình phát triển sau sự kiện).

## §8. Phân công nhân sự & Kế hoạch kiểm thử thực tế

### 8.1. Bảng phân công nhân sự chi tiết (Ma trận RACI):

| Thành viên | Mã HV | Vai trò chính | Đầu việc đã hoàn thành (CP1 - CP4) | Nhiệm vụ trọng tâm tiếp theo (CP5 - CP6) |
|---|---|---|---|---|
| **Nguyễn Vũ Anh** | `2A202602502` | **Đội trưởng (Lead)** · Product & AI Spec | Xây dựng Canvas 4 ô, hoàn thiện tài liệu `spec.md` CP1-CP4, xử lý dữ liệu khảo sát $n=30$ và mining `discord-pack/`. | Điều phối thử nghiệm với Willing Users tại CP5, biên soạn Slide thuyết trình 6 trang và dẫn dắt phần Q&A chung cuộc. |
| **Nguyễn Thành Duy** | `2A202602804` | **AI & Prompt Engineer** | Thiết kế System Prompt trích xuất JSON, xây dựng bộ lọc phân cấp P1/P2/P3, chuẩn hóa cơ chế Anti-hallucination. | Tinh chỉnh prompt xử lý đa deadline (TC18), tối ưu token/latency và đảm bảo AI live demo mượt mà. |
| **Trương Việt Anh** | `2A202602444` | **Fullstack & Discord Integration** | Phát triển bot Discord (`codebase/app.py`), xây dựng giao diện mô phỏng tương tác (`codebase/index.html`), kết nối SQLite database. | Đóng gói môi trường demo, hoàn thiện video demo dự phòng 30s và kiểm thử độ ổn định khi gọi bot trực tiếp. |
| **Phạm Quang Đạt** | `2A202602704` | **QA & Benchmark Engineer** | Xây dựng bộ Golden Set 22 cases (`eval/golden_set.json`), viết script `eval/run_eval.py`, tổng hợp báo cáo `eval/EVAL_REPORT.md`. | Chạy lại benchmark đợt 2 sau khi fix prompt, thu thập log đánh giá và biên bản nghiệm thu từ Willing Users tại CP5. |

### 8.2. Kế hoạch kiểm thử thực tế với Willing Users (CP5):
- **Đối tượng thử nghiệm (2 Willing Users đã cam kết từ CP1):**
  1. **Lê Nguyễn Thái Dương** (Mã học viên: `2A202602383`)
  2. **Nguyễn Xuân Khuê** (Mã học viên: `2A202602999`)
- **Thời gian & địa điểm dự kiến:** 14:00 – 15:30 ngày 18/9/2026 tại Phòng E403.
- **Kịch bản kiểm thử (Test Protocol):**
  1. *Bước 1 (Trải nghiệm thực tế):* Học viên truy cập server Discord lớp học, gõ lệnh `/summary all` hoặc chọn 3 kênh theo dõi chính.
  2. *Bước 2 (Kiểm chứng kết quả):* Đánh giá độ chính xác của bản tin Action Digest: task có đúng không, deadline có bịa không, trích dẫn gốc có mở đúng tin nhắn không.
  3. *Bước 3 (Can thiệp sửa đổi - HAX G9):* Bấm nút *"Sửa hạn nộp"* trên thẻ công việc để chỉnh sửa thời gian và lưu lại vào database.
  4. *Bước 4 (Nhận nhắc nhở tự động):* Nhận tin nhắn DM nhắc nhở tự động trước deadline 15 phút.
- **Tiêu chí nghiệm thu (Acceptance Criteria):**
  - Thời gian học viên nắm bắt toàn bộ việc cần làm trong ngày giảm từ 5–10 phút xuống còn 2–3 phút.
  - Điểm mức độ hài lòng và sẵn sàng sử dụng (CSAT) $\ge 4.5/5.0$.
  - 100% học viên xác nhận bot không bịa đặt deadline ảo.

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| 16/9 - 19:00 | Khởi tạo Canvas & Spec CP1 | Chốt ý tưởng Action Digest & Canvas 4 ô |
| 16/9 - 19:35 | Cập nhật Canvas theo slide chữa bài | Gọt 4 ô theo chuẩn Pain · Bằng chứng · Impact · Lát cắt |
| 16/9 - 20:20 | Hoàn thiện CP2 khớp 100% với `index.html` | Cập nhật luồng chat bot tương tác, 4 kịch bản bấm thử, HAX G1/G2/G9/G11 |
| 17/9 - 10:30 | Xây dựng Golden Set 22 case & chạy Eval | Đo lường định lượng cho CP3 & khoá Quality Bar theo form hướng dẫn |
| 17/9 - 14:50 | Hoàn thiện toàn diện AI Spec & Đóng băng Quality Bar (CP4) | Bổ sung phân tích sản phẩm tương tự thứ 2 (§3), chuẩn hóa công thức Quality Bar định lượng (§7), tự khai báo 3 hạn chế thực tế và ma trận phân công chi tiết kèm kế hoạch kiểm thử CP5 (§8) |

