# AI SPEC — Discord Action Digest (Trích xuất Task, Deadline & Thay đổi lịch) · Nhóm Magician · Phòng E403
Hướng: [ ] A — VLearn  [x] B — Trợ lý Học viên (Discord)  [ ] C — Làn mở  
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới

---

## 📌 Phụ lục CP1: Canvas 4 Ô (Đã nộp Checkpoint 1)

### 🟩 Ô 1: Người dùng & Nỗi đau
- **Job executor:** Học viên khóa học AI và TA quản lý kênh Discord hàng ngày.
- **Quy trình hiện tại:** Học viên phải theo dõi từ 3 đến 10 channel Discord mỗi ngày để tìm kiếm thông báo bài tập, lịch học, lịch nộp lab.
- **Nỗi đau cốt lõi (Core Pain - KHÔNG chữ AI):** Kênh Discord có lượng tin nhắn thảo luận quá lớn khiến học viên mất 10–20 phút mỗi ngày đọc lướt và 50% từng bỏ lỡ hạn nộp bài tập hoặc nhầm phòng học do thông báo bị trôi.

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
- **Problem statement (KHÔNG chữ AI):** Kênh Discord có lượng tin nhắn thảo luận quá lớn khiến học viên mất 10–20 phút mỗi ngày đọc lướt và 50% từng bỏ lỡ hạn nộp bài tập hoặc nhầm phòng học do thông báo bị trôi.
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
- **Bảng impact ≥3 ứng viên:**

| Ứng viên | Đối tượng tác động | Tần suất | Chi phí sai sót (Cost of error) | Tính khả thi (47.5h) |
|---|---|---|---|---|
| **A. Trợ lý Q&A kiến thức bài học** | Học viên hỏi bài | Rất cao | Thấp - Trung bình (giải thích sai khái niệm) | Thấp (cần RAG toàn bộ bài giảng và slide) |
| **B. Bot chủ động phát hiện học viên stuck & gửi DM** | Học viên gặp khó | Thấp | Rất cao (xâm phạm riêng tư, gây ức chế và spam) | Trung bình (khó xác định ngữ cảnh stuck) |
| **C. Action Digest: Trích xuất Task, Deadline & Đổi lịch (CHỌN)** | Toàn bộ học viên + TA | Hàng ngày | Cao nếu bịa deadline (giải quyết triệt để bằng Conditional + Trích dẫn) | Rất cao, bám đúng 50% nỗi đau thật của học viên |

- **Ứng viên ĐÃ LOẠI:** Loại A vì trùng lặp VLearn Tutor và quá rộng; loại B vì vi phạm tính riêng tư và rủi ro spam người dùng.
- **Ứng viên CHỌN:** Chọn C vì tác động trực tiếp đến $50\%$ học viên từng miss tin, có $96.7\%$ nhu cầu sử dụng thực tế.

## §3. Giải pháp tương tự đã nghiên cứu
- **Bot bản tin ngày hiện tại (trong `data/discord-pack/`):**
  - *Flow:* Tự động gom tin nhắn trong ngày và xuất ra một đoạn văn xuôi tóm tắt các chủ đề được hỏi.
  - *Đáng học:* Cơ chế tự động lên lịch quét định kỳ.
  - *Đáng né:* Tóm tắt cắt cụt, chèn lỗi "nguồn tham chiếu", không phân biệt được đâu là tin rác và đâu là việc cần làm ngay.
  - *Mình khác gì:* Tập trung vào Actionable Items (Task, Deadline, Lịch đổi), phân loại 3 mức ưu tiên P1/P2/P3 và luôn hiển thị trích dẫn nguồn gốc kèm nút kiểm chứng.

## §4. Thiết kế & Bản mẫu tương tác (CP2)
- **Lát cắt MỘT CÂU:** *Một học viên khóa AI Thực Chiến · dán hoặc chọn một luồng tin nhắn Discord trong ngày (hoặc gõ lệnh 'tìm cho tôi những vấn đề quan trọng hôm nay') · AI quyết định tin này chứa Task, Deadline hay Lịch đổi khẩn cấp hay không (P1/P2/P3) · trả về Thẻ công việc gồm tiêu đề, thời hạn và độ ưu tiên kèm trích dẫn nguyên văn câu gốc từ TA/Giảng viên (hoặc gắn cờ cảnh báo nếu mốc giờ mập mờ).*
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

## §6. Bốn đường đi của trải nghiệm (Thao tác trực tiếp trên `codebase/index.html`)
- **Đường 1 — Thuận lợi khi AI tự tin cao (Happy path):**
  - *Thao tác:* Người dùng gõ câu lệnh *"tìm cho tôi những vấn đề quan trọng hôm nay"* (hoặc bấm nút gợi ý 1).
  - *Xử lý & Kết quả:* Bot hiển thị hiệu ứng đang đọc tin, sau đó xuất Bản tin Action Digest với 4 thẻ việc chia theo 🔴 P1 Khẩn cấp, 🟡 P2 Quan trọng, 🟢 P3 Theo dõi kèm trích dẫn nguyên văn câu gốc từ TA/Giảng viên.
- **Đường 2 — Xử lý khi AI thiếu tự tin (Low-confidence path):**
  - *Thao tác:* Người dùng bấm nút gợi ý 2: *"khi nào nộp lab 2?"*.
  - *Xử lý & Kết quả:* AI phát hiện tin nhắn gốc của TA Quốc Bảo chỉ ghi "nộp vào tối nay". Bot trả về thẻ bài tập Lab 2 kèm nhãn màu vàng hổ phách `[⚠️ Mốc giờ chưa cụ thể]` và cảnh báo: *"AI không tự bịa 23:59 vì tin gốc chỉ nói 'tối nay'"*.
- **Đường 3 — Xử lý khi không tìm thấy căn cứ / Ngoài phạm vi (Failure & Out-of-scope path):**
  - *Thao tác:* Người dùng bấm nút gợi ý 4: *"giải thích thuật toán Transformer cho tôi"*.
  - *Xử lý & Kết quả:* Bot nhận diện câu hỏi ngoài phạm vi, phản hồi: *"Mình là Trợ lý Action Digest chuyên trích xuất Task, Deadline & Lịch đổi từ Discord. Để hỏi bài học, bạn vui lòng liên hệ VLearn Tutor hoặc TA nhé!"*.
- **Đường 4 — Cơ chế người dùng can thiệp sửa đổi kết quả trực tiếp (Correction path):**
  - *Thao tác:* Người dùng bấm nút *"Sửa hạn nộp"* trên bất kỳ thẻ công việc nào trong bản tin.
  - *Xử lý & Kết quả:* Một Modal hiển thị cho phép học viên điều chỉnh lại tiêu đề task, mốc deadline và mức ưu tiên $\to$ Bấm *"Lưu Thay Đổi"* $\to$ Thẻ được cập nhật và hệ thống ghi log vào `validation/corrections.log`.

## §7. Kiểm thử
- **Chiều chất lượng:** Precision trích xuất $\ge 90\%$, Recall deadline $\ge 85\%$, Zero Hallucination Rate $100\%$.
- **Cơ cấu Golden Set (22 trường hợp tại `eval/golden_set.json`):**
  - $\ge 2$ case cho mỗi lớp trong 4 lớp chỗ khó:
    - ① Nguồn sự thật (Chống bịa giờ): TC01, TC02 (2 cases)
    - ② Mơ hồ / thiếu thông tin: TC03, TC04 (2 cases)
    - ③ Ngoài phạm vi / thẩm quyền: TC05, TC06 (2 cases)
    - ④ Đặc thù nghiệp vụ: TC07, TC08, TC22 (3 cases)
  - 8 trường hợp phổ biến hàng ngày: TC09 đến TC16 (8 cases)
  - 5 trường hợp hiếm gặp (Edge cases): TC17 đến TC21 (5 cases)
  - **13/22 trường hợp trích xuất trực tiếp từ data thật (`discord-pack/k4_messages.csv`).**
- **Quality Bar đã chốt:** "Đạt khi $\ge 85.0\%$ qua bộ Golden Set, và $100\%$ không bịa đặt deadline khi thông tin mập mờ (Zero Hallucination)."
- **Kết quả lượt chạy thực tế (Lượt 1 - Cập nhật trước CP3 tại `eval/EVAL_REPORT.md`):**
  - **Số ca kiểm thử:** 22 cases
  - **Đạt chuẩn (PASS):** 19/22 cases (**86.4%** — Đạt Quality Bar $\ge 85\%$)
  - **Không đạt (FAIL):** 3/22 cases (TC11, TC14, TC18)
  - *Tỷ lệ theo 4 lớp chỗ khó:*
    - ① Nguồn sự thật: 2/2 (100%) — Tuyệt đối không bịa giờ 23:59.
    - ② Mơ hồ / Thiếu tin: 2/2 (100%) — Gắn cờ cảnh báo đúng chuẩn.
    - ③ Ngoài phạm vi: 2/2 (100%) — Từ chối hữu ích, hướng dẫn VLearn Tutor.
    - ④ Đặc thù nghiệp vụ: 3/3 (100%) — Bắt đúng dời lịch và dời phòng học.
  - *Phân tích 3 lỗi thất bại:*
    1. TC18 (Nhiều deadline trong 1 tin): Bị cắt cụt mốc sau, chỉ bắt được mốc đầu. Khắc phục: Đệ quy duyệt JSON items.
    2. TC11 (Phân loại nhầm P3): Thiếu keyword 'lab/spec', xếp nhầm Slide PDF vào P3. Khắc phục: Thêm trọng số keyword 'slide/demo'.
    3. TC14 (Nhận diện quá thận trọng): Gắn cờ ambiguous do câu 'trước buổi học ngày mai'. Khắc phục: Chuẩn hóa ngữ cảnh thời gian.

## §8. Phân công & Kế hoạch
- **Nguyễn Vũ Anh (2A202602502):** Đội trưởng · AI Spec & Bằng chứng khảo sát.
- **Nguyễn Thành Duy (2A202602804):** AI & Prompt Engineering (P1/P2/P3).
- **Trương Việt Anh (2A202602444):** Fullstack & Discord Integration (`codebase/index.html`).
- **Phạm Quang Đạt (2A202602704):** QA & Golden Set 22 case (`eval/golden_set.json` & `eval/run_eval.py`).
- **Willing users (CP5):** Lê Nguyễn Thái Dương (2A202602383), Nguyễn Xuân Khuê (2A202602999).

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| 16/9 - 19:00 | Khởi tạo Canvas & Spec CP1 | Chốt ý tưởng Action Digest & Canvas 4 ô |
| 16/9 - 19:35 | Cập nhật Canvas theo slide chữa bài | Gọt 4 ô theo chuẩn Pain · Bằng chứng · Impact · Lát cắt |
| 16/9 - 20:20 | Hoàn thiện CP2 khớp 100% với `index.html` | Cập nhật luồng chat bot tương tác, 4 kịch bản bấm thử, HAX G1/G2/G9/G11 |
| 17/9 - 10:30 | Xây dựng Golden Set 22 case & chạy Eval | Đo lường định lượng cho CP3 & khoá Quality Bar theo form hướng dẫn |

