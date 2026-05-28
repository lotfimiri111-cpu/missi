"""
Premium Engine v28 — Envato-Grade Sidebar Layout with Visual Intelligence
شريط جانبي فاخر + محتوى ذكي يملأ الشريحة
"""
from __future__ import annotations
from pptx.enum.text import PP_ALIGN
from engine.primitives import (
    W, H, rect, rrect, oval, bg, hline, vline,
    gradient_fill, gradient_rect, shadow, set_solid_alpha,
    multi_stop_gradient, glow, diamond, decorative_dots,
    number_badge, icon_circle, slide_number, txt, blank_slide,
    # Design intelligence
    kpi_card, result_row, section_divider_line,
    adaptive_body_size, _smart_font_size, premium_bg,
    premium_card, card_with_accent_top,
)
from core.themes import Theme
from core.models import PresentationRequest

_FONT = "Cairo"
def set_font(n): global _FONT; _FONT = n

# ── Layout constants ────────────────────────────────────────────────
SW = 5.4     # sidebar width
CX = SW + 0.60
CW = W - CX - 0.55

# ── Typography ──────────────────────────────────────────────────────
SZ_SLIDE_TITLE   = 30
SZ_SECTION_LABEL = 19
SZ_BODY          = 13.5
SZ_LABEL         = 13
SZ_FINAL_TITLE   = 40
SZ_FINAL_SUB     = 22


def _sidebar(slide, T, icon, label1, label2=""):
    """Premium sidebar with depth layers."""
    # Main sidebar gradient
    sb = rect(slide, 0, 0, SW, H, T.bg_rgb)
    gradient_rect(slide, 0, 0, SW, H, T.grad2, T.grad1, angle=180)

    # Separator with glow
    sep = rect(slide, SW, 0, 0.14, H, T.accent_rgb)
    if sep: gradient_fill(sep, T.accent_grad1, T.accent_grad2, 90)

    # Ambient shapes in sidebar
    oval(slide, -3.5, -3.5, 10, 10, T.accent_rgb, alpha=6)
    oval(slide, 0.4, H - 6, 7, 7, T.bg2_rgb, alpha=44)
    decorative_dots(slide, 0.38, H * 0.55, 5, 4, 0.14, 0.32, T.accent_rgb, alpha=11)
    diamond(slide, SW * 0.6, H * 0.08, 1.4, 1.4, T.accent_rgb, alpha=8)

    # Icon circle — top section of sidebar
    ic_y = H * 0.16
    ic_bg = oval(slide, SW / 2 - 1.6, ic_y, 3.2, 3.2, T.accent_rgb)
    if ic_bg:
        multi_stop_gradient(ic_bg, [(0, T.accent), (100, T.accent2)], 135)
        shadow(ic_bg, blur=16, dist=5, alpha=0.42)
        glow(ic_bg, T.accent.lstrip('#'), radius=22, alpha=0.22)
    txt(slide, icon, SW / 2 - 1.6, ic_y + 0.32, 3.2, 2.56,
        font="Calibri", size=36, bold=False,
        color=T.text_dark_rgb, align=PP_ALIGN.CENTER, rtl=False)

    # Labels
    label_y = ic_y + 3.4
    fs1 = _smart_font_size(label1, 22, 16, 26, SW - 0.4, 1.2)
    txt(slide, label1, 0.18, label_y, SW - 0.36, 1.15,
        font=_FONT, size=fs1, bold=True,
        color=T.text_light_rgb, align=PP_ALIGN.CENTER, rtl=True)
    if label2:
        txt(slide, label2, 0.18, label_y + 1.2, SW - 0.36, 0.95,
            font=_FONT, size=15, bold=False,
            color=T.muted_rgb, align=PP_ALIGN.CENTER, rtl=True)

    # Decorative divider in sidebar
    hl = rect(slide, 0.45, label_y + 2.38, SW - 0.9, 0.06, T.accent_rgb)
    if hl: multi_stop_gradient(hl, [(0, T.bg), (50, T.accent), (100, T.bg)], 0)
    rect(slide, 0.6, label_y + 2.52, SW - 1.2, 0.03, T.muted_rgb)

    # Content area background
    rect(slide, SW + 0.14, 0, W - SW - 0.14, H, T.bg2_rgb)
    gradient_rect(slide, SW + 0.14, 0, W - SW - 0.14, H, T.grad1, T.bg2, angle=135)

    # Content area decorations
    oval(slide, W - 9, -3.5, 13, 13, T.accent_rgb, alpha=4)
    diamond(slide, W - 5.5, H - 5.5, 4.5, 4.5, T.accent_rgb, alpha=5)


def _section_slide(prs, T, icon, label1, label2=""):
    slide = blank_slide(prs)
    bg(slide, T.bg_rgb)
    _sidebar(slide, T, icon, label1, label2)
    return slide


# ── COVER ─────────────────────────────────────────────────────────────
def make_cover(prs, req: PresentationRequest, T: Theme):
    slide = blank_slide(prs)
    bg(slide, T.bg_rgb)
    gradient_rect(slide, 0, 0, SW + 0.55, H, T.grad2, T.grad1, angle=180)
    sep = rect(slide, SW + 0.55, 0, 0.14, H, T.accent_rgb)
    if sep: gradient_fill(sep, T.accent_grad1, T.accent_grad2, 90)

    oval(slide, -3.5, -3.5, 10, 10, T.accent_rgb, alpha=6)
    oval(slide, 0.4, H - 6, 7.5, 7.5, T.bg2_rgb, alpha=44)
    decorative_dots(slide, 0.38, H * 0.55, 5, 4, 0.14, 0.32, T.accent_rgb, alpha=11)

    ic_bg = oval(slide, SW + 0.55 - 3.5, H * 0.07, 3.5, 3.5, T.accent_rgb)
    if ic_bg:
        multi_stop_gradient(ic_bg, [(0, T.accent), (100, T.accent2)], 135)
        shadow(ic_bg, blur=16, dist=5, alpha=0.44)
        glow(ic_bg, T.accent.lstrip('#'), radius=22, alpha=0.22)
    txt(slide, "🎓", SW + 0.55 - 3.5, H * 0.07 + 0.38, 3.5, 2.78,
        font="Calibri", size=36, bold=False, color=T.text_dark_rgb,
        align=PP_ALIGN.CENTER, rtl=False, vcenter=True)

    if req.institution:
        txt(slide, req.institution, 0.18, H * 0.48, SW + 0.32, 2.3,
            font=_FONT, size=10, bold=False, color=T.muted_rgb,
            align=PP_ALIGN.CENTER, rtl=True, vcenter=True, line_spacing=1.22)
    if req.year:
        yb = rrect(slide, 0.38, H - 1.52, SW - 0.28, 0.68, T.accent_rgb, radius_pct=40)
        if yb: multi_stop_gradient(yb, [(0, T.accent), (100, T.accent2)], 0)
        txt(slide, req.year, 0.38, H - 1.52, SW - 0.28, 0.68,
            font="Calibri", size=13.5, bold=True, color=T.text_dark_rgb,
            align=PP_ALIGN.CENTER, rtl=False, vcenter=True)

    # Content area
    gradient_rect(slide, SW + 0.69, 0, W - SW - 0.69, H, T.grad1, T.bg2, angle=135)
    oval(slide, W - 9, -3.5, 13, 13, T.accent_rgb, alpha=4)
    diamond(slide, W - 5.5, H - 5.5, 4.5, 4.5, T.accent_rgb, alpha=5)

    mcx = SW + 1.05; mcw = W - mcx - 0.75
    tp = rect(slide, mcx - 0.32, 0, mcw + 0.32, 0.40, T.accent_rgb)
    if tp: multi_stop_gradient(tp, [(0, T.bg), (38, T.accent), (62, T.accent2), (100, T.bg)], 0)

    title_y = 0.52; title_h = 7.5
    info_y = title_y + title_h + 0.26
    info_h = H - info_y - 0.38

    tc = rrect(slide, mcx, title_y, mcw, title_h, T.card_rgb, radius_pct=13)
    if tc:
        multi_stop_gradient(tc, [(0, T.card), (100, T.bg2)], 135)
        shadow(tc, blur=24, dist=7, alpha=0.50)
    ct = rrect(slide, mcx, title_y, mcw, 0.34, T.accent_rgb, radius_pct=0)
    if ct: multi_stop_gradient(ct, [(0, T.accent), (50, T.accent2), (100, T.accent)], 0)
    vline(slide, mcx + mcw - 0.22, title_y + 0.34, title_h - 0.34, T.accent_rgb, thickness=0.22)

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
    title_text_h = title_h * (0.57 if has_year else 0.67)
    ts = _smart_font_size(_title_clean, 24, 14, 28, mcw - 0.9, title_text_h)

    txt(slide, _title_clean, mcx + 0.42, title_y + 0.40, mcw - 0.88, title_text_h,
        font=_FONT, size=ts, bold=True, color=T.text_light_rgb,
        align=PP_ALIGN.CENTER, rtl=True, vcenter=True, line_spacing=1.22)

    if req.title_en:
        txt(slide, req.title_en, mcx + 0.42, title_y + title_text_h + 0.30, mcw - 0.88, title_h * 0.14,
            font="Calibri", size=10.5, bold=False, italic=True,
            color=T.muted_rgb, align=PP_ALIGN.CENTER, rtl=False, vcenter=True)

    if has_year:
        yr_y = title_y + title_h * 0.77
        yr_h = title_h * 0.13
        yr_cx = mcx + mcw * 0.2; yr_cw = mcw * 0.60
        yb2 = rrect(slide, yr_cx, yr_y, yr_cw, yr_h, T.accent_rgb, radius_pct=50)
        if yb2: set_solid_alpha(yb2, 26)
        hline(slide, yr_cx + yr_cw * 0.08, yr_y, yr_cw * 0.84, T.accent_rgb, thickness=0.035)
        hline(slide, yr_cx + yr_cw * 0.08, yr_y + yr_h, yr_cw * 0.84, T.accent_rgb, thickness=0.035)
        txt(slide, f'( {_year_str} )', yr_cx, yr_y, yr_cw, yr_h,
            font=_FONT, size=13, bold=False, italic=True,
            color=T.accent_rgb, align=PP_ALIGN.CENTER, rtl=False, vcenter=True)

    hl = rect(slide, mcx + mcw * 0.09, title_y + title_h * 0.92, mcw * 0.82, 0.055, T.accent_rgb)
    if hl: multi_stop_gradient(hl, [(0, T.bg2), (50, T.accent), (100, T.bg2)], 0)

    ic = rrect(slide, mcx, info_y, mcw, info_h, T.card_rgb, radius_pct=12)
    if ic:
        multi_stop_gradient(ic, [(0, T.bg2), (100, T.card)], 135)
        shadow(ic, blur=15, dist=4, alpha=0.35)
    vline(slide, mcx + mcw - 0.2, info_y, info_h, T.accent_rgb, thickness=0.2)

    rows = [("الطالب", req.student_name)]
    if req.supervisor:     rows.append(("المشرف", req.supervisor))
    if req.co_supervisor:  rows.append(("المشرف المساعد", req.co_supervisor))
    if req.specialization: rows.append(("التخصص", req.specialization))

    rh = info_h / max(len(rows), 1)
    for i, (lbl, val) in enumerate(rows):
        y = info_y + i * rh
        rb = rrect(slide, mcx + 0.24, y + 0.05, mcw - 0.60, rh - 0.1, T.bg_rgb, radius_pct=7)
        if rb: set_solid_alpha(rb, 50)
        lbl_w = 4.3; val_w = mcw - lbl_w - 1.0
        lbl_x = mcx + mcw - lbl_w - 0.32
        val_x = mcx + 0.44
        txt(slide, f"{lbl} :", lbl_x, y + 0.05, lbl_w, rh - 0.1,
            font=_FONT, size=max(13, min(15, rh * 8.5)), bold=True,
            color=T.accent_rgb, align=PP_ALIGN.RIGHT, rtl=True, vcenter=True)
        vline(slide, lbl_x - 0.2, y + rh * 0.14, rh * 0.72, T.muted_rgb, thickness=0.045)
        txt(slide, val, val_x, y + 0.05, val_w, rh - 0.1,
            font=_FONT, size=max(14, min(16, rh * 10)), bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.LEFT, rtl=False, vcenter=True)

    bt = rect(slide, 0, H - 0.30, W, 0.30, T.accent_rgb)
    if bt: gradient_fill(bt, T.accent_grad1, T.accent_grad2, 0)
    return slide


# ── INTRO ──────────────────────────────────────────────────────────────
def make_intro(prs, req, T):
    slide = _section_slide(prs, T, "📖", "مقدمة", "البحث")
    CY = 0.30; CH = H - CY - 0.24
    items = []
    if req.intro_overview: items.append(("📖", "نظرة عامة", req.intro_overview))
    if req.intro_approach:  items.append(("🔬", "المنهج المتبع", req.intro_approach))
    if not items: return slide

    n = len(items); gap = 0.28
    cw = (CW - gap * (n - 1)) / n
    CARD_H = min(CH * 0.92, 12.5)
    card_y = CY + (CH - CARD_H) / 2
    ic_s = min(1.7, CARD_H * 0.20)
    ic_y_off = 0.52
    lbl_y_off = ic_y_off + ic_s + 0.28
    div_y_off = lbl_y_off + 0.72 + 0.12
    txt_y_off = div_y_off + 0.12
    txt_h = CARD_H - txt_y_off - 0.42

    for i, (icon, lbl, val) in enumerate(items[:2]):
        x = CX + i * (cw + gap)
        cc = card_with_accent_top(slide, x, card_y, cw, CARD_H, T, radius=12, bar_h=0.30)
        icon_circle(slide, x + cw / 2 - ic_s / 2, card_y + ic_y_off, ic_s,
                    T.accent_grad1, T.accent_grad2, icon, max(14, int(ic_s * 11.5)), T)
        txt(slide, lbl, x + 0.22, card_y + lbl_y_off, cw - 0.44, 0.72,
            font=_FONT, size=SZ_SECTION_LABEL, bold=True, color=T.accent_rgb,
            align=PP_ALIGN.CENTER, rtl=True, vcenter=True)
        section_divider_line(slide, x + cw * 0.12, card_y + div_y_off, cw * 0.76, T)
        fs = adaptive_body_size(val, txt_h, base=13, min_s=10.5, max_s=15)
        txt(slide, val, x + 0.24, card_y + txt_y_off, cw - 0.48, txt_h,
            font=_FONT, size=fs, bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
            rtl=True, vcenter=True, line_spacing=1.32)

    slide_number(slide, 1, getattr(req, '_total_slides', 13), T)
    return slide


# ── PLAN ───────────────────────────────────────────────────────────────
def make_plan(prs, req: PresentationRequest, T: Theme):
    slide = _section_slide(prs, T, "📋", "خطة", "البحث")
    CY = 0.30; CH = H - CY - 0.24
    chapters = req.chapters[:8]; n = len(chapters)
    if not chapters: return slide

    gap = 0.15
    row_h = (CH - gap * (n - 1)) / n

    for i, ch in enumerate(chapters):
        y = CY + i * (row_h + gap)
        even = i % 2 == 0
        rw = rrect(slide, CX, y, CW, row_h,
                   T.card_rgb if even else T.bg2_rgb, radius_pct=10)
        if rw:
            stops = [(0, T.card), (100, T.bg2)] if even else [(0, T.bg2), (100, T.card)]
            multi_stop_gradient(rw, stops, 0)

        acc = rect(slide, CX + CW - 0.24, y, 0.24, row_h, T.accent_rgb)
        if acc: gradient_fill(acc, T.accent_grad1, T.accent_grad2, 90)

        nd = min(0.70, row_h * 0.72)
        nx = CX + CW - 1.82; ny = y + (row_h - nd) / 2
        nc = oval(slide, nx, ny, nd, nd, T.accent_rgb)
        if nc:
            multi_stop_gradient(nc, [(0, T.accent), (100, T.accent2)], 135)
            shadow(nc, blur=7, dist=2, alpha=0.30)
        txt(slide, str(i + 1), nx, ny, nd, nd,
            font="Calibri", size=max(9, int(nd * 11)), bold=True,
            color=T.text_dark_rgb, align=PP_ALIGN.CENTER, rtl=False, vcenter=True)

        fs = _smart_font_size(ch.title, 14, 11, 16, CW - 2.6, row_h)
        txt(slide, ch.title, CX + 0.28, y, CW - 2.56, row_h,
            font=_FONT, size=fs, bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
            rtl=True, vcenter=True, line_spacing=1.15)

        if ch.pages:
            pb = rrect(slide, CX + 0.22, y + (row_h - 0.36) / 2, 1.96, 0.36, T.bg_rgb, radius_pct=40)
            if pb: set_solid_alpha(pb, 55)
            txt(slide, ch.pages, CX + 0.22, y + (row_h - 0.36) / 2, 1.96, 0.36,
                font="Calibri", size=8.5, bold=False,
                color=T.muted_rgb, align=PP_ALIGN.CENTER, rtl=False, vcenter=True)

    slide_number(slide, 2, getattr(req, '_total_slides', 13), T)
    return slide


# ── PROBLEM ────────────────────────────────────────────────────────────
def make_problem(prs, req: PresentationRequest, T: Theme):
    slide = _section_slide(prs, T, "❓", "إشكالية", "البحث")
    CY = 0.36; CH = H - CY - 0.30

    secs = []
    if req.main_problem:  secs.append('p')
    if req.main_question: secs.append('q')
    if req.sub_questions: secs.append('s')

    weights = {'p': 2.8, 'q': 1.6, 's': 2.0}
    tw = sum(weights[s] for s in secs)
    gap = 0.24; avail = CH - gap * (len(secs) - 1)
    cy = CY

    if 'p' in secs:
        h = avail * weights['p'] / tw
        pc = rrect(slide, CX, cy, CW, h, T.card_rgb, radius_pct=12)
        if pc:
            multi_stop_gradient(pc, [(0, T.card), (100, T.bg2)], 135)
            shadow(pc, blur=18, dist=5, alpha=0.42)
            glow(pc, T.accent.lstrip('#'), radius=22, alpha=0.09)
        lb = rrect(slide, CX + CW - 6.4, cy, 6.0, 0.52, T.accent_rgb, radius_pct=0)
        if lb: multi_stop_gradient(lb, [(0, T.accent), (100, T.accent2)], 0)
        txt(slide, "◆  الإشكالية الرئيسية", CX + CW - 6.4, cy, 6.0, 0.52,
            font=_FONT, size=11, bold=True,
            color=T.text_dark_rgb, align=PP_ALIGN.CENTER, rtl=True, vcenter=True)
        txt(slide, "❝", CX + 0.32, cy + 0.60, 1.4, 1.1,
            font="Calibri", size=30, bold=False, color=T.accent_rgb,
            align=PP_ALIGN.LEFT, rtl=False, vcenter=False)
        fs = adaptive_body_size(req.main_problem, h - 0.78, base=12.5, min_s=10.5, max_s=15)
        txt(slide, req.main_problem, CX + 1.88, cy + 0.58, CW - 2.35, h - 0.74,
            font=_FONT, size=fs, bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
            rtl=True, vcenter=True, line_spacing=1.35)
        cy += h + gap

    if 'q' in secs:
        h = avail * weights['q'] / tw
        qc = rrect(slide, CX, cy, CW, h, T.bg2_rgb, radius_pct=10)
        if qc: shadow(qc, blur=8, dist=2, alpha=0.24)
        vline(slide, CX + CW - 0.22, cy, h, T.accent_rgb, thickness=0.22)
        dot = oval(slide, CX + CW - 2.9, cy + h / 2 - 0.20, 0.40, 0.40, T.accent_rgb)
        if dot: multi_stop_gradient(dot, [(0, T.accent), (100, T.accent2)], 135)
        fs = adaptive_body_size(req.main_question, h, base=13, min_s=11, max_s=15.5)
        txt(slide, req.main_question, CX + 0.32, cy, CW - 1.6, h,
            font=_FONT, size=fs, bold=True, italic=True,
            color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
            rtl=True, vcenter=True, line_spacing=1.22)
        cy += h + gap

    if 's' in secs and req.sub_questions:
        h = avail * weights['s'] / tw
        subs = req.sub_questions[:5]
        sub_h = h / len(subs)
        for i, q in enumerate(subs):
            y2 = cy + i * sub_h
            if i % 2 == 0:
                sb = rrect(slide, CX, y2, CW, sub_h - 0.05, T.card_rgb, radius_pct=5)
                if sb: set_solid_alpha(sb, 48)
            nc = oval(slide, CX + CW - 2.62, y2 + (sub_h - 0.35) / 2, 0.35, 0.35, T.accent_rgb)
            if nc: set_solid_alpha(nc, 65)
            txt(slide, str(i + 1), CX + CW - 2.62, y2 + (sub_h - 0.35) / 2, 0.35, 0.35,
                font="Calibri", size=8, bold=True,
                color=T.accent_rgb, align=PP_ALIGN.CENTER, rtl=False, vcenter=True)
            fs = _smart_font_size(q, 12, 10, 13.5, CW - 3.2, sub_h)
            txt(slide, q, CX + 0.32, y2, CW - 3.2, sub_h,
                font=_FONT, size=fs, bold=False,
                color=T.muted_rgb, align=PP_ALIGN.RIGHT, rtl=True, vcenter=True)

    slide_number(slide, 3, getattr(req, '_total_slides', 13), T)
    return slide


# ── OBJECTIVES ─────────────────────────────────────────────────────────
def make_objectives(prs, req: PresentationRequest, T: Theme):
    slide = _section_slide(prs, T, "🎯", "أهداف", "وفرضيات")
    CY = 0.36; CH = H - CY - 0.30
    cols = []
    if req.objectives: cols.append(("🎯  الأهداف", req.objectives))
    if req.hypotheses:  cols.append(("💡  الفرضيات", req.hypotheses))
    if not cols: return slide

    n_c = len(cols); gap = 0.28
    col_w = (CW - gap * (n_c - 1)) / n_c

    for i, (lbl, items) in enumerate(cols):
        x = CX + i * (col_w + gap)
        cc = rrect(slide, x, CY, col_w, CH, T.card_rgb, radius_pct=13)
        if cc:
            multi_stop_gradient(cc, [(0, T.card), (100, T.bg2)], 150)
            shadow(cc, blur=16, dist=5, alpha=0.38)
        hh = 0.72
        hdr = rrect(slide, x, CY, col_w, hh, T.accent_rgb, radius_pct=0)
        if hdr: multi_stop_gradient(hdr, [(0, T.accent2), (100, T.accent)], 0)
        txt(slide, lbl, x + 0.18, CY, col_w - 0.36, hh,
            font=_FONT, size=14, bold=True,
            color=T.text_dark_rgb, align=PP_ALIGN.CENTER, rtl=True, vcenter=True)

        ia = CH - hh - 0.14; n_items = min(len(items), 8); ig = 0.1
        ih = (ia - ig * (n_items - 1)) / n_items

        for j, item in enumerate(items[:8]):
            iy = CY + hh + 0.07 + j * (ih + ig)
            rb = rrect(slide, x + 0.10, iy, col_w - 0.20, ih,
                       T.bg2_rgb if j % 2 == 0 else T.bg_rgb, radius_pct=7)
            if rb: set_solid_alpha(rb, 72)
            number_badge(slide, x + col_w - 0.82, iy + (ih - 0.52) / 2, 0.52, j + 1, T)
            fs = _smart_font_size(item, 12.5, 10, 14, col_w - 1.25, ih)
            txt(slide, item, x + 0.22, iy + 0.05, col_w - 1.24, ih - 0.1,
                font=_FONT, size=fs, bold=False,
                color=T.text_light_rgb, align=PP_ALIGN.RIGHT, rtl=True, vcenter=True)

    slide_number(slide, 4, getattr(req, '_total_slides', 13), T)
    return slide


# ── IMPORTANCE ─────────────────────────────────────────────────────────
def make_importance(prs, req: PresentationRequest, T: Theme):
    slide = _section_slide(prs, T, "⭐", "أهمية", "البحث")
    CY = 0.36; CH = H - CY - 0.30
    items = (req.importance or [])[:6]
    if not items: return slide

    icons = ["⭐", "🔑", "📌", "🌟", "💎", "🏆"]
    cols = 2 if len(items) > 3 else 1
    rows_n = (len(items) + cols - 1) // cols
    gh = 0.20; gv = 0.20
    cw = (CW - gh * (cols - 1)) / cols
    ch = (CH - gv * (rows_n - 1)) / rows_n

    for i, item in enumerate(items):
        ci = i % cols; ri = i // cols
        x = CX + ci * (cw + gh); y = CY + ri * (ch + gv)
        cc = rrect(slide, x, y, cw, ch, T.card_rgb, radius_pct=11)
        if cc:
            multi_stop_gradient(cc, [(0, T.card), (100, T.bg2)], 145)
            shadow(cc, blur=14, dist=4, alpha=0.34)
        acc = rect(slide, x + cw - 0.27, y, 0.27, ch, T.accent_rgb)
        if acc: gradient_fill(acc, T.accent_grad1, T.accent_grad2, 90)

        ic_s = min(1.35, ch * 0.62)
        icon_circle(slide, x + 0.28, y + (ch - ic_s) / 2, ic_s,
                    T.accent_grad1, T.accent_grad2, icons[i % len(icons)],
                    max(13, int(ic_s * 11)), T)
        fs = adaptive_body_size(item, ch - 0.24, base=12.5, min_s=10, max_s=14)
        txt(slide, item, x + ic_s + 0.54, y + 0.12, cw - ic_s - 1.06, ch - 0.24,
            font=_FONT, size=fs, bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
            rtl=True, vcenter=True, line_spacing=1.3)

    slide_number(slide, 5, getattr(req, '_total_slides', 13), T)
    return slide


# ── METHODOLOGY ────────────────────────────────────────────────────────
def make_methodology(prs, req: PresentationRequest, T: Theme):
    slide = _section_slide(prs, T, "🔬", "منهجية", "البحث")
    CY = 0.36; CH = H - CY - 0.30
    icons_map = {"المنهج": "📊", "العينة": "👥", "حجم العينة": "📏", "الأداة": "🛠️"}
    fields = []
    if req.methodology: fields.append(("المنهج", req.methodology))
    if req.sample_type:  fields.append(("العينة", req.sample_type))
    if req.sample_size:  fields.append(("حجم العينة", req.sample_size))
    if req.tool:         fields.append(("الأداة", req.tool))
    if not fields: return slide

    cols = 2 if len(fields) > 2 else len(fields)
    rows_n = (len(fields) + cols - 1) // cols
    gh = 0.24; gv = 0.22
    cw = (CW - gh * (cols - 1)) / cols
    ch = (CH - gv * (rows_n - 1)) / rows_n

    for i, (lbl, val) in enumerate(fields[:4]):
        ci = i % cols; ri = i // cols
        x = CX + ci * (cw + gh); y = CY + ri * (ch + gv)
        cc = card_with_accent_top(slide, x, y, cw, ch, T, radius=12, bar_h=0.28)
        if cc: shadow(cc, blur=14, dist=4, alpha=0.38)

        ic_s = min(1.85, ch * 0.36)
        ic_x = x + cw / 2 - ic_s / 2
        ic_bg = oval(slide, ic_x, y + 0.38, ic_s, ic_s, T.accent_rgb)
        if ic_bg:
            multi_stop_gradient(ic_bg, [(0, T.accent), (100, T.accent2)], 135)
            shadow(ic_bg, blur=10, dist=3, alpha=0.30)
            glow(ic_bg, T.accent.lstrip('#'), radius=15, alpha=0.18)
        txt(slide, icons_map.get(lbl, "📌"), ic_x, y + 0.42, ic_s, ic_s * 0.86,
            font="Calibri", size=max(14, int(ic_s * 10.5)), bold=False,
            color=T.text_dark_rgb, align=PP_ALIGN.CENTER, rtl=False, vcenter=True)

        lbl_y = y + ic_s + 0.56
        txt(slide, lbl, x + 0.18, lbl_y, cw - 0.36, 0.64,
            font=_FONT, size=13, bold=True, color=T.accent_rgb,
            align=PP_ALIGN.CENTER, rtl=True, vcenter=True)
        section_divider_line(slide, x + cw * 0.14, lbl_y + 0.66, cw * 0.72, T)

        remain = ch - (lbl_y - y) - 0.90
        fs = adaptive_body_size(val, remain, base=12.5, min_s=10, max_s=14)
        txt(slide, val, x + 0.20, lbl_y + 0.78, cw - 0.40, remain,
            font=_FONT, size=fs, bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.CENTER,
            rtl=True, vcenter=True, line_spacing=1.25)

    slide_number(slide, 6, getattr(req, '_total_slides', 13), T)
    return slide


# ── STATS ★ ────────────────────────────────────────────────────────────
def make_stats(prs, req: PresentationRequest, T: Theme):
    slide = _section_slide(prs, T, "📈", "الأرقام", "الرئيسية")
    CY = 0.36; CH = H - CY - 0.30
    stats = req.stats[:6]
    if not stats: return slide

    cols = 3 if len(stats) >= 3 else len(stats)
    rows_n = (len(stats) + cols - 1) // cols
    gh = 0.24; gv = 0.22
    cw = (CW - gh * (cols - 1)) / cols
    ch = (CH - gv * (rows_n - 1)) / rows_n

    for i, stat in enumerate(stats):
        ci = i % cols; ri = i // cols
        x = CX + ci * (cw + gh); y = CY + ri * (ch + gv)
        kpi_card(slide, x, y, cw, ch, T,
                 value=stat.value, label=stat.label,
                 unit=getattr(stat, 'unit', ''), font=_FONT)

    slide_number(slide, 7, getattr(req, '_total_slides', 13), T)
    return slide


# ── RESULTS ★ ──────────────────────────────────────────────────────────
def make_results(prs, req: PresentationRequest, T: Theme):
    slide = _section_slide(prs, T, "📊", "نتائج", "البحث")
    CY = 0.36; CH = H - CY - 0.30
    results = req.main_results[:8]; n = len(results)
    if not results: return slide

    gap = 0.15
    row_h = (CH - gap * (n - 1)) / n

    for i, result in enumerate(results):
        y = CY + i * (row_h + gap)
        highlight = (i < 2 and n >= 3)
        result_row(slide, CX, y, CW, row_h, T, result, i + 1,
                   font=_FONT, highlight=highlight)

    slide_number(slide, 8, getattr(req, '_total_slides', 13), T)
    return slide


# ── CONCLUSION ─────────────────────────────────────────────────────────
def make_conclusion(prs, req: PresentationRequest, T: Theme):
    slide = _section_slide(prs, T, "💡", "خاتمة", "البحث")
    CY = 0.30; CH = H - CY - 0.24

    og = rrect(slide, CX - 0.12, CY - 0.12, CW + 0.24, CH + 0.24, T.accent_rgb, radius_pct=16)
    if og: set_solid_alpha(og, 11)

    cc = rrect(slide, CX, CY, CW, CH, T.card_rgb, radius_pct=14)
    if cc:
        multi_stop_gradient(cc, [(0, T.card), (50, T.bg2), (100, T.card)], 135)
        shadow(cc, blur=24, dist=7, alpha=0.46)

    tp = rrect(slide, CX, CY, CW, 0.32, T.accent_rgb, radius_pct=0)
    if tp:
        multi_stop_gradient(tp, [(0, T.accent2), (50, T.accent), (100, T.accent2)], 0)
        glow(tp, T.accent.lstrip('#'), radius=12, alpha=0.30)

    diamond(slide, CX + 0.30, CY + 0.46, 1.0, 1.0, T.accent_rgb, alpha=12)

    txt(slide, "❝", CX + 0.34, CY + 0.45, 1.65, 1.5,
        font="Calibri", size=48, bold=False, color=T.accent_rgb,
        align=PP_ALIGN.LEFT, rtl=False, vcenter=False)

    fs = adaptive_body_size(req.general_conclusion, CH - 2.25, base=13, min_s=11, max_s=16)
    txt(slide, req.general_conclusion, CX + 0.34, CY + 1.36, CW - 0.95, CH - 2.20,
        font=_FONT, size=fs, bold=False,
        color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
        rtl=True, vcenter=True, line_spacing=1.38)

    ny = CY + CH - 0.92
    hl = rect(slide, CX + CW * 0.18, ny, CW * 0.64, 0.06, T.accent_rgb)
    if hl: multi_stop_gradient(hl, [(0, T.bg2), (50, T.accent), (100, T.bg2)], 0)
    txt(slide, req.student_name, CX, ny + 0.12, CW, 0.72,
        font=_FONT, size=13.5, bold=True, color=T.accent_rgb,
        align=PP_ALIGN.CENTER, rtl=True, vcenter=True)

    slide_number(slide, 9, getattr(req, '_total_slides', 13), T)
    return slide


# ── RECOMMENDATIONS ────────────────────────────────────────────────────
def make_recommendations(prs, req: PresentationRequest, T: Theme):
    slide = _section_slide(prs, T, "✅", "توصيات", "البحث")
    CY = 0.36; CH = H - CY - 0.30
    recs = req.recommendations[:8]; n = len(recs)
    if not recs: return slide
    gap = 0.15
    row_h = (CH - gap * (n - 1)) / n

    for i, rec in enumerate(recs):
        y = CY + i * (row_h + gap)
        rw = rrect(slide, CX, y, CW, row_h, T.card_rgb, radius_pct=9)
        if rw:
            multi_stop_gradient(rw, [(0, T.card), (100, T.bg2)], 0)
            shadow(rw, blur=5, dist=2, alpha=0.20)
        dot = oval(slide, CX + CW - 1.88, y + (row_h - 0.38) / 2, 0.38, 0.38, T.accent_rgb)
        if dot: multi_stop_gradient(dot, [(0, T.accent), (100, T.accent2)], 135)
        acc = rect(slide, CX + CW - 0.26, y, 0.26, row_h, T.accent_rgb)
        if acc: gradient_fill(acc, T.accent_grad1, T.accent_grad2, 90)
        fs = _smart_font_size(rec, 13, 10.5, 14.5, CW - 2.4, row_h)
        txt(slide, rec, CX + 0.28, y + 0.07, CW - 2.38, row_h - 0.14,
            font=_FONT, size=fs, bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.RIGHT, rtl=True, vcenter=True)

    slide_number(slide, 10, getattr(req, '_total_slides', 13), T)
    return slide


# ── FUTURE ─────────────────────────────────────────────────────────────
def make_future(prs, req: PresentationRequest, T: Theme):
    slide = _section_slide(prs, T, "🔭", "آفاق", "مستقبلية")
    CY = 0.36; CH = H - CY - 0.30
    items = req.future_work[:6]
    if not items: return slide
    cols = 2 if len(items) > 3 else 1
    rows_n = (len(items) + cols - 1) // cols
    gh = 0.24; gv = 0.20
    cw = (CW - gh * (cols - 1)) / cols
    ch = (CH - gv * (rows_n - 1)) / rows_n

    for i, item in enumerate(items):
        ci = i % cols; ri = i // cols
        x = CX + ci * (cw + gh); y = CY + ri * (ch + gv)
        cc = rrect(slide, x, y, cw, ch, T.card_rgb, radius_pct=11)
        if cc:
            multi_stop_gradient(cc, [(0, T.card), (70, T.bg2), (100, T.bg)], 155)
            shadow(cc, blur=13, dist=4, alpha=0.34)
        tp = rrect(slide, x, y, cw, 0.28, T.accent_rgb, radius_pct=0)
        if tp: multi_stop_gradient(tp, [(0, T.accent), (100, T.accent2)], 0)
        nd = min(0.86, ch * 0.30)
        number_badge(slide, x + cw / 2 - nd / 2, y + 0.40, nd, i + 1, T)
        section_divider_line(slide, x + cw * 0.16, y + nd + 0.54, cw * 0.68, T)
        fs = adaptive_body_size(item, ch - nd - 0.86, base=12.5, min_s=10, max_s=14)
        txt(slide, item, x + 0.26, y + nd + 0.70, cw - 0.52, ch - nd - 0.88,
            font=_FONT, size=fs, bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.CENTER,
            rtl=True, vcenter=True, line_spacing=1.30)

    slide_number(slide, 11, getattr(req, '_total_slides', 13), T)
    return slide


# ── REFERENCES ─────────────────────────────────────────────────────────
def make_references(prs, req: PresentationRequest, T: Theme):
    slide = _section_slide(prs, T, "📚", "المراجع", "والمصادر")
    CY = 0.36; CH = H - CY - 0.30
    refs = req.references[:12]; n = len(refs)
    if not refs: return slide
    gap = 0.11
    row_h = min((CH - gap * (n - 1)) / n, 1.40)
    total_h = n * (row_h + gap) - gap
    sy = CY + (CH - total_h) / 2

    for i, ref in enumerate(refs):
        y = sy + i * (row_h + gap)
        if y + row_h > H - 0.20: break
        even = i % 2 == 0
        rw = rrect(slide, CX, y, CW, row_h,
                   T.card_rgb if even else T.bg2_rgb, radius_pct=5)
        if rw:
            stops = [(0, T.card), (100, T.bg2)] if even else [(0, T.bg2), (100, T.card)]
            multi_stop_gradient(rw, stops, 0)
        acc = rect(slide, CX + CW - 0.24, y, 0.24, row_h, T.accent_rgb)
        if acc: set_solid_alpha(acc, 52)
        nb = rrect(slide, CX + 0.10, y + (row_h - 0.38) / 2, 0.72, 0.38, T.bg_rgb, radius_pct=40)
        if nb: set_solid_alpha(nb, 62)
        txt(slide, f"[{i+1}]", CX + 0.10, y + (row_h - 0.38) / 2, 0.72, 0.38,
            font="Calibri", size=9, bold=True, color=T.accent_rgb,
            align=PP_ALIGN.CENTER, rtl=False, vcenter=True)
        fs = _smart_font_size(ref, 11.5, 9.5, 13, CW - 1.5, row_h)
        txt(slide, ref, CX + 0.94, y + 0.04, CW - 1.44, row_h - 0.08,
            font=_FONT, size=fs, bold=False,
            color=T.text_light_rgb, align=PP_ALIGN.RIGHT,
            rtl=True, vcenter=True, line_spacing=1.15)

    slide_number(slide, 12, getattr(req, '_total_slides', 13), T)
    return slide


# ── FINAL ──────────────────────────────────────────────────────────────
def make_final(prs, req: PresentationRequest, T: Theme):
    slide = blank_slide(prs)
    bg(slide, T.bg_rgb)
    gradient_rect(slide, 0, 0, W, H, T.grad1, T.grad2, angle=135)

    # Sidebar
    gradient_rect(slide, 0, 0, SW + 0.55, H, T.grad2, T.grad1, angle=180)
    sepc = rect(slide, SW + 0.55, 0, 0.14, H, T.accent_rgb)
    if sepc: gradient_fill(sepc, T.accent_grad1, T.accent_grad2, 90)
    oval(slide, -3.5, -3.5, 10, 10, T.accent_rgb, alpha=6)
    oval(slide, 0.4, H - 6, 7.5, 7.5, T.bg2_rgb, alpha=42)
    decorative_dots(slide, 0.38, H * 0.55, 4, 3, 0.14, 0.32, T.accent_rgb, alpha=10)
    txt(slide, "✦", SW / 2 - 1.0, H * 0.26, 2.0, 2.0,
        font="Calibri", size=30, bold=False, color=T.accent_rgb,
        align=PP_ALIGN.CENTER, rtl=False, vcenter=True)
    if req.institution:
        txt(slide, req.institution, 0.18, H * 0.52, SW + 0.28, 1.3,
            font=_FONT, size=10, bold=False, color=T.muted_rgb,
            align=PP_ALIGN.CENTER, rtl=True, vcenter=True)
    if req.year:
        yb = rrect(slide, 0.38, H - 1.55, SW - 0.28, 0.68, T.accent_rgb, radius_pct=40)
        if yb: multi_stop_gradient(yb, [(0, T.accent), (100, T.accent2)], 0)
        txt(slide, req.year, 0.38, H - 1.55, SW - 0.28, 0.68,
            font="Calibri", size=13.5, bold=True, color=T.text_dark_rgb,
            align=PP_ALIGN.CENTER, rtl=False, vcenter=True)

    # Content area
    gradient_rect(slide, SW + 0.69, 0, W - SW - 0.69, H, T.grad1, T.bg2, angle=135)
    oval(slide, W - 9, -3.5, 13, 13, T.accent_rgb, alpha=4)
    diamond(slide, W - 5.5, H - 5.5, 4.5, 4.5, T.accent_rgb, alpha=5)

    mcx = SW + 1.05; mcw = W - mcx - 0.75
    ccy = H * 0.05; cch = H * 0.90

    og = rrect(slide, mcx - 0.14, ccy - 0.14, mcw + 0.28, cch + 0.28, T.accent_rgb, radius_pct=18)
    if og: set_solid_alpha(og, 13)

    cc = rrect(slide, mcx, ccy, mcw, cch, T.card_rgb, radius_pct=16)
    if cc:
        multi_stop_gradient(cc, [(0, T.card), (50, T.bg2), (100, T.card)], 135)
        shadow(cc, blur=32, dist=10, alpha=0.54)

    tp = rrect(slide, mcx, ccy, mcw, 0.44, T.accent_rgb, radius_pct=0)
    if tp:
        multi_stop_gradient(tp, [(0, T.bg), (28, T.accent2), (50, T.accent),
                                  (72, T.accent2), (100, T.bg)], 0)
        glow(tp, T.accent.lstrip('#'), radius=18, alpha=0.38)

    bp = rrect(slide, mcx, ccy + cch - 0.28, mcw, 0.28, T.accent_rgb, radius_pct=0)
    if bp: set_solid_alpha(bp, 46)

    txt(slide, "✦", mcx + mcw / 2 - 0.78, ccy + 0.54, 1.56, 1.3,
        font="Calibri", size=24, bold=False, color=T.accent_rgb,
        align=PP_ALIGN.CENTER, rtl=False, vcenter=True)

    txt(slide, "شكراً وتقديراً", mcx + 0.7, ccy + 1.12, mcw - 1.4, cch * 0.28,
        font=_FONT, size=SZ_FINAL_TITLE, bold=True, color=T.text_light_rgb,
        align=PP_ALIGN.CENTER, rtl=True, vcenter=True, line_spacing=1.08)

    d1 = rect(slide, mcx + mcw * 0.13, ccy + cch * 0.40, mcw * 0.74, 0.07, T.accent_rgb)
    if d1: multi_stop_gradient(d1, [(0, T.bg2), (50, T.accent), (100, T.bg2)], 0)
    rect(slide, mcx + mcw * 0.23, ccy + cch * 0.40 + 0.14, mcw * 0.54, 0.033, T.muted_rgb)

    txt(slide, req.student_name, mcx + 0.7, ccy + cch * 0.44, mcw - 1.4, cch * 0.15,
        font=_FONT, size=SZ_FINAL_SUB, bold=True, color=T.accent_rgb,
        align=PP_ALIGN.CENTER, rtl=True, vcenter=True)

    ts = req.title_ar[:66] + ("..." if len(req.title_ar) > 66 else "")
    txt(slide, ts, mcx + 1.0, ccy + cch * 0.60, mcw - 2.0, cch * 0.20,
        font=_FONT, size=11.5, bold=False, italic=True, color=T.muted_rgb,
        align=PP_ALIGN.CENTER, rtl=True, vcenter=True, line_spacing=1.28)

    footer = []
    if req.institution: footer.append(req.institution)
    if req.year: footer.append(req.year)
    if footer:
        fb = rrect(slide, mcx + mcw * 0.1, ccy + cch * 0.84, mcw * 0.8, 0.64, T.bg_rgb, radius_pct=40)
        if fb: set_solid_alpha(fb, 50)
        txt(slide, "  ·  ".join(footer), mcx + 0.8, ccy + cch * 0.84, mcw - 1.6, 0.64,
            font=_FONT, size=SZ_BODY, bold=False, color=T.muted_rgb,
            align=PP_ALIGN.CENTER, rtl=True, vcenter=True)

    bt = rect(slide, 0, H - 0.30, W, 0.30, T.accent_rgb)
    if bt: multi_stop_gradient(bt, [(0, T.bg), (30, T.accent), (70, T.accent2), (100, T.bg)], 0)
    return slide
