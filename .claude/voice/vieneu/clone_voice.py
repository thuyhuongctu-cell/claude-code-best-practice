#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clone_voice.py — Nhân bản giọng của bạn bằng VieNeu-TTS (chạy CỤC BỘ, không cần API key).

VieNeu-TTS là mô hình TTS tiếng Việt on-device, clone giọng từ 3–8 giây mẫu + transcript.
  Repo:  https://github.com/  (VieNeu-TTS)   ·  Model: HuggingFace pnnbao-ump/VieNeu-TTS-*

CÀI (trên máy bạn hoặc Colab — nơi truy cập được HuggingFace):
    pip install vieneu imageio-ffmpeg
    # (lần chạy đầu sẽ tự tải model GGUF + codec từ HuggingFace)

⚠️ Trong Claude Code on the web, HuggingFace thường bị chặn bởi network allowlist nên
   KHÔNG tải được model ở đó. Hãy chạy script này trên máy bạn, hoặc tạo môi trường với
   chính sách mạng cho phép huggingface.co.

DÙNG:
    # 1) Một câu:
    python3 clone_voice.py \
        --ref-audio ../samples/reference_0-8s.wav \
        --ref-text "ĐÚNG câu bạn nói trong đoạn mẫu" \
        --text "Xin chào, đây là giọng của tôi." \
        --out thu.wav

    # 2) Cả một bài giảng (đọc file JSON của lecture-toolkit):
    python3 clone_voice.py \
        --ref-audio ../samples/reference_0-8s.wav \
        --ref-text "ĐÚNG câu bạn nói trong đoạn mẫu" \
        --lecture ../../../coursework/EC1103/output/lecture/Chuong4.json
    # -> sinh wav cho từng slide + ghi Chuong4.cloned.json (mỗi slide có 'audio'),
    #    sau đó chạy build_lecture.py trên file .cloned.json là ra video, KHÔNG cần ElevenLabs.
"""

import sys
import json
import argparse
from pathlib import Path


def load_engine(mode, emotion):
    try:
        from vieneu import Vieneu
    except ImportError:
        sys.exit("Chưa cài 'vieneu'. Chạy: pip install vieneu imageio-ffmpeg "
                 "(trên máy truy cập được HuggingFace).")
    try:
        return Vieneu(mode=mode) if mode == "turbo" else Vieneu(emotion=emotion)
    except Exception as e:
        sys.exit(f"Không khởi tạo được VieNeu (thường do không tải được model từ HuggingFace): {e}")


def synth(tts, text, ref_audio, ref_text):
    """Trả về audio đã clone từ giọng tham chiếu."""
    return tts.infer(text=text, ref_audio=str(ref_audio), ref_text=ref_text)


def do_single(args):
    tts = load_engine(args.mode, args.emotion)
    text = Path(args.text_file).read_text(encoding="utf-8") if args.text_file else args.text
    audio = synth(tts, text, args.ref_audio, args.ref_text)
    tts.save(audio, args.out)
    print(f"💾 Đã lưu: {args.out}")


def do_lecture(args):
    tts = load_engine(args.mode, args.emotion)
    jpath = Path(args.lecture).resolve()
    data = json.loads(jpath.read_text(encoding="utf-8"))
    key = data.get("title", jpath.stem)
    audio_dir = jpath.parent / f"{key}_audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    for i, slide in enumerate(data["slides"], 1):
        narr = (slide.get("narration") or "").strip()
        if not narr:
            continue
        out = audio_dir / f"seg-{i:02d}.wav"
        print(f"  🦜 Slide {i:02d}: đang sinh giọng ({len(narr)} ký tự)…")
        audio = synth(tts, narr, args.ref_audio, args.ref_text)
        tts.save(audio, str(out))
        slide["audio"] = str(out)  # để build_lecture.py dùng audio có sẵn

    out_json = jpath.with_suffix(".cloned.json")
    out_json.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ Xong. Audio trong: {audio_dir}")
    print(f"   File kịch bản mới: {out_json}")
    print(f"   Bước cuối (ghép video):")
    print(f"   python3 .claude/voice/lecture/build_lecture.py --script {out_json}")


def main():
    ap = argparse.ArgumentParser(description="Clone giọng bằng VieNeu-TTS (cục bộ).")
    ap.add_argument("--ref-audio", required=True, help="File wav mẫu (3–8s, mono).")
    ap.add_argument("--ref-text", required=True, help="ĐÚNG câu nói trong đoạn mẫu (transcript).")
    ap.add_argument("--text", help="Câu cần đọc (chế độ 1 câu).")
    ap.add_argument("--text-file", help="File .txt cần đọc (thay cho --text).")
    ap.add_argument("--lecture", help="File JSON lecture-toolkit để sinh giọng cả bài.")
    ap.add_argument("--out", default="output.wav", help="File wav đầu ra (chế độ 1 câu).")
    ap.add_argument("--mode", default="standard", choices=["standard", "turbo"],
                    help="standard = chất lượng cao; turbo = nhanh, song ngữ.")
    ap.add_argument("--emotion", default="natural", choices=["natural", "storytelling"],
                    help="natural = tự nhiên; storytelling = kể chuyện (chỉ mode standard).")
    args = ap.parse_args()

    if not Path(args.ref_audio).exists():
        sys.exit(f"Không thấy file mẫu: {args.ref_audio}")
    if args.lecture:
        do_lecture(args)
    elif args.text or args.text_file:
        do_single(args)
    else:
        sys.exit("Cần --text/--text-file (1 câu) hoặc --lecture (cả bài).")


if __name__ == "__main__":
    main()
