# 🎬 Lecture Toolkit — video bài giảng bằng giọng nhân bản của bạn

Biến một **kịch bản JSON** (mỗi slide một đoạn lời) thành:
- **Video MP4**: ảnh slide + giọng đọc của bạn + phụ đề `.srt`
- **Audio MP3**: bản đọc cả bài giảng

Toolkit này tái dùng giọng đã clone ở `../README.md` (cùng `voice-config.json`).

---

## Yêu cầu khi render (chạy trên máy bạn)

| Công cụ | Dùng để | Cài đặt |
| --- | --- | --- |
| `ffmpeg` + `ffprobe` | ghép ảnh+giọng, nối video | macOS `brew install ffmpeg` · Ubuntu `apt install ffmpeg` · Windows: tải tại ffmpeg.org |
| `pdftoppm` *(tuỳ chọn)* | tách PDF thành ảnh trang | macOS `brew install poppler` · Ubuntu `apt install poppler-utils` |
| `ELEVENLABS_API_KEY` + `ELEVENLABS_VOICE_ID` | sinh giọng của bạn | xem `../README.md` phần 3 |

> Môi trường Claude Code trên web **không có** các công cụ này — hãy chạy toolkit **trên máy bạn**.
> Tại đây bạn vẫn dùng được `--check` để kiểm tra kịch bản trước.

---

## Quy trình 4 bước

### 1. Chuẩn bị slide
- **Ảnh có sẵn:** đặt `slides/01.png`, `02.png`, … cạnh kịch bản.
- **PowerPoint:** xuất ra ảnh — *File → Export → PNG* (mỗi slide một ảnh), hoặc lưu PDF rồi dùng cách dưới.
- **PDF:** đặt `"pdf": "bai-giang.pdf"` ở cấp gốc kịch bản; toolkit tự tách trang (cần `pdftoppm`).

### 2. Viết kịch bản
Sao chép `lecture.example.json` rồi sửa. Mỗi slide:
```json
{ "image": "slides/01.png", "narration": "Lời thuyết minh cho slide này.", "subtitle": "Phụ đề tuỳ chọn" }
```
- `image` — ảnh slide (bỏ qua nếu dùng `"pdf"` cấp gốc, ánh xạ theo thứ tự).
- `narration` — lời đọc (sinh bằng giọng bạn). Thay bằng `"audio": "narration/seg-03.mp3"` nếu đã thu sẵn.
- `subtitle` — chữ hiện trong `.srt` (mặc định lấy theo `narration`).

### 3. Kiểm tra (không cần ffmpeg/key)
```bash
python3 build_lecture.py --script lecture.example.json --check
```
Báo: slide nào thiếu ảnh/lời, công cụ nào chưa cài, key đã có chưa.

### 4. Render
```bash
# Cả video + audio (mặc định)
python3 build_lecture.py --script lecture.example.json

# Chỉ audio (không cần ảnh đẹp)
python3 build_lecture.py --script lecture.example.json --mode audio

# Chỉ video, đổi độ phân giải / thư mục xuất
python3 build_lecture.py --script lecture.example.json --mode video --resolution 1280x720 --out ./output
```
Kết quả mặc định nằm trong `output/`:
- `<title>.mp4`, `<title>.srt`, `<title>.mp3`

---

## Mẹo cho giảng viên

- **Chia nhỏ theo slide** giúp giọng đọc tự nhiên và dễ sửa từng đoạn (chỉ sinh lại slide cần đổi).
- Giữ mỗi đoạn `narration` **1–4 câu**; câu quá dài làm phụ đề khó đọc.
- Muốn nhạc nền/đầu-cuối, dựng video xong rồi ghép thêm bằng ffmpeg hoặc trình dựng phim.
- File đầu ra (`output/`, `slides/`, `*.mp4/.mp3/.srt`) đã được **gitignore** — không bị đẩy lên GitHub.

---

## Avatar nói chuyện (talking-head)?

Toolkit này làm **slide + thuyết minh**, không nhập miệng avatar. Nếu cần gương mặt AI nói theo
giọng, dùng dịch vụ chuyên biệt (HeyGen, D-ID, Synthesia): tải video/audio giọng bạn lên đó.
Lưu ý: trả phí và **gửi hình ảnh/giọng ra dịch vụ bên thứ ba** — cân nhắc quyền riêng tư.
