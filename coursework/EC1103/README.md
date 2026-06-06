# HLS EC1103 — Phần GV Đỗ Thùy Hương

Học liệu số (HLS) cho học phần **EC1103 – Kỹ năng giao tiếp và soạn thảo văn bản** (Đào tạo từ xa).
Phần được phân công (theo trao đổi nhóm trên Zalo): **Chương 4 + Bài thực hành 2 & 3**.

| Đơn vị | Nội dung | Số slide |
| --- | --- | --- |
| **Chương 4** | Soạn thảo và trình bày văn bản (4.1→4.4) | 12 |
| **Bài 2 (TH)** | Soạn thảo văn bản hành chính (Quyết định, Tờ trình, Công văn, Biên bản, Báo cáo) | 13 |
| **Bài 3 (TH)** | Soạn thảo văn bản thương mại (Thư tín, Báo giá, Hợp đồng/nghiệm thu/thanh lý) | 11 |

## Cấu trúc thư mục

```
coursework/EC1103/
├── content.py            # Toàn bộ nội dung + lời thuyết minh (sửa ở đây)
├── build.py              # Bộ sinh: PPTX + kịch bản Word + JSON quay video
├── _assets/template.pptx # Template FEL Đào tạo từ xa (giữ nguyên nền)
└── output/
    ├── Chuong4.pptx / Bai2.pptx / Bai3.pptx        # Slide hoàn chỉnh
    ├── *_kichban.docx                               # Kịch bản thuyết minh, chia theo clip 10–15'
    └── lecture/*.json                               # Dùng cho lecture-toolkit (quay video)
```

## Cách dùng

### 1. Sửa nội dung & sinh lại slide
Mọi nội dung nằm trong `content.py` (bullet trên slide + lời thuyết minh). Sửa xong chạy:
```bash
cd coursework/EC1103
pip install python-pptx python-docx     # nếu chưa có
python3 build.py
```
Bộ sinh **giữ nguyên 100% nền/bố cục template** (chỉ thay chữ), tự đánh số trang và chia clip.

### 2. Quay video bài giảng bằng giọng của chị
Bộ slide đã nối sẵn với **lecture-toolkit** (`.claude/voice/lecture/`):
```bash
# B1: Xuất slide ra ảnh PNG (PowerPoint: File → Export → PNG), đặt vào
#     .claude/voice/lecture/slides/Chuong4-01.png, -02.png, ...
# B2: Đặt giọng đã clone (xem .claude/voice/README.md), rồi:
cd .claude/voice/lecture
python3 build_lecture.py --script <đường_dẫn>/output/lecture/Chuong4.json
```
→ Xuất `Chuong4.mp4` (slide + giọng của chị + phụ đề) và `Chuong4.mp3`.

## Ghi chú biên soạn

- Nội dung thể thức bám **Nghị định 30/2020/NĐ-CP** về công tác văn thư (9 thành phần thể thức).
- Mỗi clip mục tiêu **10–15 phút**; kịch bản `.docx` đã tự chia clip theo độ dài lời thuyết minh.
- Nền/tiêu đề thống nhất theo template chung của nhóm (phong cách môn Khởi nghiệp).
- **Cần rà soát trước khi nghiệm thu (dự kiến 20/9):** đối chiếu lại với ĐCCT mới nhất, bổ sung
  ảnh minh hoạ mẫu văn bản thật vào các slide thân bài, và thống nhất số trang với các chương của nhóm.
