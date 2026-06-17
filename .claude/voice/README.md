# 🎙️ Voice Assistant — Agent nói bằng giọng thật của bạn

Khung (scaffolding) để agent `voice-assistant` phát âm thanh **bằng giọng đã nhân bản của chính bạn**:

- **Thông báo bằng giọng nói** — agent phát clip giọng bạn khi xong việc, khi xin quyền, khi lỗi.
- **Trợ lý cá nhân** — một subagent đại diện cho bạn (xem `.claude/agents/voice-assistant.md`).
- **Đọc to nội dung** — đọc câu trả lời/tóm tắt bằng giọng bạn (chế độ TTS động).

> ⚠️ **Quan trọng về quyền riêng tư:** Giọng nói thật của bạn (file trong `clips/`, `samples/`)
> được `.gitignore` chặn lại — chúng **chỉ nằm ở máy bạn**, không bao giờ bị đẩy lên GitHub.
> Repo chỉ chứa *khung*: script, config mẫu, và README này.

---

## Cách hoạt động (kiến trúc)

```
Sự kiện hook (Stop / Notification / PermissionRequest / PostToolUseFailure)
        │
        ▼
.claude/agents/voice-assistant.md  (hooks trong frontmatter)
        │  gọi
        ▼
.claude/hooks/scripts/speak.py
        │
        ├─ Chế độ clip:  đọc tên sự kiện từ stdin → phát clips/<tên>.wav|mp3
        └─ Chế độ --say "text":  gọi TTS ElevenLabs (nếu có API key) → phát giọng bạn
```

`speak.py` **luôn thoát mã 0** — nếu thiếu file/clip/key thì im lặng bỏ qua, không bao giờ làm gián đoạn Claude.

---

## Phần 1 — Nhân bản giọng của bạn (làm 1 lần)

Cách repo này tạo các giọng mẫu (Samara X) là dùng **elevenlabs.io**. Bạn làm tương tự với giọng mình:

1. Tạo tài khoản tại https://elevenlabs.io/
2. Vào **Voices → Add a new voice → Instant Voice Cloning**.
3. Tải lên **mẫu giọng của bạn** (file ghi âm bạn đã gửi, hoặc ghi 1–2 phút nói rõ ràng).
4. Đặt tên giọng, đồng ý điều khoản, bấm **Add Voice**.
5. Mở giọng vừa tạo, copy **Voice ID** (chuỗi như `21m00Tcm4TlvDq8ikWAM`).

> 🔒 Bước này gửi mẫu giọng của bạn lên ElevenLabs (dịch vụ bên thứ ba). Đây là bước duy nhất giọng bạn rời khỏi máy, và do **chính bạn** thực hiện.

---

## Phần 2 — Tạo các clip thông báo (giọng bạn)

Trên trang giọng vừa clone, dùng ô **Text to Speech**, lần lượt gõ từng câu dưới đây, tải file `.mp3`
về và lưu vào `.claude/voice/clips/` đúng tên file:

| Sự kiện hook         | Tên file clip          | Câu gợi ý (tiếng Việt)                  |
| -------------------- | ---------------------- | --------------------------------------- |
| `Stop`               | `clips/done.mp3`       | "Mình đã làm xong rồi nhé."             |
| `SubagentStop`       | `clips/subagent_done.mp3` | "Tác vụ phụ đã hoàn tất."            |
| `Notification`       | `clips/notification.mp3` | "Bạn ơi, có thông báo này."           |
| `PermissionRequest`  | `clips/permission.mp3` | "Mình cần bạn cấp quyền nhé."           |
| `PostToolUseFailure` | `clips/error.mp3`      | "Có lỗi xảy ra rồi, kiểm tra giúp mình."|
| `SessionStart`       | `clips/hello.mp3`      | "Chào bạn, mình sẵn sàng làm việc."     |

> 💡 Có thể đổi câu/tên file tùy ý — chỉ cần khớp cột "Tên file clip", hoặc sửa ánh xạ
> trong `voice-config.json → event_clips`. Định dạng `.wav` được ưu tiên (Linux `paplay`
> không phát được `.mp3`; máy macOS/Windows thì `.mp3` vẫn chạy).

---

## Phần 3 — (Tùy chọn) Bật "đọc to" động

Để agent đọc to **bất kỳ câu nào** (không chỉ clip có sẵn), cần API key:

1. Lấy **API key** tại ElevenLabs → *Profile → API Keys*.
2. Khai báo qua biến môi trường (khuyến nghị — không lộ key vào git):
   ```bash
   export ELEVENLABS_API_KEY="sk_..."
   export ELEVENLABS_VOICE_ID="<voice_id_cua_ban>"
   ```
   *(hoặc* điền `voice_id` vào `voice-config.json`; **đừng** commit `api_key` thật — dùng
   `voice-config.local.json` đã được gitignore nếu muốn lưu ra file.)*
3. Thử:
   ```bash
   python3 .claude/hooks/scripts/speak.py --say "Xin chào, đây là giọng của tôi."
   ```
   Có key → nghe thấy giọng bạn. Chưa có key → script chỉ in text ra (không lỗi).

---

## Phần 4 — Kiểm tra

```bash
# Phát thử clip "done" (cần đã có clips/done.wav hoặc .mp3)
python3 .claude/hooks/scripts/speak.py --event Stop

# Hoặc mô phỏng đúng cách hook gọi (truyền JSON qua stdin):
echo '{"hook_event_name":"Stop"}' | python3 .claude/hooks/scripts/speak.py
```

Sau đó gọi agent trong Claude Code:
```
> Dùng agent voice-assistant để tóm tắt và đọc to.
```

Khi agent kết thúc (`Stop`), hook sẽ phát `clips/done` — bằng giọng của bạn. 🎉
