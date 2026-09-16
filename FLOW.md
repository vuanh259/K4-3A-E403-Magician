# Sơ đồ Luồng Hoạt Động (User Flow Diagram) — CP2

Dưới đây là sơ đồ luồng hoạt động từ lúc tin nhắn Discord phát sinh đến khi xuất ra bản tin Action Digest cho học viên.

```mermaid
flowchart TD
    A([Tin nhắn mới trên kênh Discord]) --> B[Bộ lọc tiền xử lý Pre-filter]
    
    B -- "Sticker / Icon / Chào hỏi / Tán gẫu" --> C[(Bỏ qua - Không xử lý)]
    
    B -- "Tin có nội dung thông báo / thảo luận" --> D{AI Intent & Action Classifier}
    
    D -- "Không có Task / Deadline / Đổi lịch" --> C
    
    D -- "Chứa Task / Deadline / Đổi lịch" --> E[Trích xuất Thông tin cốt lõi:\n- Tiêu đề việc (Task)\n- Mốc thời gian (Deadline)\n- Người thông báo & Trích dẫn gốc]
    
    E --> F{Kiểm tra Độ chắc chắn của thời gian}
    
    F -- "Thời gian mập mờ (vd: 'tối nay')" --> G[Gắn cờ cảnh báo: ⚠️ Cần xác nhận lại\nGiữ nguyên quote gốc, không bịa giờ]
    F -- "Thời gian rõ ràng (ngày, giờ cụ thể)" --> H[Ghi nhận Deadline chính xác]
    
    G --> I{Phân loại Mức độ Ưu tiên}
    H --> I
    
    I -- "Thay đổi lịch / Phòng học HOẶC Deadline < 24h" --> J[🔴 P1 - Khẩn cấp: Cần làm ngay]
    I -- "Task bài tập mới / Deadline > 24h" --> K[🟡 P2 - Quan trọng: Lên kế hoạch]
    I -- "Thông báo chung / Nhắc nhở định kỳ" --> L[🟢 P3 - Theo dõi]
    
    J --> M[Tổng hợp vào Action Digest]
    K --> M
    L --> M
    
    M --> N([Bản tin hiển thị trên Web Dashboard & Discord Channel])
    
    N --> O{Tương tác của Học viên}
    O -- "Bấm xem tin gốc" --> P[Mở trực tiếp tin nhắn Discord để đối chiếu]
    O -- "Bấm báo sai" --> Q[Gửi feedback điều chỉnh vào validation log]
```

### Giải thích các nhánh luồng (4 đường đi trải nghiệm):
1. **Happy Path:** Thông báo có thời hạn rõ ràng từ Giảng viên/TA -> Trích xuất thành công -> Phân vào P1/P2 kèm link tin nhắn gốc.
2. **Low-confidence (Thời gian mập mờ):** Tin nhắn dùng từ tương đối ("tối nay", "mai") -> Gắn nhãn vàng cảnh báo, hiển thị trích dẫn nguyên văn, tuyệt đối không bịa mốc giờ.
3. **Out of Scope / Noise:** Tin chào hỏi, spam, tán gẫu cafe -> Bộ lọc Pre-filter loại bỏ ngay lập tức để tiết kiệm token và chống rác bản tin.
4. **Correction Path:** Nếu AI phân loại nhầm hoặc trích xuất sai, học viên bấm "Báo sai" để gắn cờ điều chỉnh.
