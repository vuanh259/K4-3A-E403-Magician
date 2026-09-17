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
- **Khảo sát thực tế (Đạt Chuẩn A với $n = 33$ học viên, trong đó 30 người ngoài nhóm):**
  - **51.5% (17/33)** học viên xác nhận từng bỏ lỡ hoặc phát hiện muộn thông tin quan trọng trên Discord (deadline lab, workshop, daily standup).
  - **97.0% (32/33)** học viên mong muốn có công cụ tự động lọc và tổng hợp task/deadline/lịch thay đổi.
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
  - **Phạm Quang Đạt (2A202602704):** QA & Eval · Xây dựng Golden Set 22 case và đo lường độ chính xác.

---

## §1. User & Job
- **Job executor + workflow:** Học viên khóa học AI và TA phụ trách kênh Discord. Mỗi ngày học viên mở Discord 5-7 lần, lướt qua các kênh `#thông-báo`, `#general`, `#q-and-a` để tìm bài tập và lịch học, tự ghi chép lại hoặc chụp màn hình.
  
  ```mermaid
  flowchart LR
      A["Mở Discord 5–7 lần/ngày"] --> B["Lướt 3–10 channel tìm tin"]
      B --> C{"Tin quan trọng?"}
      C -- "Thảo luận vụn vặt" --> D["Bỏ qua (Tốn 5–10p/ngày)"]
      C -- "Thông báo Task/Deadline" --> E["Ghi chép thủ công / Chụp màn hình"]
      E --> F{"Dễ bị trôi tin?"}
      F -- "Có (51.5%)" --> G["Trễ hạn nộp bài / Nhầm phòng học"]
      F -- "Không" --> H["Nộp bài đúng giờ"]
  ```

- **Core JTBD:** Nắm bắt kịp thời, đầy đủ và chính xác các đầu việc cần làm cùng thời hạn nộp bài mà không phải đọc thủ công hàng trăm tin nhắn thảo luận.
- **Problem statement (KHÔNG chữ AI):** Kênh Discord có lượng tin nhắn thảo luận quá lớn khiến học viên mất 5–10 phút mỗi ngày đọc lướt và 50% từng bỏ lỡ hạn nộp bài tập hoặc nhầm phòng học do thông báo bị trôi.
- **Evidence (Chuẩn A và B — log đầy đủ tại `evidence_log.md`):**
  - **Số liệu khảo sát (Chuẩn A):** $n = 33$ học viên (trong đó 30 người ngoài nhóm), $51.5\%$ (17/33) xác nhận từng bỏ lỡ thông tin quan trọng; $97.0\%$ (32/33) mong muốn công cụ tự động tổng hợp.
  - **Khai thác dữ liệu (Chuẩn B):** Mining tập `discord-pack/` gồm 1.092 tin nhắn (779 tin từ học viên, 313 tin từ bot/BTC), chỉ ra 4 bản tin bot hiện có bị lỗi cắt cụt và thiếu trích xuất task.
  - **≥5 quote nguyên văn (Trích xuất 100% từ dữ liệu biểu mẫu khảo sát thực tế):**
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
| **C. Action Digest: Trích xuất Task, Deadline & Đổi lịch (CHỌN)** | **Toàn bộ ~230 học viên** phòng E403 + đội ngũ TA | **5–7 lần/ngày** (mỗi khi mở Discord tìm thông báo) | Mất **5–10 phút/ngày** lướt 3–10 kênh để nhặt task (dùng Action Digest giảm xuống còn **2–3 phút**); **51.5% (17/33)** từng bỏ lỡ deadline hoặc nhầm phòng học | Lãng phí **~20–38 giờ đọc lướt/ngày** cho cả phòng (dùng bot tiết kiệm được **~15–25 giờ/ngày** cho 230 học viên); gây hậu quả 0 điểm bài tập hoặc lỡ buổi học | **Cao nếu bịa deadline** (đã giải quyết triệt để bằng Conditional + Trích dẫn gốc) | **Rất cao** (lát cắt tập trung, dữ liệu `discord-pack/` dồi dào, kiểm chứng được ngay) |

- **Ứng viên ĐÃ LOẠI:** 
  - *Loại phương án A:* Bị trùng lặp trực tiếp với VLearn Tutor có sẵn của trường; phạm vi quá rộng không thể làm chỉn chu trong 47.5h.
  - *Loại phương án B:* Rủi ro Cost of error quá cao (học viên phản cảm việc bot tự tiện nhắn tin riêng khi chưa yêu cầu), vi phạm nguyên tắc tôn trọng quyền riêng tư.
- **Ứng viên CHỌN:** Chọn **Phương án C (Action Digest)** với lý do bằng số liệu định lượng vững chắc:
  1. **Đúng điểm đau lớn nhất:** $51.5\%$ (17/33) học viên xác nhận từng bị trôi tin quan trọng; $97.0\%$ (32/33) bày tỏ nhu cầu cấp thiết cần công cụ này.
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
- **Mức prototype nhắm tới:** [x] Working Prototype — Bot Discord AI thật chạy trực tiếp trên Server lớp học (`codebase/app.py`)
  > [!IMPORTANT]
  > **Khẳng định nghiệm thu Tiêu chí R5 (8 điểm — `codebase/` + demo):**
  > Bản mẫu của nhóm là **BOT DISCORD THẬT 100%** ([`codebase/app.py`](codebase/app.py)), KHÔNG PHẢI bản web mock (`index.html`). Hệ thống chạy live thực tế trên nền tảng Discord, đáp ứng đầy đủ 3 điều kiện của Rubric R5:
  > 1. **Chạy End-to-End theo lát cắt đã khai:** Học viên gõ lệnh `/summary all` $\to$ Bot quét tin nhắn thật 24h từ các kênh $\to$ AI phân tích lọc tin $\to$ Trả về Embed bản tin Action Digest với link nguồn $\to$ Học viên gõ `/correct` sửa trực tiếp vào SQLite $\to$ Hệ thống tự động gửi DM nhắc nhở trước hạn chót. Toàn bộ luồng khép kín không can thiệp thủ công giữa chừng.
  > 2. **Quyết định trung tâm bằng AI thật 100%:** Lời gọi LLM API thật tại [`codebase/ai.py`](codebase/ai.py) (Gemini 2.5 Flash / GPT-4o-mini) với JSON Schema bắt buộc; toàn bộ vết gọi AI thật được lưu tại [`eval/ai_traces.log`](eval/ai_traces.log).
  > 3. **Phần Mock vs Phần Thật minh bạch:**
  >    - *Phần Thật (100% Core Engine):* Bot Discord thật ([`app.py`](codebase/app.py)), AI Engine ([`ai.py`](codebase/ai.py)), CSDL SQLite ([`storage.py`](codebase/storage.py)), Nhắc hẹn tự động qua DM ([`reminders.py`](codebase/reminders.py)), Giao diện Rich Embed trên Discord ([`ui.py`](codebase/ui.py)).
  >    - *Phần Mock:* Hoàn toàn KHÔNG có logic giả lập trong Discord Bot. File `codebase/index.html` chỉ là bản mô phỏng giao diện tĩnh (Companion Web Mockup) tạo từ mốc CP2 để phục vụ trình chiếu slide hoặc chạy demo dự phòng offline khi mất mạng.
- **Automation:** [x] Conditional / Augment
  - *Lý do theo Cost-of-error:* Việc thông báo sai hạn nộp bài (deadline) hoặc sai phòng học gây hậu quả nghiêm trọng trực tiếp (học viên bị 0 điểm hoặc lỡ buổi học). Vì vậy giải pháp áp dụng **Conditional / Augment**: Con người luôn là người quyết định cuối cùng; AI chỉ trích xuất có bằng chứng và gắn cờ cảnh báo khi độ tin cậy thấp.
- **§4b. Bảng 4 nguyên tắc HAX/PAIR áp dụng cụ thể trên Bot Discord thật & Bản demo:**

| Nguyên tắc | Mô tả nguyên tắc | Vị trí áp dụng cụ thể trên Bot Discord thật (`codebase/app.py`, `ui.py`) & Bản demo |
|---|---|---|
| **HAX G1 (Nêu rõ năng lực hệ thống)** | Giúp người dùng hiểu hệ thống có thể làm gì và không làm gì | 1. **Trên Bot Discord thật:** Lệnh slash command `/summary`: mô tả rõ ràng *"Tổng hợp tin nhắn 24h qua và trích xuất Task, Deadline, Lịch đổi"*. Khi user hỏi ngoài phạm vi (như giải bài tập), bot từ chối lịch sự và hướng dẫn gặp VLearn Tutor.<br>2. **Trên Companion UI (`index.html`):** Dòng mô tả chức năng ngay dưới Header. |
| **HAX G2 (Thể hiện rõ độ tin cậy)** | Hiển thị mức độ chắc chắn của kết quả AI | 1. **Trên Bot Discord thật (`ui.py` L48-84):** Icon màu sắc trực quan (🔴 high, 🟠 medium, 🟢 low); hiển thị điểm `Confidence: 0.xx` (nếu < 0.80 thì kèm cờ cảnh báo `⚠️ Mốc giờ/thông tin cần xác nhận lại`, gán `deadline_iso: null` chứ tuyệt đối không tự bịa giờ 23:59).<br>2. **Trên Companion UI (`index.html`):** Thẻ màu vàng `🟡 Needs review` cảnh báo *"AI không đủ căn cứ để tự kết luận"*. |
| **HAX G9 (Hỗ trợ sửa sai tức thì)** | Cho phép người dùng can thiệp và sửa đổi kết quả trực tiếp | 1. **Trên Bot Discord thật ([`app.py` L422](codebase/app.py#L422)):** Lệnh slash command `/correct task_id [deadline_iso] [priority] [title]`, ghi đè trực tiếp vào SQLite database và tự động tính lại lịch reminder.<br>2. **Trên Companion UI (`index.html`):** Nút **"✏️ Sửa task"** trên từng thẻ mở Modal chỉnh sửa live. |
| **HAX G11 (Giải thích lý do & Dẫn nguồn)** | Giúp người dùng hiểu vì sao AI đưa ra kết quả | 1. **Trên Bot Discord thật ([`ui.py` L66-76](codebase/ui.py#L66-L76)):** Trên mỗi thẻ Embed đều trích dẫn kênh `#{source_channel}`, người gửi `{source_author}`, trích dẫn nguyên văn `> {snippet}` và link bấm trực tiếp mở tin nhắn Discord gốc `[Nguồn]({source_url})`.<br>2. **Trên Companion UI (`index.html`):** Nút "Xem message gốc" hiển thị câu nói của TA/Giảng viên. |

## §5. Kiểu lỗi — 4 lớp chỗ khó & kịch bản (8 kịch bản rủi ro theo chuẩn HAX Playbook)

| STT | Lớp chỗ khó | Tình huống cụ thể (Input) | Nguy cơ lỗi | Hành vi mong muốn (Nói gì, Hiện gì, Cho user làm gì tiếp) | Nguyên tắc áp dụng (HAX/PAIR) |
|---|---|---|---|---|---|
| 1 | ① Nguồn sự thật | "Bài tập Lab 2 nộp vào tối nay nhé" | AI tự ý bịa mốc giờ 23:59 (Hallucination) | Trích xuất task nhưng đặt `deadline_iso: null`; trên Bot Discord thật hiển thị Confidence < 0.80 kèm cảnh báo cần xác nhận mốc giờ, không tự bịa giờ (trên companion UI hiển thị nhãn `🟡 Needs review`) | **HAX G2** (Rõ độ tin cậy) & **HAX G11** (Dẫn nguồn) |
| 2 | ① Nguồn sự thật | Học viên A nhắn: "Chắc mai nộp lab đấy cả nhà" | AI nhặt tin đồn của học viên thành deadline thật | Lọc bỏ qua tin nhắn không thuộc người có thẩm quyền (GV/TA/BTC), không tạo thẻ công việc | **PAIR Explainability & Grounding** |
| 3 | ② Mơ hồ / Thiếu tin | TA nhắn: "Tuần này nhớ nộp báo cáo tiến độ nhé" | AI đoán mò thứ hoặc bỏ sót việc | Gắn nhãn `[Chưa rõ ngày cụ thể]`, tự động xếp vào nhóm 🟢 Low (Theo dõi), gợi ý hỏi lại TA | **HAX G2** & **PAIR Graceful Failure** |
| 4 | ② Mơ hồ / Thiếu tin | GV nhắn: "Mai nộp spec nha cả lớp" | AI không có giờ nộp chính xác | Gắn nhãn `[Mai - Chưa rõ giờ]`, xếp vào 🟠 Medium (Quan trọng), cho phép dùng `/correct` trên Discord (hoặc nút "Sửa task" trên companion UI) để cập nhật | **HAX G9** (Hỗ trợ sửa sai tức thì) |
| 5 | ③ Ngoài thẩm quyền | User gõ: "Giải thích thuật toán Transformer cho tôi" | Bot trả lời lan man ngoài phạm vi hoặc sai kiến thức | Bot từ chối lịch sự: *"Mình là Trợ lý Action Digest chuyên trích xuất Task & Lịch. Để hỏi bài học, bạn vui lòng sử dụng VLearn Tutor nhé!"* | **HAX G1** (Rõ năng lực hệ thống) & **PAIR Mental Models** |
| 6 | ③ Ngoài thẩm quyền | User gõ: "Hôm nay mình được điểm danh chưa bot?" | Bot suy đoán bừa hoặc lộ dữ liệu điểm danh | Bot phản hồi không có quyền truy cập DB điểm danh, hướng dẫn liên hệ trực tiếp TA trực phòng | **HAX G1** & **PAIR User Control** |
| 7 | ④ Đặc thù domain | Tin 1: "Học tại E402". Tin 2 (14:00): "Đổi sang E403" | Học viên đến nhầm phòng cũ E402 | So sánh timestamp, nhận diện từ khóa 'đổi/chuyển', ghi đè phòng mới E403 và nâng lên 🔴 High Khẩn cấp | **HAX G2** & **Domain Taxonomy** |
| 8 | ④ Đặc thù domain | "Hạn chốt CP1 lúc 19:30 và CP2 lúc 21:00 tối nay" | Bỏ sót 1 trong 2 deadline gộp trong 1 tin | Bóc tách thành 2 thẻ công việc độc lập (CP1: 19:30, CP2: 21:00) trên bản tin Action Digest | **PAIR Data Structuring** |

## §6. Bốn đường đi của trải nghiệm (Thao tác trên Bot Discord thật — kèm bản mô phỏng phụ trợ)
- **Đường 1 — Thuận lợi khi AI tự tin cao (Happy path):**
  - *Thao tác:* Học viên gõ lệnh slash command `/summary all` (hoặc `/summary` tick chọn các kênh cần quét) trên Discord.
  - *Xử lý & Kết quả:* Bot hiển thị thông báo đang quét tin nhắn 24h qua (`app.py: collect_messages`), gọi AI phân tích (`ai.py: analyze_messages`), lưu task vào SQLite (`storage.py: save_summary_run`), hiển thị Bản tin Action Digest Embed (`ui.py: build_summary_embed`) với các thẻ việc chia theo 🔴 High, 🟠 Medium, 🟢 Low kèm trích dẫn nguyên văn câu gốc, link nhảy trực tiếp đến tin nhắn Discord gốc `[Nguồn]({source_url})` và tự động lên lịch DM nhắc nhở (`reminders.py`).
- **Đường 2 — Xử lý khi AI thiếu tự tin (Low-confidence path — ②):**
  - *Thao tác:* Học viên gõ lệnh `/summary` quét kênh có tin nhắn mơ hồ (ví dụ: thông báo chỉ ghi *"nộp vào tối nay"* không rõ giờ hoặc chat *"Tối mai làm nhé"*).
  - *Xử lý & Kết quả:* AI phát hiện độ tin cậy thấp (`confidence = 0.70 < 0.80`), gán `deadline_iso: null` và không tự ý gán giờ mặc định 23:59. Trên Bot Discord thật (`ui.py` L80), bot hiển thị: *"Confidence: 0.70 ⚠️ (Mốc giờ/thông tin cần xác nhận lại)"* và trích dẫn câu gốc để học viên dùng `/correct` bổ sung giờ chính xác (HAX G2). (Trên companion UI `index.html`, bot hiển thị thẻ màu vàng `🟡 Needs review`).
- **Đường 3 — Xử lý khi không tìm thấy căn cứ (Failure / Zero Grounding — ①):**
  - *Thao tác:* Học viên gõ `/summary` trên kênh `#thao-luan-chung` chỉ toàn tin nhắn rủ đi ăn trưa và tán gẫu.
  - *Xử lý & Kết quả:* Bot phản hồi an toàn: *"Không phát hiện task, deadline hoặc lịch thay đổi nào trong 24 giờ qua từ các kênh đã chọn"*, tuyệt đối không bịa đặt task giả định (Zero Hallucination).
- **Đường 4 — Cơ chế người dùng can thiệp sửa đổi kết quả trực tiếp (Correction path — HAX G9):**
  - *Thao tác trên Bot Discord thật:* Học viên gõ lệnh `/correct task_id: 1 deadline_iso: 2026-09-17T21:00:00+07:00 priority: high title: Nộp bài Lab 2`.
  - *Xử lý & Kết quả trên Discord:* Bot gọi `store.set_correction()` ghi đè thông tin trực tiếp vào SQLite database, đặt lại cờ `reminder_sent = 0` để tiến trình ngầm `reminders.py` tự động tính toán lại lịch bắn DM nhắc nhở, và phản hồi ephemeral message xác nhận cập nhật thành công. (Trên companion UI `index.html`, học viên bấm nút *"✏️ Sửa task"* trên thẻ để chỉnh sửa tương tự).
- **Khi bị đòi hỏi ngoài phạm vi (Out-of-scope — ③):**
  - *Thao tác:* Học viên gõ hỏi: *"giải thích thuật toán Transformer cho tôi"* hoặc *"hôm nay mình được điểm danh chưa bot?"*.
  - *Xử lý & Kết quả:* Bot nhận diện câu hỏi ngoài phạm vi, từ chối lịch sự: *"Mình là Trợ lý Action Digest chuyên trích xuất Task, Deadline & Lịch đổi từ Discord. Để hỏi bài học, bạn vui lòng liên hệ VLearn Tutor hoặc TA nhé!"* (HAX G1).
- **Case đặc thù domain lớp học (Domain Specific — ④):**
  - *Thao tác:* Giảng viên/TA đăng tin lúc 08:00 thông báo học phòng E402, sau đó 14:00 đăng tin đính chính chuyển sang E403.
  - *Xử lý & Kết quả:* AI so khớp timestamp và cú pháp đính chính, tự động cập nhật phòng học mới E403, ghi chú `(Đổi từ phòng cũ E402)` và đẩy thẻ lên mức 🔴 High để tránh học viên đi nhầm phòng.

## §7. Kiểm thử & Khóa ngưỡng chất lượng (Quality Bar)

### 7.1. Các chiều chất lượng cam kết (Định nghĩa kiểm chứng được để người ngoài nhóm cùng ra 1 kết quả):
- **Precision trích xuất task/deadline ($\ge 90.0\%$):** 
  - *Định nghĩa kiểm chứng:* $\frac{\text{Số task trích đúng}}{\text{Tổng số task bot trả về}}$. Người ngoài kiểm tra: nếu thẻ chứa tin rác/tán gẫu, rủ rê ăn trưa $\to$ chấm FAIL.
- **Recall phát hiện deadline & lịch đổi ($\ge 85.0\%$):** 
  - *Định nghĩa kiểm chứng:* $\frac{\text{Số task bot phát hiện}}{\text{Tổng số task thật có trong ngữ cảnh}}$. Người ngoài kiểm tra: nếu bỏ sót bất kỳ thông báo bài tập/lịch học chính thức nào từ GV/TA $\to$ chấm FAIL.
- **Zero Hallucination Rate ($100.0\%$ — Safety Hard Gate):** 
  - *Định nghĩa kiểm chứng:* Đối chiếu câu nói gốc: nếu AI tự ý bịa thêm thông tin không có trong tin gốc (ví dụ: tự ý gán giờ mặc định "23:59" khi câu chỉ nói "tối nay", hoặc tự bịa phòng học) $\to$ chấm FAIL ngay lập tức.
- **Grounding Rate ($100.0\%$ — Grounding Hard Gate):** 
  - *Định nghĩa kiểm chứng:* $100\%$ đầu việc đều trích dẫn chính xác message ID và câu nói gốc. Người ngoài bấm link/ID: mở đúng tin nhắn gốc trên Discord $\to$ PASS.
- **Out-of-scope Safe Rejection ($100.0\%$ — Scope Hard Gate):** 
  - *Định nghĩa kiểm chứng:* Khi gặp yêu cầu giải bài tập lý thuyết hoặc tra điểm danh cá nhân, AI phải từ chối lịch sự và hướng dẫn sang VLearn Tutor hoặc TA; nếu AI cố tình trả lời lý thuyết hoặc suy đoán điểm danh $\to$ chấm FAIL.

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

| Chỉ số kiểm thử | Quality Bar cam kết | Kết quả thực tế đợt chạy CP3 | Trạng thái nghiệm thu |
|---|---|---|---|
| **Quality Bar Pass Rate** | $\ge 85.0\%$ | **86.4%** (19/22 cases) | ✅ **ĐẠT (PASS)** |
| **Zero Hallucination Rate** | **100.0%** | **100.0%** (22/22 cases) | ✅ **ĐẠT (PASS)** |
| **Grounding Rate** | **100.0%** | **100.0%** (22/22 cases) | ✅ **ĐẠT (PASS)** |
| **Out-of-scope Safe Rejection** | **100.0%** | **100.0%** (2/2 cases) | ✅ **ĐẠT (PASS)** |
| **Bảo vệ đính chính lịch đổi** | $100.0\%$ | **100.0%** (3/3 cases) | ✅ **ĐẠT (PASS)** |

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
  3. *Bước 3 (Can thiệp sửa đổi - HAX G9):* Bấm nút *"✏️ Sửa task"* (hoặc gõ lệnh `/correct task_id`) để chỉnh sửa thời gian/độ ưu tiên và lưu lại vào database.
  4. *Bước 4 (Nhận nhắc nhở tự động):* Nhận tin nhắn DM nhắc nhở tự động trước deadline 15 phút.
- **Tiêu chí nghiệm thu (Acceptance Criteria):**
  - Thời gian học viên nắm bắt toàn bộ việc cần làm trong ngày giảm từ 5–10 phút xuống còn 2–3 phút.
  - Điểm mức độ hài lòng và sẵn sàng sử dụng (CSAT) $\ge 4.5/5.0$.
  - 100% học viên xác nhận bot không bịa đặt deadline ảo.

### 8.3. Multi-prototype (Cân nhắc thiết kế & Quyết định chọn phương án):
- **Trục khác biệt cốt lõi:** Cơ chế kích hoạt & hình thức phân phối bản tin (Trigger & Delivery Mechanism):
  - *Phương án 1 (Proactive Bot Push):* Bot tự động rà soát chatlog định kỳ và tự ý gửi Direct Message (DM) nhắc việc cho từng học viên mỗi khi phát hiện thông báo mới.
  - *Phương án 2 (On-demand Slash Command `/summary` + Opt-in DM Reminders - CHỌN):* Bot chỉ tổng hợp và đăng Bản tin Embed trong kênh chung khi học viên chủ động gõ lệnh `/summary` (hoặc `/summary all`); đồng thời chỉ gửi DM nhắc nhở cá nhân trước giờ deadline khi học viên chủ động bấm theo dõi task.
- **Bằng chứng & Lý do chọn Phương án 2:**
  - *Khảo sát thực tế ($n=33$):* $83.3\%$ học viên cho biết khó khăn lớn nhất là *"quá nhiều tin nhắn và thông báo rác"*, dẫn đến việc nhiều bạn phải tắt thông báo.
  - *Chi phí sai sót (Cost of error):* Nếu bot tự động DM liên tục (Phương án 1), khi gặp false positive sẽ làm phiền và gây ức chế, dẫn đến việc học viên block bot (thất bại hoàn toàn). Phương án 2 tôn trọng quyền kiểm soát của người dùng (HAX G17 / PAIR Control), đảm bảo bot là người hỗ trợ tin cậy và không bao giờ spam.

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| 16/9 - 19:00 | Khởi tạo Canvas & Spec CP1 | Chốt ý tưởng Action Digest & Canvas 4 ô |
| 16/9 - 19:35 | Cập nhật Canvas theo slide chữa bài | Gọt 4 ô theo chuẩn Pain · Bằng chứng · Impact · Lát cắt |
| 16/9 - 20:20 | Hoàn thiện CP2 với Companion Web Mockup | Xây dựng wireframe tương tác `codebase/index.html` mô phỏng 4 kịch bản bấm thử, kiểm chứng HAX G1/G2/G9/G11 |
| 17/9 - 10:30 | Xây dựng Golden Set 22 case & chạy Eval | Đo lường định lượng cho CP3 & khoá Quality Bar theo form hướng dẫn |
| 17/9 - 14:50 | Hoàn thiện toàn diện AI Spec & Đóng băng Quality Bar (CP4) | Bổ sung phân tích sản phẩm tương tự thứ 2 (§3), chuẩn hóa công thức Quality Bar định lượng (§7), tự khai báo 3 hạn chế thực tế và ma trận phân công chi tiết kèm kế hoạch kiểm thử CP5 (§8) |
| 17/9 - 15:40 | Chuẩn hóa Working Prototype cho Tiêu chí R5 (8 điểm) | Khẳng định Working Prototype chính thức là Bot Discord thật (`codebase/app.py`), làm rõ phần Thật (Discord bot + LLM + SQLite + DM reminder) vs phần Mock (`index.html` companion UI) |

