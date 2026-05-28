"""
Classic Engine v28 — Academic Elegance with Visual Intelligence
أكاديمي راقٍ ونظيف وحديث — يجمع بين الكلاسيكية والعصرية
"""
from __future__ import annotations
from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from engine.primitives import (
    W, H, rect, rrect, oval, bg, hline, vline,
    gradient_fill, gradient_rect, shadow, set_solid_alpha,
    multi_stop_gradient, glow, diamond, decorative_dots,
    slide_number, txt, blank_slide,
    # Design intelligence
    kpi_card, result_row, section_divider_line,
    adaptive_body_size, _smart_font_size,
)
from core.themes import Theme
from core.models import PresentationRequest

_FONT = "Cairo"
def set_font(font_name: str):
    global _FONT
    _FONT = font_name

HEADER_H = 2.72    # header height — taller for more presence
FOOTER_H  = 0.34   # bottom accent bar
MX        = 1.1    # horizontal margin

# ── Typography ──────────────────────────────────────────────────────
SZ_SLIDE_TITLE   = 28
SZ_SLIDE_SUB     = 13.5
SZ_SECTION_LABEL = 17
SZ_BODY          = 13.5
SZ_LABEL         = 13.5
SZ_VALUE         = 15
SZ_FINAL_TITLE   = 38
SZ_FINAL_SUB     = 22


def _header(slide, T: Theme, title: str, page_num: int = 0, req=None):
    """Classic header: gradient bg + strong accent lines + smart title."""
    bg(slide, T.bg_rgb)

    # Header gradient
    gradient_rect(slide, 0, 0, W, HEADER_H, T.grad2, T.grad1, angle=90)

    # Double accent line at bottom of header
    al_main = rect(slide, 0, HEADER_H - 0.22, W, 0.22, T.accent_rgb)
    if al_main:
        multi_stop_gradient(al_main, [(0, T.bg), (38, T.accent2), (50, T.accent),
                                       (62, T.accent2), (100, T.bg)], 0)
    rect(slide, 0, HEADER_H - 0.30, W, 0.07, T.muted_rgb)

    # Right accent vertical strip
    vr = rect(slide, W - 0.48, 0, 0.48, HEADER_H, T.accent_rgb)
    if vr: gradient_fill(vr, T.accent_grad1, T.accent_grad2, 90)

    # Decorative corner oval
    oval(slide, W - 5.5, -2.5, 8, 8, T.accent_rgb, alpha=8)
    decorative_dots(slide, MX, HEADER_H * 0.15, 4, 2, 0.14, 0.32, T.accent_rgb, alpha=9)

    # Page number badge
    if page_num > 0:
        nb_s = 0.82
        nb_x = 0.28
        nb_y = (HEADER_H - nb_s) / 2
        pb = rrect(slide, nb_x, nb_y, nb_s, nb_s, T.accent_rgb, radius_pct=50)
        if pb: multi_stop_gradient(pb, [(0, T.accent), (100, T.accent2)], 135)
        txt(slide, str(page_num), nb_x, nb_y, nb_s, nb_s,
            font="Calibri", size=16, bold=True,
            color=T.text_dark_rgb, align=PP_ALIGN.CENTER, rtl=False, vcenter=True)
        total = getattr(req, '_total_slides', 13) if req else 13
        txt(slide, f"/{total}", nb_x + nb_s, nb_y + nb_s * 0.34, 0.88, nb_s * 0.40,
            font="Calibri", size=7.5, bold=False,
            color=T.muted_rgb, align=PP_ALIGN.LEFT, rtl=False, vcenter=True)
        title_x = nb_x + nb_s + 0.82
    else:
        title_x = MX

    title_w = W - title_x - 0.58
    fs = _smart_font_size(title, SZ_SLIDE_TITLE, 18, 32, title_w, HEADER_H - 0.42)
    txt(slide, title, title_x, 0.22, title_w, HEADER_H - 0.44,
        font=_FONT, size=fs, bold=True,
        color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
        rtl=True, vcenter=True, line_spacing=1.05)

    # Content area background
    gradient_rect(slide, 0, HEADER_H, W, H - HEADER_H, T.bg, T.bg2, angle=90)

    # Footer bar (subtle)
    bt = rect(slide, 0, H - FOOTER_H, W, FOOTER_H, T.bg2_rgb)
    bta = rect(slide, 0, H - FOOTER_H, W, 0.07, T.accent_rgb)
    if bta: gradient_fill(bta, T.accent_grad1, T.accent_grad2, 0)


def _content_y():
    return HEADER_H + 0.30

def _content_h():
    return H - HEADER_H - FOOTER_H - 0.58


# ══════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════
def make_cover(prs, req: PresentationRequest, T: Theme):
    slide = blank_slide(prs)
    bg(slide, T.bg_rgb)
    gradient_rect(slide, 0, 0, W, H, T.grad1, T.grad2, angle=155)
    oval(slide, W - 10, -3, 13, 13, T.accent_rgb, alpha=5)
    oval(slide, -2.5, H - 9, 11, 11, T.bg2_rgb, alpha=33)

    # Frame borders
    r_top = rect(slide, 0, 0, W, 0.24, T.accent_rgb)
    if r_top: gradient_fill(r_top, T.accent_grad1, T.accent_grad2, 0)
    r_bot = rect(slide, 0, H - 0.24, W, 0.24, T.accent_rgb)
    if r_bot: gradient_fill(r_bot, T.accent_grad1, T.accent_grad2, 0)
    vline(slide, 0.24, 0.24, H - 0.48, T.accent_rgb, thickness=0.09)
    vline(slide, W - 0.32, 0.24, H - 0.48, T.accent_rgb, thickness=0.09)

    if req.institution:
        txt(slide, req.institution, 2.8, 0.42, W - 5.6, 0.86,
            font=_FONT, size=12, bold=False, color=T.muted_rgb,
            align=PP_ALIGN.CENTER, rtl=True, vcenter=True)
    hline(slide, W * 0.18, 1.32, W * 0.64, T.accent_rgb, thickness=0.055)

    total_h = H - 0.24 - 1.48
    title_h = total_h * 0.42
    info_y = 1.48 + title_h + 0.24
    info_h = H - 0.24 - info_y - 0.14

    # Year extraction
    import re as _re
    _yp = _re.compile(r'\b\d{4}\s*[-–—]\s*\d{4}\b')
    _ym = _yp.search(req.title_ar or '')
    if _ym:
        _year_str = _ym.group(0).strip()
        _title_clean = _yp.sub('', req.title_ar).strip(' —–-،, ')
    elif req.year:
        _year_str = req.year.strip()
        _title_clean = req.title_ar
    else:
        _year_str = ''
        _title_clean = req.title_ar

    has_year = bool(_year_str)
    title_text_h = title_h * (0.58 if has_year else 0.72)
    ts = _smart_font_size(_title_clean, 26, 15, 30, W - 4.6, title_text_h)

    txt(slide, _title_clean, 2.3, 1.48, W - 4.6, title_text_h,
        font=_FONT, size=ts, bold=True, color=T.text_light_rgb,
        align=PP_ALIGN.CENTER, rtl=True, vcenter=True, line_spacing=1.22)

    if req.title_en:
        en_y = 1.48 + title_text_h + 0.06
        txt(slide, req.title_en, 2.6, en_y, W - 5.2, 0.76,
            font="Calibri", size=11, bold=False, italic=True,
            color=T.muted_rgb, align=PP_ALIGN.CENTER, rtl=False, vcenter=True)

    if has_year:
        yr_y = 1.48 + title_h * 0.75
        yr_h = 0.60
        yr_cx = W * 0.25; yr_cw = W * 0.50
        yb = rrect(slide, yr_cx, yr_y, yr_cw, yr_h, T.accent_rgb, radius_pct=50)
        if yb: set_solid_alpha(yb, 22)
        hline(slide, yr_cx + yr_cw * 0.08, yr_y, yr_cw * 0.84, T.accent_rgb, thickness=0.035)
        hline(slide, yr_cx + yr_cw * 0.08, yr_y + yr_h, yr_cw * 0.84, T.accent_rgb, thickness=0.035)
        txt(slide, f'( {_year_str} )', yr_cx, yr_y, yr_cw, yr_h,
            font=_FONT, size=13, bold=False, italic=True,
            color=T.accent_rgb, align=PP_ALIGN.CENTER, rtl=False, vcenter=True)

    hl1 = rect(slide, W * 0.12, info_y - 0.20, W * 0.76, 0.07, T.accent_rgb)
    if hl1: multi_stop_gradient(hl1, [(0, T.bg), (50, T.accent), (100, T.bg)], 0)
    rect(slide, W * 0.20, info_y - 0.10, W * 0.60, 0.032, T.muted_rgb)

    rows = [("اسم الطالب", req.student_name)]
    if req.supervisor:     rows.append(("المشرف", req.supervisor))
    if req.co_supervisor:  rows.append(("المشرف المساعد", req.co_supervisor))
    if req.specialization: rows.append(("التخصص", req.specialization))

    rh = info_h / max(len(rows), 1)
    row_w = W - MX * 2
    lbl_w = 4.0

    for i, (lbl, val) in enumerate(rows):
        y = info_y + i * rh
        fill = T.bg2_rgb if i % 2 == 0 else T.card_rgb
        rb = rrect(slide, MX, y, row_w, rh - 0.07, fill, radius_pct=6)
        if rb: shadow(rb, blur=5, dist=2, alpha=0.14)
        acc = rect(slide, W - MX - 0.20, y, 0.20, rh - 0.07, T.accent_rgb)
        if acc: set_solid_alpha(acc, 68)
        lbl_x = W - MX - lbl_w - 0.22
        val_x = MX + 0.32
        val_w = row_w - lbl_w - 0.56
        txt(slide, f"{lbl} :", lbl_x, y, lbl_w, rh - 0.07,
            font=_FONT, size=max(13, min(15, rh * 8.5)), bold=True,
            color=T.accent_rgb, align=PP_ALIGN.RIGHT, rtl=True, vcenter=True, line_spacing=1.0)
        vline(slide, lbl_x - 0.16, y + rh * 0.10, rh * 0.70, T.muted_rgb, thickness=0.045)
        txt(slide, val, val_x, y, val_w, rh - 0.07,
            font=_FONT, size=max(14, min(16, rh * 10)), bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.LEFT, rtl=False, vcenter=True, line_spacing=1.0)

    return slide


# ══════════════════════════════════════════════════════════════════════
# INTRO
# ══════════════════════════════════════════════════════════════════════
def make_intro(prs, req: PresentationRequest, T: Theme):
    slide = blank_slide(prs)
    _header(slide, T, "مقدمة البحث", 1, req=req)
    CY = _content_y(); CH = _content_h()
    items = []
    if req.intro_overview: items.append(("نظرة عامة", req.intro_overview))
    if req.intro_approach:  items.append(("المنهج المتبع", req.intro_approach))
    if not items: return slide

    avail_h = CH
    card_h = (avail_h - 0.28 * (len(items) - 1)) / max(len(items), 1)

    for i, (lbl, val) in enumerate(items[:2]):
        y = CY + i * (card_h + 0.28)
        cw = W - MX * 2 - 0.36
        cb = rrect(slide, MX, y, cw, card_h,
                   T.bg2_rgb if i % 2 == 0 else T.card_rgb, radius_pct=9)
        if cb:
            stops = [(0, T.bg2), (100, T.card)] if i % 2 == 0 else [(0, T.card), (100, T.bg2)]
            multi_stop_gradient(cb, stops, 0)
            shadow(cb, blur=15, dist=4, alpha=0.34)

        # Right accent bar
        vline(slide, W - MX - 0.34 - 0.14, y, card_h, T.accent_rgb, thickness=0.14)

        # Header bar
        hdr_bar = rrect(slide, MX, y, cw, 0.66, T.accent_rgb, radius_pct=0)
        if hdr_bar: multi_stop_gradient(hdr_bar, [(0, T.accent), (100, T.accent2)], 0)

        txt(slide, lbl, MX + 0.20, y, cw - 0.80, 0.66,
            font=_FONT, size=SZ_SECTION_LABEL, bold=True,
            color=T.text_dark_rgb, align=PP_ALIGN.RIGHT, rtl=True, vcenter=True)

        section_divider_line(slide, MX, y + 0.68, cw, T)

        fs = adaptive_body_size(val, card_h - 0.90, base=13.5, min_s=11, max_s=16)
        txt(slide, val, MX + 0.22, y + 0.78, cw - 0.60, card_h - 0.90,
            font=_FONT, size=fs, bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
            rtl=True, vcenter=True, line_spacing=1.35)

    return slide


# ══════════════════════════════════════════════════════════════════════
# PLAN
# ══════════════════════════════════════════════════════════════════════
def make_plan(prs, req: PresentationRequest, T: Theme):
    slide = blank_slide(prs)
    _header(slide, T, "خطة البحث", page_num=2, req=req)
    CY = _content_y(); CH = _content_h()
    chapters = req.chapters[:8]; n = len(chapters)
    if not chapters: return slide

    gap = 0.15
    row_h = (CH - gap * (n - 1)) / n

    for i, ch in enumerate(chapters):
        y = CY + i * (row_h + gap)
        fill = T.bg2_rgb if i % 2 == 0 else T.card_rgb
        rw = rrect(slide, MX, y, W - MX * 2, row_h, fill, radius_pct=8)
        if rw:
            stops = [(0, T.bg2), (100, T.card)] if i % 2 == 0 else [(0, T.card), (100, T.bg2)]
            multi_stop_gradient(rw, stops, 0)
            shadow(rw, blur=6, dist=2, alpha=0.18)

        acc = rect(slide, W - MX - 0.24, y, 0.24, row_h, T.accent_rgb)
        if acc: gradient_fill(acc, T.accent_grad1, T.accent_grad2, 90)

        # Chapter label
        num_lbl = f"الفصل {i + 1}"
        txt(slide, num_lbl, MX + 0.15, y, 3.3, row_h,
            font=_FONT, size=max(13, min(15, int(row_h * 9.5))),
            bold=True, color=T.accent_rgb,
            align=PP_ALIGN.RIGHT, rtl=True, vcenter=True)
        vline(slide, MX + 3.5, y + row_h * 0.12, row_h * 0.76, T.muted_rgb, thickness=0.045)

        fs = _smart_font_size(ch.title, 14.5, 11.5, 17, W - MX * 2 - 4.8, row_h)
        txt(slide, ch.title, MX + 3.65, y, W - MX * 2 - 4.5, row_h,
            font=_FONT, size=fs, bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
            rtl=True, vcenter=True, line_spacing=1.15)

        if ch.pages:
            txt(slide, ch.pages, MX + 0.15, y, 1.9, row_h,
                font="Calibri", size=9, bold=False,
                color=T.muted_rgb, align=PP_ALIGN.LEFT, rtl=False, vcenter=True)

    return slide


# ══════════════════════════════════════════════════════════════════════
# PROBLEM
# ══════════════════════════════════════════════════════════════════════
def make_problem(prs, req: PresentationRequest, T: Theme):
    slide = blank_slide(prs)
    _header(slide, T, "إشكالية البحث", 3, req=req)
    cx = MX; cw = W - MX * 2; cy = _content_y()

    if req.main_problem:
        # Problem card
        pb_h = min(_content_h() * 0.45, 4.5)
        pc = rrect(slide, cx, cy, cw, pb_h, T.card_rgb, radius_pct=10)
        if pc:
            multi_stop_gradient(pc, [(0, T.card), (100, T.bg2)], 135)
            shadow(pc, blur=16, dist=4, alpha=0.36)

        vline(slide, W - MX - 0.16, cy, pb_h, T.accent_rgb, thickness=0.16)

        lbl_bar = rrect(slide, cx, cy, cw, 0.58, T.accent_rgb, radius_pct=0)
        if lbl_bar: multi_stop_gradient(lbl_bar, [(0, T.accent), (100, T.accent2)], 0)
        txt(slide, "◆  الإشكالية الرئيسية", cx + 0.20, cy, cw - 0.40, 0.58,
            font=_FONT, size=SZ_LABEL, bold=True,
            color=T.text_dark_rgb, align=PP_ALIGN.RIGHT, rtl=True, vcenter=True)

        txt(slide, "❝", cx + 0.22, cy + 0.62, 1.5, 1.1,
            font="Calibri", size=30, bold=False, color=T.accent_rgb,
            align=PP_ALIGN.LEFT, rtl=False, vcenter=False)

        fs = adaptive_body_size(req.main_problem, pb_h - 0.78, base=13.5, min_s=11, max_s=16)
        txt(slide, req.main_problem, cx + 1.85, cy + 0.65, cw - 2.22, pb_h - 0.80,
            font=_FONT, size=fs, bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
            rtl=True, vcenter=True, line_spacing=1.36)
        cy += pb_h + 0.24

    if req.main_question:
        qh = min(_content_h() * 0.28, 2.8)
        hline(slide, cx, cy, cw, T.accent_rgb, thickness=0.07)
        cy += 0.16
        txt(slide, "التساؤل الرئيسي", cx, cy, cw, 0.62,
            font=_FONT, size=SZ_LABEL, bold=True, color=T.accent_rgb,
            align=PP_ALIGN.RIGHT, rtl=True, vcenter=True)
        fs = adaptive_body_size(req.main_question, qh - 0.72, base=13.5, min_s=11, max_s=15)
        txt(slide, req.main_question, cx, cy + 0.68, cw, qh - 0.72,
            font=_FONT, size=fs, bold=False, italic=True,
            color=T.text_light_rgb, align=PP_ALIGN.RIGHT, rtl=True, vcenter=True)
        cy += qh

    if req.sub_questions:
        hline(slide, cx, cy, cw, T.muted_rgb, thickness=0.034)
        cy += 0.22
        txt(slide, "التساؤلات الفرعية", cx, cy, cw, 0.58,
            font=_FONT, size=SZ_LABEL, bold=True,
            color=T.muted_rgb, align=PP_ALIGN.RIGHT, rtl=True, vcenter=True)
        cy += 0.64
        avail = H - cy - FOOTER_H - 0.28
        sub_h = min(avail / max(len(req.sub_questions), 1), 0.88)
        for i, q in enumerate(req.sub_questions[:6]):
            y = cy + i * sub_h
            if i % 2 == 0:
                rb = rrect(slide, cx, y, cw, sub_h - 0.06, T.bg2_rgb, radius_pct=5)
                if rb: set_solid_alpha(rb, 55)
            dot = oval(slide, W - MX - 0.56, y + (sub_h - 0.30) / 2, 0.30, 0.30, T.accent_rgb)
            if dot: set_solid_alpha(dot, 70)
            txt(slide, str(i + 1), W - MX - 0.56, y + (sub_h - 0.30) / 2, 0.30, 0.30,
                font="Calibri", size=7.5, bold=True,
                color=T.accent_rgb, align=PP_ALIGN.CENTER, rtl=False, vcenter=True)
            fs = _smart_font_size(q, 13, 10.5, 14.5, cw - 0.9, sub_h)
            txt(slide, q, cx, y, cw - 0.7, sub_h,
                font=_FONT, size=fs, bold=False,
                color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
                rtl=True, vcenter=True, line_spacing=1.18)

    return slide


# ══════════════════════════════════════════════════════════════════════
# OBJECTIVES
# ══════════════════════════════════════════════════════════════════════
def make_objectives(prs, req: PresentationRequest, T: Theme):
    slide = blank_slide(prs)
    _header(slide, T, "أهداف البحث وفرضياته", page_num=4, req=req)
    CY = _content_y(); CH = _content_h()
    cols_data = []
    if req.objectives: cols_data.append(("الأهداف", req.objectives))
    if req.hypotheses:  cols_data.append(("الفرضيات", req.hypotheses))
    if not cols_data: return slide

    n_c = len(cols_data); gap = 0.32
    col_w = (W - MX * 2 - gap * (n_c - 1)) / n_c

    for i, (lbl, items) in enumerate(cols_data[:2]):
        x = MX + i * (col_w + gap)
        hh = 0.68
        hdr = rrect(slide, x, CY, col_w, hh, T.bg2_rgb, radius_pct=0)
        acc_top = rect(slide, x, CY, col_w, 0.11, T.accent_rgb)
        if acc_top: gradient_fill(acc_top, T.accent_grad1, T.accent_grad2, 0)
        acc_r = rect(slide, x + col_w - 0.13, CY, 0.13, hh, T.accent_rgb)
        txt(slide, lbl, x + 0.18, CY, col_w - 0.38, hh,
            font=_FONT, size=SZ_SECTION_LABEL, bold=True,
            color=T.accent_rgb, align=PP_ALIGN.RIGHT, rtl=True, vcenter=True)

        ia = CH - hh - 0.12; n_items = min(len(items), 8); ig = 0.12
        ih = (ia - ig * (n_items - 1)) / n_items

        for j, item in enumerate(items[:8]):
            iy = CY + hh + 0.06 + j * (ih + ig)
            fill = T.bg2_rgb if j % 2 == 0 else T.card_rgb
            rb = rrect(slide, x, iy, col_w, ih, fill, radius_pct=6)
            if rb: shadow(rb, blur=4, dist=1, alpha=0.12)

            txt(slide, str(j + 1), x + 0.12, iy, 0.84, ih,
                font="Calibri", size=max(9, int(ih * 7)),
                bold=True, color=T.accent_rgb,
                align=PP_ALIGN.CENTER, rtl=False, vcenter=True)
            vline(slide, x + 0.98, iy + ih * 0.10, ih * 0.80, T.muted_rgb, thickness=0.045)

            fs = _smart_font_size(item, 13.5, 11, 15.5, col_w - 1.28, ih)
            txt(slide, item, x + 1.10, iy + 0.04, col_w - 1.28, ih - 0.08,
                font=_FONT, size=fs, bold=False,
                color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
                rtl=True, vcenter=True, line_spacing=1.2)

    return slide


# ══════════════════════════════════════════════════════════════════════
# IMPORTANCE
# ══════════════════════════════════════════════════════════════════════
def make_importance(prs, req: PresentationRequest, T: Theme):
    slide = blank_slide(prs)
    _header(slide, T, "أهمية البحث", page_num=5, req=req)
    CY = _content_y(); CH = _content_h()
    items = req.importance[:6]
    if not items: return slide

    n = len(items); gap = 0.16
    row_h = (CH - gap * (n - 1)) / n

    for i, item in enumerate(items):
        y = CY + i * (row_h + gap)
        fill = T.bg2_rgb if i % 2 == 0 else T.card_rgb
        rb = rrect(slide, MX, y, W - MX * 2, row_h, fill, radius_pct=8)
        if rb:
            stops = [(0, T.bg2), (100, T.card)] if i % 2 == 0 else [(0, T.card), (100, T.bg2)]
            multi_stop_gradient(rb, stops, 0)
            shadow(rb, blur=5, dist=2, alpha=0.16)

        acc = rect(slide, W - MX - 0.22, y, 0.22, row_h, T.accent_rgb)
        if acc: gradient_fill(acc, T.accent_grad1, T.accent_grad2, 90)

        num_text = f"{i+1:02d}"
        txt(slide, num_text, MX + 0.14, y, 1.45, row_h,
            font="Calibri", size=max(14, int(row_h * 9.5)),
            bold=True, color=T.accent_rgb,
            align=PP_ALIGN.CENTER, rtl=False, vcenter=True)
        vline(slide, MX + 1.65, y + row_h * 0.08, row_h * 0.84, T.muted_rgb, thickness=0.045)

        fs = _smart_font_size(item, 13.5, 11, 16, W - MX * 2 - 2.3, row_h)
        txt(slide, item, MX + 1.84, y + 0.08, W - MX * 2 - 2.28, row_h - 0.16,
            font=_FONT, size=fs, bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
            rtl=True, vcenter=True, line_spacing=1.3)

    return slide


# ══════════════════════════════════════════════════════════════════════
# METHODOLOGY
# ══════════════════════════════════════════════════════════════════════
def make_methodology(prs, req: PresentationRequest, T: Theme):
    slide = blank_slide(prs)
    _header(slide, T, "منهجية البحث", 6, req=req)
    CY = _content_y(); CH = _content_h()
    cx = MX; cw = W - MX * 2
    fields = []
    if req.methodology:  fields.append(("المنهج المتبع", req.methodology))
    if req.sample_type:  fields.append(("نوع العينة", req.sample_type))
    if req.sample_size:  fields.append(("حجم العينة", req.sample_size))
    if req.tool:         fields.append(("أداة الدراسة", req.tool))
    if not fields: return slide

    row_h = min((CH - 0.18 * (len(fields) - 1)) / max(len(fields), 1), 2.8)

    for i, (lbl, val) in enumerate(fields[:4]):
        y = CY + i * (row_h + 0.18)
        fill = T.bg2_rgb if i % 2 == 0 else T.card_rgb
        rw = rrect(slide, cx, y, cw, row_h, fill, radius_pct=8)
        if rw:
            shadow(rw, blur=7, dist=2, alpha=0.18)

        vline(slide, W - MX - 0.14, y, row_h, T.accent_rgb, thickness=0.14)

        # Label column
        lbl_bg = rrect(slide, cx, y, 5.2, row_h,
                       T.bg2_rgb if i % 2 != 0 else T.card_rgb, radius_pct=0)
        acc_lbl = rect(slide, cx, y, 5.2, 0.09, T.accent_rgb)
        if acc_lbl: gradient_fill(acc_lbl, T.accent_grad1, T.accent_grad2, 0)

        fs_lbl = _smart_font_size(lbl, SZ_LABEL, 11, 16, 5.0, row_h)
        txt(slide, lbl, cx + 0.16, y, 4.9, row_h,
            font=_FONT, size=fs_lbl, bold=True,
            color=T.accent_rgb, align=PP_ALIGN.RIGHT, rtl=True, vcenter=True)
        vline(slide, cx + 5.3, y + 0.10, row_h - 0.20, T.muted_rgb, thickness=0.045)

        fs = adaptive_body_size(val, row_h - 0.24, base=13.5, min_s=11, max_s=16)
        txt(slide, val, cx + 5.5, y + 0.12, cw - 5.88, row_h - 0.24,
            font=_FONT, size=fs, bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
            rtl=True, vcenter=True, line_spacing=1.28)

    return slide


# ══════════════════════════════════════════════════════════════════════
# STATS ★
# ══════════════════════════════════════════════════════════════════════
def make_stats(prs, req: PresentationRequest, T: Theme):
    slide = blank_slide(prs)
    _header(slide, T, "الأرقام والإحصاءات الرئيسية", page_num=7, req=req)
    CY = _content_y(); CH = _content_h()
    stats = req.stats[:6]
    if not stats: return slide

    cols = 3 if len(stats) >= 3 else len(stats)
    rows_n = (len(stats) + cols - 1) // cols
    gh = 0.30; gv = 0.22
    cw = (W - MX * 2 - gh * (cols - 1)) / cols
    ch = (CH - gv * (rows_n - 1)) / rows_n

    for i, stat in enumerate(stats):
        ci = i % cols; ri = i // cols
        x = MX + ci * (cw + gh); y = CY + ri * (ch + gv)
        kpi_card(slide, x, y, cw, ch, T,
                 value=stat.value, label=stat.label,
                 unit=getattr(stat, 'unit', ''), font=_FONT)

    return slide


# ══════════════════════════════════════════════════════════════════════
# RESULTS ★
# ══════════════════════════════════════════════════════════════════════
def make_results(prs, req: PresentationRequest, T: Theme):
    slide = blank_slide(prs)
    _header(slide, T, "نتائج البحث", page_num=8, req=req)
    CY = _content_y(); CH = _content_h()
    results = req.main_results[:8]; n = len(results)
    if not results: return slide

    gap = 0.16
    row_h = (CH - gap * (n - 1)) / n

    for i, result in enumerate(results):
        y = CY + i * (row_h + gap)
        highlight = (i < 2 and n >= 3)
        result_row(slide, MX, y, W - MX * 2, row_h, T, result, i + 1,
                   font=_FONT, highlight=highlight)

    return slide


# ══════════════════════════════════════════════════════════════════════
# CONCLUSION
# ══════════════════════════════════════════════════════════════════════
def make_conclusion(prs, req: PresentationRequest, T: Theme):
    slide = blank_slide(prs)
    _header(slide, T, "خاتمة البحث", page_num=9, req=req)
    CY = _content_y(); CH = _content_h(); cw = W - MX * 2

    # Outer glow
    og = rrect(slide, MX - 0.10, CY - 0.10, cw + 0.20, CH + 0.20, T.accent_rgb, radius_pct=10)
    if og: set_solid_alpha(og, 10)

    cb = rrect(slide, MX, CY, cw, CH, T.bg2_rgb, radius_pct=9)
    if cb:
        multi_stop_gradient(cb, [(0, T.bg2), (100, T.card)], 135)
        shadow(cb, blur=22, dist=6, alpha=0.40)

    acc_r = rect(slide, W - MX - 0.22, CY, 0.22, CH, T.accent_rgb)
    if acc_r: gradient_fill(acc_r, T.accent_grad1, T.accent_grad2, 90)

    # Accent top bar
    tp = rrect(slide, MX, CY, cw, 0.30, T.accent_rgb, radius_pct=0)
    if tp: multi_stop_gradient(tp, [(0, T.accent2), (50, T.accent), (100, T.accent2)], 0)

    txt(slide, "الاستنتاج العام", MX + 0.30, CY + 0.38, cw - 0.60, 0.74,
        font=_FONT, size=14.5, bold=True,
        color=T.accent_rgb, align=PP_ALIGN.RIGHT, rtl=True, vcenter=True)

    section_divider_line(slide, MX, CY + 1.16, cw, T)

    fs = adaptive_body_size(req.general_conclusion, CH - 2.12, base=14, min_s=12, max_s=17)
    txt(slide, req.general_conclusion, MX + 0.30, CY + 1.28, cw - 0.58, CH - 2.10,
        font=_FONT, size=fs, bold=False,
        color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
        rtl=True, vcenter=True, line_spacing=1.38)

    ny = CY + CH - 0.82
    hline(slide, MX + cw * 0.16, ny, cw * 0.68, T.accent_rgb, thickness=0.07)
    rect(slide, MX + cw * 0.26, ny + 0.12, cw * 0.48, 0.032, T.muted_rgb)
    txt(slide, req.student_name, MX, ny + 0.14, cw, 0.66,
        font=_FONT, size=22, bold=True, color=T.accent_rgb,
        align=PP_ALIGN.CENTER, rtl=True, vcenter=True)

    return slide


# ══════════════════════════════════════════════════════════════════════
# RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════
def make_recommendations(prs, req: PresentationRequest, T: Theme):
    slide = blank_slide(prs)
    _header(slide, T, "توصيات البحث", page_num=10, req=req)
    CY = _content_y(); CH = _content_h()
    recs = req.recommendations[:8]; n = len(recs)
    if not recs: return slide

    gap = 0.16
    row_h = (CH - gap * (n - 1)) / n

    for i, rec in enumerate(recs):
        y = CY + i * (row_h + gap)
        fill = T.bg2_rgb if i % 2 == 0 else T.card_rgb
        rb = rrect(slide, MX, y, W - MX * 2, row_h, fill, radius_pct=8)
        if rb:
            stops = [(0, T.bg2), (100, T.card)] if i % 2 == 0 else [(0, T.card), (100, T.bg2)]
            multi_stop_gradient(rb, stops, 0)
            shadow(rb, blur=5, dist=2, alpha=0.18)

        acc = rect(slide, W - MX - 0.22, y, 0.22, row_h, T.accent_rgb)
        if acc: gradient_fill(acc, T.accent_grad1, T.accent_grad2, 90)

        dot = oval(slide, MX + 0.26, y + (row_h - 0.40) / 2, 0.40, 0.40, T.accent_rgb)
        if dot: gradient_fill(dot, T.accent_grad1, T.accent_grad2, 135)

        fs = _smart_font_size(rec, 13.5, 11, 15.5, W - MX * 2 - 1.24, row_h)
        txt(slide, rec, MX + 0.82, y + 0.06, W - MX * 2 - 1.24, row_h - 0.12,
            font=_FONT, size=fs, bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
            rtl=True, vcenter=True, line_spacing=1.26)

    return slide


# ══════════════════════════════════════════════════════════════════════
# FUTURE
# ══════════════════════════════════════════════════════════════════════
def make_future(prs, req: PresentationRequest, T: Theme):
    slide = blank_slide(prs)
    _header(slide, T, "آفاق البحث المستقبلية", page_num=11, req=req)
    CY = _content_y(); CH = _content_h()
    items = req.future_work[:6]
    if not items: return slide

    cols = 2 if len(items) > 3 else 1
    rows_n = (len(items) + cols - 1) // cols
    gh = 0.28; gv = 0.20
    cw = (W - MX * 2 - gh * (cols - 1)) / cols
    ch = (CH - gv * (rows_n - 1)) / rows_n

    for i, item in enumerate(items):
        ci = i % cols; ri = i // cols
        x = MX + ci * (cw + gh); y = CY + ri * (ch + gv)
        cb = rrect(slide, x, y, cw, ch,
                   T.bg2_rgb if i % 2 == 0 else T.card_rgb, radius_pct=8)
        if cb:
            shadow(cb, blur=8, dist=3, alpha=0.22)

        acc = rect(slide, x + cw - 0.20, y, 0.20, ch, T.accent_rgb)
        if acc: gradient_fill(acc, T.accent_grad1, T.accent_grad2, 90)

        tp = rect(slide, x, y, cw, 0.11, T.accent_rgb)
        if tp: gradient_fill(tp, T.accent_grad1, T.accent_grad2, 0)

        txt(slide, str(i + 1), x + 0.16, y, 1.1, ch,
            font="Calibri", size=max(18, int(ch * 8.5)),
            bold=True, color=T.accent_rgb,
            align=PP_ALIGN.CENTER, rtl=False, vcenter=True)
        vline(slide, x + 1.30, y + ch * 0.10, ch * 0.80, T.muted_rgb, thickness=0.045)

        fs = _smart_font_size(item, 13.5, 11, 15.5, cw - 1.68, ch - 0.22)
        txt(slide, item, x + 1.46, y + 0.12, cw - 1.70, ch - 0.24,
            font=_FONT, size=fs, bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
            rtl=True, vcenter=True, line_spacing=1.28)

    return slide


# ══════════════════════════════════════════════════════════════════════
# REFERENCES
# ══════════════════════════════════════════════════════════════════════
def make_references(prs, req: PresentationRequest, T: Theme):
    slide = blank_slide(prs)
    _header(slide, T, "قائمة المراجع", page_num=12, req=req)
    CY = _content_y(); CH = _content_h()
    refs = req.references[:12]; n = len(refs)
    if not refs: return slide

    gap = 0.13
    row_h = (CH - gap * (n - 1)) / n

    for i, ref in enumerate(refs):
        y = CY + i * (row_h + gap)
        fill = T.bg2_rgb if i % 2 == 0 else T.card_rgb
        rb = rrect(slide, MX, y, W - MX * 2, row_h, fill, radius_pct=6)
        if rb:
            stops = [(0, T.bg2), (100, T.card)] if i % 2 == 0 else [(0, T.card), (100, T.bg2)]
            multi_stop_gradient(rb, stops, 0)

        acc = rect(slide, W - MX - 0.20, y, 0.20, row_h, T.accent_rgb)
        if acc: set_solid_alpha(acc, 58)

        txt(slide, f"[{i+1}]", MX + 0.12, y, 0.76, row_h,
            font="Calibri", size=max(8.5, int(row_h * 7)),
            bold=True, color=T.accent_rgb,
            align=PP_ALIGN.CENTER, rtl=False, vcenter=True)
        vline(slide, MX + 0.94, y + row_h * 0.08, row_h * 0.84, T.muted_rgb, thickness=0.035)

        fs = _smart_font_size(ref, 13, 10.5, 14.5, W - MX * 2 - 1.46, row_h)
        txt(slide, ref, MX + 1.08, y + 0.04, W - MX * 2 - 1.46, row_h - 0.08,
            font=_FONT, size=fs, bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
            rtl=True, vcenter=True, line_spacing=1.15)

    return slide


# ══════════════════════════════════════════════════════════════════════
# FINAL (Thank You)
# ══════════════════════════════════════════════════════════════════════
def make_final(prs, req: PresentationRequest, T: Theme):
    slide = blank_slide(prs)
    bg(slide, T.bg_rgb)
    gradient_rect(slide, 0, 0, W, H, T.grad1, T.grad2, angle=155)

    # Border frame
    r_top = rect(slide, 0, 0, W, 0.24, T.accent_rgb)
    if r_top: gradient_fill(r_top, T.accent_grad1, T.accent_grad2, 0)
    r_bot = rect(slide, 0, H - 0.24, W, 0.24, T.accent_rgb)
    if r_bot: gradient_fill(r_bot, T.accent_grad1, T.accent_grad2, 0)
    vline(slide, 0.24, 0.24, H - 0.48, T.accent_rgb, thickness=0.09)
    vline(slide, W - 0.32, 0.24, H - 0.48, T.accent_rgb, thickness=0.09)

    # Ambient shapes
    oval(slide, W - 10, -3, 13, 13, T.accent_rgb, alpha=5)
    oval(slide, -2.5, H - 9, 11, 11, T.bg2_rgb, alpha=30)
    decorative_dots(slide, W * 0.06, H * 0.42, 4, 4, 0.14, 0.34, T.accent_rgb, alpha=8)

    cw = W - MX * 2
    cy = H * 0.10; ch = H * 0.80

    # Outer glow
    og = rrect(slide, MX - 0.14, cy - 0.14, cw + 0.28, ch + 0.28, T.accent_rgb, radius_pct=12)
    if og: set_solid_alpha(og, 13)

    cb = rrect(slide, MX, cy, cw, ch, T.bg2_rgb, radius_pct=11)
    if cb:
        multi_stop_gradient(cb, [(0, T.bg2), (100, T.card)], 135)
        shadow(cb, blur=30, dist=9, alpha=0.54)

    acc_top = rect(slide, MX, cy, cw, 0.18, T.accent_rgb)
    if acc_top: gradient_fill(acc_top, T.accent_grad1, T.accent_grad2, 0)
    acc_bot = rect(slide, MX, cy + ch - 0.18, cw, 0.18, T.accent_rgb)
    if acc_bot: gradient_fill(acc_bot, T.accent_grad1, T.accent_grad2, 0)
    acc_r = rect(slide, MX + cw - 0.20, cy, 0.20, ch, T.accent_rgb)
    acc_l = rect(slide, MX, cy, 0.20, ch, T.accent_rgb)

    # ✦ decorative
    txt(slide, "✦", MX + 0.4, cy + 0.38, cw - 0.8, 1.2,
        font="Calibri", size=30, bold=False, color=T.accent_rgb,
        align=PP_ALIGN.CENTER, rtl=False, vcenter=True)

    txt(slide, "شكراً وتقديراً", MX + 0.40, cy + 0.48, cw - 0.80, H * 0.26,
        font=_FONT, size=SZ_FINAL_TITLE, bold=True,
        color=T.text_light_rgb, align=PP_ALIGN.CENTER, rtl=True, vcenter=True)

    hl1 = rect(slide, MX + cw * 0.15, cy + H * 0.32, cw * 0.70, 0.07, T.accent_rgb)
    if hl1: multi_stop_gradient(hl1, [(0, T.bg2), (50, T.accent), (100, T.bg2)], 0)
    rect(slide, MX + cw * 0.25, cy + H * 0.32 + 0.14, cw * 0.50, 0.033, T.muted_rgb)

    txt(slide, req.student_name, MX + 0.40, cy + H * 0.35, cw - 0.80, H * 0.14,
        font=_FONT, size=SZ_FINAL_SUB, bold=True,
        color=T.accent_rgb, align=PP_ALIGN.CENTER, rtl=True, vcenter=True)

    ts = req.title_ar[:72] + ("..." if len(req.title_ar) > 72 else "")
    txt(slide, ts, MX + 0.60, cy + H * 0.50, cw - 1.20, H * 0.18,
        font=_FONT, size=SZ_BODY, bold=False, italic=True,
        color=T.muted_rgb, align=PP_ALIGN.CENTER, rtl=True, vcenter=True, line_spacing=1.28)

    footer = []
    if req.institution: footer.append(req.institution)
    if req.year: footer.append(req.year)
    if footer:
        txt(slide, "  ·  ".join(footer), MX + 0.40, cy + H * 0.70, cw - 0.80, H * 0.10,
            font=_FONT, size=SZ_BODY, bold=False,
            color=T.muted_rgb, align=PP_ALIGN.CENTER, rtl=True, vcenter=True)

    return slide
