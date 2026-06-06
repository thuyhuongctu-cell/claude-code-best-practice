#!/usr/bin/env python3
"""
Lecture Builder — bài giảng bằng giọng nhân bản của bạn
=======================================================
Biến một kịch bản JSON (mỗi slide một đoạn lời) thành:
  • Video MP4: ảnh slide + giọng đọc của bạn + phụ đề SRT  (--mode video)
  • Audio MP3: đọc toàn bộ bài giảng theo từng phần         (--mode audio)
  • Cả hai                                                  (--mode both, mặc định)

Tái dùng phần tổng hợp giọng ElevenLabs từ .claude/hooks/scripts/speak.py
(cùng API key / voice_id trong .claude/voice/voice-config.json).

Phụ thuộc khi RENDER (chạy trên máy bạn, không bắt buộc trong môi trường remote):
  • ffmpeg, ffprobe   (ghép ảnh+audio, đo thời lượng, nối video)
  • pdftoppm (poppler) — chỉ khi nguồn slide là PDF cần tách trang
  • Biến môi trường ELEVENLABS_API_KEY + ELEVENLABS_VOICE_ID (hoặc trong voice-config.json)

Dùng thử cấu trúc mà KHÔNG cần render:
  python3 build_lecture.py --script lecture.example.json --check
"""

import sys
import json
import shutil
import argparse
import subprocess
import importlib.util
from pathlib import Path

# ---- Đường dẫn & nạp lại hàm tổng hợp giọng từ speak.py ----------------------
THIS_DIR = Path(__file__).resolve().parent          # .claude/voice/lecture
VOICE_DIR = THIS_DIR.parent                          # .claude/voice
PROJECT_ROOT = VOICE_DIR.parents[1]                  # repo root
SPEAK_PY = PROJECT_ROOT / ".claude" / "hooks" / "scripts" / "speak.py"


def _load_speak():
    """Nạp speak.py như một module để tái dùng synth + load_config."""
    spec = importlib.util.spec_from_file_location("speak", SPEAK_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---- Tiện ích phụ thuộc ------------------------------------------------------
def have(binary):
    return shutil.which(binary) is not None


def run(cmd):
    """Chạy lệnh, ném lỗi kèm stderr nếu thất bại."""
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Lệnh thất bại: {' '.join(cmd)}\n{proc.stderr.strip()}")
    return proc.stdout


def audio_duration(path):
    """Đo thời lượng audio (giây) bằng ffprobe."""
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=noprint_wrappers=1:nokey=1", str(path)])
    return float(out.strip())


def srt_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# ---- Nguồn slide: PDF -> PNG -------------------------------------------------
def ensure_slides_from_pdf(pdf_path, out_dir):
    """Tách PDF thành slides/page-1.png, page-2.png, ... và trả danh sách."""
    out_dir.mkdir(parents=True, exist_ok=True)
    if not have("pdftoppm"):
        raise RuntimeError("Cần 'pdftoppm' (gói poppler-utils) để tách PDF. "
                           "Cài: macOS `brew install poppler`, Ubuntu `apt install poppler-utils`.")
    run(["pdftoppm", "-png", "-r", "150", str(pdf_path), str(out_dir / "page")])
    return sorted(out_dir.glob("page-*.png"))


# ---- Tải & chuẩn hoá kịch bản ------------------------------------------------
def load_script(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if "slides" not in data or not isinstance(data["slides"], list) or not data["slides"]:
        raise ValueError("Kịch bản phải có mảng 'slides' không rỗng.")
    return data


def resolve_slide_images(data, script_path, work_dir):
    """Trả về danh sách đường dẫn ảnh, mỗi phần tử ứng với một slide.

    Mỗi slide có thể khai báo 'image' (PNG/JPG) HOẶC dùng PDF chung ('pdf' ở cấp
    gốc) ánh xạ theo thứ tự. Đường dẫn tương đối tính từ thư mục chứa kịch bản.
    """
    base = Path(script_path).resolve().parent
    slides = data["slides"]

    # Trường hợp dùng 1 PDF chung -> tách ra ảnh theo trang
    if data.get("pdf"):
        pdf_path = (base / data["pdf"]).resolve()
        if not pdf_path.exists():
            raise FileNotFoundError(f"Không thấy PDF: {pdf_path}")
        pages = ensure_slides_from_pdf(pdf_path, work_dir / "slides")
        if len(pages) < len(slides):
            raise ValueError(f"PDF có {len(pages)} trang nhưng kịch bản có {len(slides)} slide.")
        return [pages[i] for i in range(len(slides))]

    # Ngược lại: mỗi slide tự khai báo 'image'
    images = []
    for i, s in enumerate(slides, 1):
        if not s.get("image"):
            raise ValueError(f"Slide #{i} thiếu 'image' (hoặc khai báo 'pdf' ở cấp gốc).")
        p = (base / s["image"]).resolve()
        if not p.exists():
            raise FileNotFoundError(f"Slide #{i}: không thấy ảnh {p}")
        images.append(p)
    return images


# ---- Tổng hợp giọng cho từng slide ------------------------------------------
def synth_segments(data, script_path, audio_dir, speak, cfg):
    """Tạo audio_dir/seg-NN.mp3 cho mỗi slide. Trả về danh sách đường dẫn."""
    base = Path(script_path).resolve().parent
    audio_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, s in enumerate(data["slides"], 1):
        target = audio_dir / f"seg-{i:02d}.mp3"

        # Cho phép tái dùng audio có sẵn (đã thu/đã sinh trước đó)
        if s.get("audio"):
            src = (base / s["audio"]).resolve()
            if not src.exists():
                raise FileNotFoundError(f"Slide #{i}: không thấy audio {src}")
            shutil.copyfile(src, target)
            paths.append(target)
            continue

        text = (s.get("narration") or "").strip()
        if not text:
            raise ValueError(f"Slide #{i} thiếu 'narration' (và không có 'audio').")

        tmp = speak.synthesize_elevenlabs(text, cfg)
        if not tmp:
            raise RuntimeError(
                f"Slide #{i}: tổng hợp giọng thất bại. Hãy đặt ELEVENLABS_API_KEY và "
                f"ELEVENLABS_VOICE_ID (hoặc điền vào voice-config.json)."
            )
        shutil.move(tmp, target)
        paths.append(target)
        print(f"  ✓ Slide {i:02d}: đã sinh giọng ({len(text)} ký tự)")
    return paths


# ---- Xuất AUDIO (nối các đoạn) -----------------------------------------------
def build_audio(seg_audio, out_path):
    list_file = out_path.parent / "_audio_concat.txt"
    list_file.write_text("".join(f"file '{p.resolve()}'\n" for p in seg_audio), encoding="utf-8")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
         "-c:a", "libmp3lame", "-q:a", "2", str(out_path)])
    list_file.unlink(missing_ok=True)
    print(f"  ✓ Audio: {out_path}")


# ---- Xuất VIDEO (ảnh + audio mỗi slide, rồi nối) -----------------------------
def build_video(images, seg_audio, out_path, resolution, work_dir):
    w, h = resolution.split("x")
    seg_dir = work_dir / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)
    seg_videos, srt_lines, t = [], [], 0.0
    # scale + pad để mọi ảnh vừa khung, nền đen, không méo
    vf = (f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
          f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p")

    for i, (img, aud) in enumerate(zip(images, seg_audio), 1):
        dur = audio_duration(aud)
        seg_mp4 = seg_dir / f"seg-{i:02d}.mp4"
        run(["ffmpeg", "-y", "-loop", "1", "-i", str(img), "-i", str(aud),
             "-vf", vf, "-c:v", "libx264", "-tune", "stillimage", "-r", "25",
             "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
             "-shortest", str(seg_mp4)])
        seg_videos.append(seg_mp4)
        srt_lines.append(f"{i}\n{srt_timestamp(t)} --> {srt_timestamp(t + dur)}\n"
                         f"{_subtitle_text(i)}\n")
        t += dur
        print(f"  ✓ Slide {i:02d}: video {dur:.1f}s")

    # Nối các đoạn video
    list_file = work_dir / "_video_concat.txt"
    list_file.write_text("".join(f"file '{p.resolve()}'\n" for p in seg_videos), encoding="utf-8")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
         "-c", "copy", str(out_path)])
    list_file.unlink(missing_ok=True)

    # Phụ đề SRT đi kèm (đặt cạnh video)
    srt_path = out_path.with_suffix(".srt")
    srt_path.write_text("\n".join(srt_lines), encoding="utf-8")
    print(f"  ✓ Video: {out_path}")
    print(f"  ✓ Phụ đề: {srt_path}")


# Bộ nhớ phụ đề điền bởi main() trước khi build_video chạy
_SUBTITLES = {}
def _subtitle_text(i):
    return _SUBTITLES.get(i, "")


# ---- Chế độ kiểm tra (không render) -----------------------------------------
def check(data, script_path):
    print("== KIỂM TRA KỊCH BẢN ==")
    print(f"Tiêu đề : {data.get('title', '(không có)')}")
    print(f"Số slide: {len(data['slides'])}")
    base = Path(script_path).resolve().parent
    problems = []
    for i, s in enumerate(data["slides"], 1):
        has_text = bool((s.get("narration") or "").strip()) or bool(s.get("audio"))
        if not has_text:
            problems.append(f"Slide #{i}: thiếu 'narration' và 'audio'")
        if not data.get("pdf") and not s.get("image"):
            problems.append(f"Slide #{i}: thiếu 'image' (và không có 'pdf' cấp gốc)")
        if s.get("image"):
            p = (base / s["image"])
            if not p.exists():
                problems.append(f"Slide #{i}: ảnh không tồn tại — {p}")
    if data.get("pdf"):
        p = base / data["pdf"]
        if not p.exists():
            problems.append(f"PDF không tồn tại — {p}")

    print("\n== PHỤ THUỘC ==")
    for b in ("ffmpeg", "ffprobe", "pdftoppm"):
        print(f"  {'✓' if have(b) else '✗'} {b}")
    speak = _load_speak()
    cfg = speak.load_config()
    tts = cfg.get("tts", {})
    import os
    key = os.environ.get("ELEVENLABS_API_KEY") or tts.get("api_key")
    vid = os.environ.get("ELEVENLABS_VOICE_ID") or tts.get("voice_id", "")
    print(f"  {'✓' if key else '✗'} ELEVENLABS_API_KEY")
    print(f"  {'✓' if vid and not vid.startswith('<') else '✗'} voice_id")

    print("\n== KẾT QUẢ ==")
    if problems:
        print("Cần sửa:")
        for p in problems:
            print(f"  ✗ {p}")
        return 1
    print("  ✓ Kịch bản hợp lệ. Đặt API key + voice_id và cài ffmpeg để render.")
    return 0


# ---- main -------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Tạo video/audio bài giảng bằng giọng nhân bản.")
    ap.add_argument("--script", required=True, help="Đường dẫn file kịch bản JSON.")
    ap.add_argument("--mode", choices=["audio", "video", "both"], default="both")
    ap.add_argument("--out", default=None, help="Thư mục xuất (mặc định: ./output cạnh kịch bản).")
    ap.add_argument("--resolution", default=None, help="Độ phân giải video, vd 1920x1080.")
    ap.add_argument("--check", action="store_true", help="Chỉ kiểm tra kịch bản & phụ thuộc, không render.")
    args = ap.parse_args()

    data = load_script(args.script)
    if args.check:
        sys.exit(check(data, args.script))

    # Chuẩn bị thư mục làm việc & xuất
    base = Path(args.script).resolve().parent
    out_dir = Path(args.out).resolve() if args.out else (base / "output")
    out_dir.mkdir(parents=True, exist_ok=True)
    work_dir = out_dir / "_work"
    work_dir.mkdir(parents=True, exist_ok=True)
    title = data.get("title", "lecture").replace("/", "-")
    resolution = args.resolution or data.get("resolution", "1920x1080")

    # Kiểm tra phụ thuộc theo chế độ
    need_video = args.mode in ("video", "both")
    if need_video and (not have("ffmpeg") or not have("ffprobe")):
        sys.exit("Cần ffmpeg + ffprobe để render video. Cài rồi chạy lại "
                 "(hoặc dùng --mode audio, hoặc --check).")
    if args.mode == "audio" and not have("ffmpeg"):
        sys.exit("Cần ffmpeg để nối audio. Cài rồi chạy lại (hoặc --check).")

    speak = _load_speak()
    cfg = speak.load_config()

    # 1) Tổng hợp giọng cho từng slide
    print("[1/3] Tổng hợp giọng cho từng slide…")
    seg_audio = synth_segments(data, args.script, work_dir / "audio", speak, cfg)

    # 2) Audio gộp
    if args.mode in ("audio", "both"):
        print("[2/3] Xuất audio bài giảng…")
        build_audio(seg_audio, out_dir / f"{title}.mp3")

    # 3) Video
    if need_video:
        print("[3/3] Xuất video bài giảng…")
        images = resolve_slide_images(data, args.script, work_dir)
        # nạp text phụ đề
        for i, s in enumerate(data["slides"], 1):
            _SUBTITLES[i] = (s.get("subtitle") or s.get("narration") or "").strip()
        build_video(images, seg_audio, out_dir / f"{title}.mp4", resolution, work_dir)

    print(f"\nHoàn tất. Kết quả trong: {out_dir}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.exit(f"Lỗi: {e}")
