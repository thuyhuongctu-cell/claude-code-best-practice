# -*- coding: utf-8 -*-
"""
Bộ sinh Học liệu số (HLS) cho EC1103 — phần GV Đỗ Thùy Hương (Chương 4, Bài 2, Bài 3).

Đầu ra (thư mục output/):
  • <key>.pptx        — bộ slide giữ nguyên nền/template FEL Đào tạo từ xa
  • <key>_kichban.docx — kịch bản thuyết minh, chia theo clip 10–15 phút
  • lecture/<key>.json — file cho .claude/voice/lecture/build_lecture.py (quay video bằng giọng clone)

Chạy:  python3 build.py
Phụ thuộc: python-pptx, python-docx  (pip install python-pptx python-docx)
"""

import copy
import json
from pathlib import Path

from pptx import Presentation
from pptx.oxml.ns import qn

import content as C

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "_assets" / "template.pptx"
OUT = HERE / "output"
LEC = OUT / "lecture"
WPM = 140  # tốc độ đọc ước lượng (từ/phút) để chia clip

# Chỉ số shape chứa "page number" trên từng loại slide template (0-based)
PAGENUM = {0: 19, 1: 9, 2: 13, 6: 12, 7: 11, 8: 12, 9: 11}


# ---------- helpers thao tác slide / text -----------------------------------
def duplicate_slide(prs, index):
    """Nhân bản slide template tại index, thêm vào cuối; copy cả quan hệ ảnh."""
    src = prs.slides[index]
    new = prs.slides.add_slide(src.slide_layout)
    for sh in list(new.shapes):
        sh._element.getparent().remove(sh._element)
    for sh in src.shapes:
        new.shapes._spTree.append(copy.deepcopy(sh._element))
    for rid, rel in src.part.rels.items():
        if "notesSlide" in rel.reltype:
            continue
        if rel.is_external:
            new.part.rels.get_or_add_ext_rel(rel.reltype, rel.target_ref)
        else:
            new.part.relate_to(rel.target_part, rel.reltype)
    return new


def _ensure_run(p0):
    """Trả về run đầu của paragraph; nếu rỗng thì tạo run kế thừa định dạng endParaRPr."""
    if p0.runs:
        run = p0.runs[0]
        for r in p0.runs[1:]:
            r._r.getparent().remove(r._r)
        return run
    run = p0.add_run()
    end = p0._p.find(qn("a:endParaRPr"))
    if end is not None:
        rPr = run._r.get_or_add_rPr()
        for k, v in end.attrib.items():
            rPr.set(k, v)
        for child in list(end):
            rPr.append(copy.deepcopy(child))
    return run


def set_text(shape, text):
    """Đặt `text` vào shape, giữ định dạng run đầu; xoá các run/paragraph thừa."""
    tf = shape.text_frame
    p0 = tf.paragraphs[0]
    run = _ensure_run(p0)
    run.text = text
    for p in tf.paragraphs[1:]:
        p._p.getparent().remove(p._p)


def apply(slide, mapping):
    """mapping: {shape_index: text}. Bỏ qua None (để xoá nội dung placeholder)."""
    shapes = list(slide.shapes)
    for idx, text in mapping.items():
        if idx >= len(shapes):
            continue
        sh = shapes[idx]
        if not sh.has_text_frame:
            continue
        set_text(sh, text if text is not None else "")


# ---------- xây danh sách slide cho 1 deck ----------------------------------
def build_slide_specs(deck):
    """Trả về list (tpl_index, mapping, narration, slide_title)."""
    unit = {"Chuong4": "CHƯƠNG 4", "Bai2": "BÀI 2", "Bai3": "BÀI 3"}[deck["key"]]
    specs = []

    # 1) Trang bìa (tpl 0): shape 15 = phụ đề (tên chương/bài)
    specs.append((0, {15: deck["title"]}, deck["narr_title"], "Trang bìa"))

    # 2) Mục tiêu (tpl 1): title 11; mục tiêu 12,13,14,16
    objs = deck["objectives"]
    m = {11: f"MỤC TIÊU {unit}"}
    for shp, txt in zip([12, 13, 14, 16], objs):
        m[shp] = txt
    specs.append((1, m, deck["narr_objectives"], "Mục tiêu"))

    # 3) Nội dung (tpl 2): title 15; 5 slot item 17,22,23,24,25; số 16,18,19,20,21
    item_slots = [17, 22, 23, 24, 25]
    num_slots = [16, 18, 19, 20, 21]
    m = {15: f"NỘI DUNG {unit}"}
    for i, slot in enumerate(item_slots):
        m[slot] = deck["contents"][i] if i < len(deck["contents"]) else ""
        if i >= len(deck["contents"]):
            m[num_slots[i]] = ""  # ẩn số thứ tự dư
    specs.append((2, m, deck["narr_contents"], "Nội dung"))

    # 4) Thân bài: mỗi section dùng tpl 9 (title 13; ý 14-17; sidebar 19-22)
    for sec in deck["sections"]:
        m = {13: sec["title"]}
        for shp, txt in zip([14, 15, 16, 17], sec["points"] + [""] * 4):
            m[shp] = txt
        for shp, txt in zip([19, 20, 21, 22], sec["sidebar"] + [""] * 4):
            m[shp] = txt
        specs.append((9, m, sec["narration"], sec["title"]))

    # 5) Case study (tpl 6): desc 22; câu hỏi 17,19,21
    cs = deck["case"]
    m = {22: cs["desc"]}
    for shp, q in zip([17, 19, 21], cs["questions"]):
        m[shp] = q
    specs.append((6, m, cs["narration"], "Tình huống thực tiễn"))

    # 6) Thảo luận (tpl 7): câu hỏi 13
    specs.append((7, {13: deck["discussion"]["q"]}, deck["discussion"]["narration"], "Thảo luận"))

    # 7) Bài tập (tpl 8): 16 nội dung, 18 yêu cầu, 20 hướng dẫn, 22 thời gian
    ex = deck["exercise"]
    specs.append((8, {16: ex["noidung"], 18: ex["yeucau"], 20: ex["huongdan"], 22: ex["thoigian"]},
                  ex["narration"], "Bài tập vận dụng"))

    # 8) Tổng kết (tpl 9): title 13; ý 14-17; sidebar 19-22
    sm = deck["summary"]
    m = {13: "TỔNG KẾT NỘI DUNG"}
    for shp, txt in zip([14, 15, 16, 17], sm["points"] + [""] * 4):
        m[shp] = txt
    for shp, txt in zip([19, 20, 21, 22], sm["sidebar"] + [""] * 4):
        m[shp] = txt
    specs.append((9, m, sm["narration"], "Tổng kết"))

    # 9) Cảm ơn (tpl 10): giữ nguyên
    specs.append((10, {}, "Xin cảm ơn các anh chị đã theo dõi. Hẹn gặp lại ở nội dung tiếp theo.", "Cảm ơn"))
    return specs


def build_pptx(deck):
    prs = Presentation(str(TEMPLATE))
    n_template = len(prs.slides._sldIdLst)
    specs = build_slide_specs(deck)

    page = 1
    for tpl_idx, mapping, _narr, _title in specs:
        slide = duplicate_slide(prs, tpl_idx)
        apply(slide, mapping)
        # đánh số trang chạy
        if tpl_idx in PAGENUM:
            shapes = list(slide.shapes)
            pidx = PAGENUM[tpl_idx]
            if pidx < len(shapes) and shapes[pidx].has_text_frame:
                set_text(shapes[pidx], str(page))
        page += 1

    # xoá 11 slide template gốc (đứng đầu)
    sldIdLst = prs.slides._sldIdLst
    for sldId in list(sldIdLst)[:n_template]:
        sldIdLst.remove(sldId)

    OUT.mkdir(parents=True, exist_ok=True)
    out_path = OUT / f"{deck['key']}.pptx"
    prs.save(str(out_path))
    return out_path, specs


# ---------- kịch bản Word (chia clip 10–15 phút) ----------------------------
def build_docx(deck, specs):
    from docx import Document
    from docx.shared import Pt

    doc = Document()
    doc.add_heading(f"KỊCH BẢN THUYẾT MINH — {deck['title']}", level=0)
    doc.add_paragraph("Học phần EC1103 — Kỹ năng giao tiếp và soạn thảo văn bản. "
                      "GV: Đỗ Thùy Hương. Mỗi clip mục tiêu 10–15 phút.")

    # gom slide thành clip ~ <= 15 phút (≈ WPM*15 từ); tách khi vượt 12 phút
    clips, cur, cur_words = [], [], 0
    limit = WPM * 12
    for i, (tpl_idx, _m, narr, title) in enumerate(specs, 1):
        w = len(narr.split())
        if cur and cur_words + w > limit:
            clips.append(cur); cur, cur_words = [], 0
        cur.append((i, title, narr, w)); cur_words += w
    if cur:
        clips.append(cur)

    total_words = sum(len(n.split()) for _, _, n, _ in specs)
    doc.add_paragraph(f"Tổng số slide: {len(specs)} · Tổng lời thuyết minh ≈ {total_words} từ "
                      f"≈ {total_words/WPM:.0f} phút · Số clip: {len(clips)}.")

    for ci, clip in enumerate(clips, 1):
        cw = sum(w for *_x, w in clip)
        h = doc.add_heading(f"CLIP {ci} — ước lượng {cw/WPM:.1f} phút", level=1)
        for (sn, title, narr, w) in clip:
            doc.add_heading(f"Slide {sn}: {title}", level=2)
            p = doc.add_paragraph(narr)
            p.style.font.size = Pt(13)
    out_path = OUT / f"{deck['key']}_kichban.docx"
    doc.save(str(out_path))
    return out_path


# ---------- JSON cho lecture-toolkit ----------------------------------------
def build_lecture_json(deck, specs):
    LEC.mkdir(parents=True, exist_ok=True)
    slides = []
    for i, (tpl_idx, _m, narr, title) in enumerate(specs, 1):
        slides.append({
            "image": f"slides/{deck['key']}-{i:02d}.png",
            "narration": narr,
            "subtitle": title,
        })
    data = {"title": deck["key"], "resolution": "1920x1080", "slides": slides}
    out_path = LEC / f"{deck['key']}.json"
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def main():
    for deck in C.DECKS:
        pptx, specs = build_pptx(deck)
        docx = build_docx(deck, specs)
        js = build_lecture_json(deck, specs)
        print(f"✓ {deck['key']}: {len(specs)} slide")
        print(f"    PPTX     : {pptx.relative_to(HERE)}")
        print(f"    Kịch bản : {docx.relative_to(HERE)}")
        print(f"    Lecture  : {js.relative_to(HERE)}")


if __name__ == "__main__":
    main()
