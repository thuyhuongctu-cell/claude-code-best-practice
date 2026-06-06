# 🦜 VieNeu-TTS — nhân bản giọng CỤC BỘ (không cần API key)

Giải pháp clone giọng tiếng Việt **chạy offline trên CPU**, thay cho ElevenLabs (không cần khóa API,
không gửi giọng lên dịch vụ ngoài). Dùng [VieNeu-TTS](https://huggingface.co/pnnbao-ump) —
mô hình on-device, clone giọng chỉ từ **3–8 giây mẫu + transcript**.

## ⚠️ Vì sao không chạy được trong Claude Code on the web?

Mô hình VieNeu tải trọng số từ **HuggingFace**, nhưng môi trường web bị giới hạn bởi
**network allowlist** (PyPI/GitHub được phép, HuggingFace bị chặn — `Host not in allowlist`).
Do đó hãy chạy theo một trong hai cách:

1. **Trên máy của bạn / Google Colab** (HF truy cập được) — khuyến nghị.
2. **Tạo môi trường web với chính sách mạng cho phép `huggingface.co`** — xem
   https://code.claude.com/docs/en/claude-code-on-the-web — rồi mình clone ngay tại đây.

## Cài đặt (máy bạn / Colab)

```bash
pip install vieneu imageio-ffmpeg
# Lần chạy đầu sẽ tự tải model GGUF + codec (~vài trăm MB) từ HuggingFace.
```

## Chuẩn bị mẫu giọng

Đã có sẵn (mình tạo từ bản ghi `Ghi âm của tôi 2.m4a` của chị, lưu cục bộ — gitignore):
- `.claude/voice/samples/Ghi_am_2_full.wav` — bản đầy đủ 61 giây (24 kHz, mono)
- `.claude/voice/samples/reference_0-8s.wav` — đoạn 8 giây đầu để clone

> 📝 **Cần transcript:** VieNeu cần *đúng câu bạn nói* trong đoạn mẫu (`--ref-text`).
> Hãy nghe lại `reference_0-8s.wav` và gõ chính xác lời thoại trong 8 giây đó (hoặc cắt một
> đoạn 3–8 giây rõ tiếng khác và ghi lại transcript tương ứng).

## Dùng

### 1) Đọc một câu bằng giọng của bạn
```bash
cd .claude/voice/vieneu
python3 clone_voice.py \
  --ref-audio ../samples/reference_0-8s.wav \
  --ref-text "ĐÚNG câu bạn nói trong đoạn mẫu" \
  --text "Xin chào, đây là giọng của tôi." \
  --out thu.wav
```

### 2) Sinh giọng cho cả bài giảng → ghép video
```bash
python3 clone_voice.py \
  --ref-audio ../samples/reference_0-8s.wav \
  --ref-text "ĐÚNG câu bạn nói trong đoạn mẫu" \
  --lecture ../../../coursework/EC1103/output/lecture/Chuong4.json
# -> sinh wav cho từng slide + tạo Chuong4.cloned.json
python3 ../lecture/build_lecture.py --script ../../../coursework/EC1103/output/lecture/Chuong4.cloned.json
# -> Chuong4.mp4 (slide + GIỌNG CỦA CHỊ + phụ đề) — toàn bộ offline, không API key.
```

## Tham số

| Cờ | Ý nghĩa |
| --- | --- |
| `--ref-audio` | File wav mẫu (3–8s, mono) |
| `--ref-text`  | Transcript đúng của đoạn mẫu (bắt buộc) |
| `--text` / `--text-file` | Câu / file cần đọc (chế độ 1 câu) |
| `--lecture`   | File JSON bài giảng để sinh giọng hàng loạt |
| `--mode`      | `standard` (chất lượng cao, mặc định) hoặc `turbo` (nhanh, song ngữ Anh–Việt) |
| `--emotion`   | `natural` hoặc `storytelling` (chỉ mode standard) |

## So với ElevenLabs (trong `../README.md`)

| | VieNeu (cục bộ) | ElevenLabs (đám mây) |
| --- | --- | --- |
| API key | ❌ không cần | ✅ cần |
| Giọng rời máy | ❌ không | ⚠️ có (upload lên dịch vụ) |
| Tiếng Việt | ⭐ tối ưu | tốt |
| Cần GPU? | Không (CPU GGUF được) | Không |
| Chạy trên web sandbox | ❌ (HF bị chặn) | ⚠️ (cần key + mạng) |

→ Khuyến nghị **VieNeu** cho bài giảng tiếng Việt: riêng tư, miễn phí, không khóa.
