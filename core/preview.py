"""
core/preview.py v7 — محسّن بالكامل لـ Render.com (بدون LibreOffice)
يستخدم Pillow renderer متقدم مع دعم كامل للأشكال والصور والتدرجات
"""
import base64
import hashlib
import hmac
import io
import logging
import os
import secrets
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

log = logging.getLogger(__name__)

# ─── Storage & Security ───────────────────────────────────────────────────────
_preview_store: Dict[str, dict] = {}
_store_lock = threading.Lock()

PREVIEW_TTL = 3 * 3600
MAX_PREVIEW_SLIDES = 999
SLIDE_QUALITY_DPI = 150
WATERMARK_TEXT = "مذكرتي Pro — معاينة فقط"

# ─── Session Management ───────────────────────────────────────────────────────

def create_preview_session(presentation_id: str) -> str:
    token = secrets.token_urlsafe(32)
    with _store_lock:
        _preview_store[presentation_id] = {
            "token": token,
            "slides": [],
            "status": "pending",
            "created_at": time.time(),
            "slide_count": 0,
        }
    return token


def get_preview_session(presentation_id: str) -> Optional[dict]:
    _cleanup_expired()
    with _store_lock:
        return _preview_store.get(presentation_id)


def get_preview_slides(presentation_id: str, token: str) -> Optional[List[str]]:
    session = get_preview_session(presentation_id)
    if not session:
        return None
    if not hmac.compare_digest(session["token"], token):
        log.warning(f"Invalid token for preview {presentation_id}")
        return None
    return session.get("slides", [])


def set_preview_ready(presentation_id: str, slides: List[str]):
    with _store_lock:
        if presentation_id in _preview_store:
            _preview_store[presentation_id]["slides"] = slides
            _preview_store[presentation_id]["status"] = "ready"
            _preview_store[presentation_id]["slide_count"] = len(slides)


def set_preview_error(presentation_id: str, msg: str):
    with _store_lock:
        if presentation_id in _preview_store:
            _preview_store[presentation_id]["status"] = "error"
            _preview_store[presentation_id]["error"] = msg


def _cleanup_expired():
    now = time.time()
    with _store_lock:
        expired = [k for k, v in _preview_store.items()
                   if now - v.get("created_at", 0) > PREVIEW_TTL]
        for k in expired:
            del _preview_store[k]


# ─── Font Management ──────────────────────────────────────────────────────────

CAIRO_PATHS = [
    os.path.expanduser("~/.fonts/cairo/Cairo-Bold.ttf"),
    os.path.expanduser("~/.fonts/cairo/Cairo.ttf"),
    "/root/.fonts/cairo/Cairo-Bold.ttf",
    "/root/.fonts/cairo/Cairo.ttf",
    "/tmp/fonts/cairo/Cairo.ttf",
    "/opt/render/project/src/.fonts/cairo/Cairo.ttf",
]
FALLBACK_FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
]

_font_cache = {}

def _find_font(size=16, bold=False):
    from PIL import ImageFont
    key = (size, bold)
    if key in _font_cache:
        return _font_cache[key]
    for p in CAIRO_PATHS:
        if os.path.exists(p):
            try:
                f = ImageFont.truetype(p, size)
                _font_cache[key] = f
                return f
            except:
                pass
    for p in FALLBACK_FONTS:
        if os.path.exists(p):
            try:
                f = ImageFont.truetype(p, size)
                _font_cache[key] = f
                return f
            except:
                pass
    f = ImageFont.load_default()
    _font_cache[key] = f
    return f


# ─── Color Utilities ──────────────────────────────────────────────────────────

def _hex_to_rgb(h) -> tuple:
    h = str(h).lstrip("#")
    if len(h) == 6:
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    if len(h) == 8:  # ARGB
        return (int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16))
    return (200, 200, 200)


def _read_color_xml(elem) -> Optional[tuple]:
    if elem is None:
        return None
    try:
        for child in elem.iter():
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if tag == 'srgbClr':
                val = child.get('val', '')
                if val:
                    return _hex_to_rgb(val)
            elif tag == 'sysClr':
                val = child.get('lastClr', '')
                if val:
                    return _hex_to_rgb(val)
            elif tag == 'prstClr':
                prstMap = {
                    'white': (255, 255, 255), 'black': (0, 0, 0),
                    'red': (255, 0, 0), 'blue': (0, 0, 255),
                    'green': (0, 128, 0), 'yellow': (255, 255, 0),
                    'orange': (255, 165, 0), 'purple': (128, 0, 128),
                    'gray': (128, 128, 128), 'grey': (128, 128, 128),
                    'darkBlue': (0, 0, 139), 'darkGray': (169, 169, 169),
                    'ltGray': (211, 211, 211),
                }
                return prstMap.get(child.get('val', ''), (128, 128, 128))
    except:
        pass
    return None


def _smart_text_color(bg: tuple) -> tuple:
    lum = 0.299 * bg[0] + 0.587 * bg[1] + 0.114 * bg[2]
    return (255, 255, 255) if lum < 128 else (20, 20, 20)


def _blend(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


# ─── Background Rendering ─────────────────────────────────────────────────────

def _get_slide_bg(slide) -> tuple:
    """استخرج لون خلفية الشريحة"""
    try:
        fill = slide.background.fill
        if fill.type is not None:
            try:
                c = fill.fore_color.rgb
                return (c.r, c.g, c.b)
            except:
                pass
    except:
        pass
    try:
        bg_elem = slide.background._element
        c = _read_color_xml(bg_elem)
        if c:
            return c
    except:
        pass
    return (255, 255, 255)


def _render_background(img, slide, W, H):
    """رسم خلفية الشريحة مع دعم التدرجات والصور"""
    from PIL import Image, ImageDraw
    try:
        from lxml import etree
        ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'
        bg_elem = slide.background._element

        # محاولة تدرج
        grad = bg_elem.find(f'.//{{{ns}}}gradFill')
        if grad is not None:
            stops = []
            for gs in grad.findall(f'.//{{{ns}}}gs'):
                pos = int(gs.get('pos', '0')) / 100000.0
                c = _read_color_xml(gs)
                if c:
                    stops.append((pos, c))
            if len(stops) >= 2:
                stops = sorted(stops, key=lambda x: x[0])
                # رسم تدرج عمودي
                draw = ImageDraw.Draw(img)
                for y in range(H):
                    t = y / H
                    c1 = stops[0][1]
                    for i in range(len(stops) - 1):
                        p0, col0 = stops[i]
                        p1, col1 = stops[i + 1]
                        if p0 <= t <= p1:
                            lt = (t - p0) / (p1 - p0) if p1 > p0 else 0
                            c1 = _blend(col0, col1, lt)
                            break
                    draw.line([(0, y), (W, y)], fill=c1)
                return

        # لون صلب
        bg_color = _get_slide_bg(slide)
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, W, H], fill=bg_color)

    except Exception as e:
        log.debug(f"BG render error: {e}")
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, W, H], fill=(255, 255, 255))


# ─── Shape Fill & Color Extraction ───────────────────────────────────────────

def _get_shape_fill(shape) -> Optional[tuple]:
    """استخرج لون تعبئة الشكل"""
    try:
        from pptx.enum.dml import MSO_FILL
        fill = shape.fill
        if hasattr(MSO_FILL, 'BACKGROUND') and fill.type == MSO_FILL.BACKGROUND:
            return None
        if fill.type is not None and fill.type != 5:
            try:
                c = fill.fore_color.rgb
                return (c.r, c.g, c.b)
            except:
                pass
    except:
        pass
    try:
        ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'
        solid = shape._element.find(f'.//{{{ns}}}solidFill')
        if solid is not None:
            return _read_color_xml(solid)
    except:
        pass
    return None


def _get_text_color(run) -> Optional[tuple]:
    """استخرج لون النص"""
    try:
        rgb = run.font.color.rgb
        return (rgb.r, rgb.g, rgb.b)
    except:
        pass
    try:
        ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'
        r_elem = run._r
        rPr = r_elem.find(f'{{{ns}}}rPr')
        if rPr is not None:
            solid = rPr.find(f'{{{ns}}}solidFill')
            if solid is not None:
                return _read_color_xml(solid)
    except:
        pass
    return None


def _get_para_color(para) -> Optional[tuple]:
    """استخرج لون النص من مستوى الفقرة"""
    try:
        ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'
        pPr = para._p.find(f'{{{ns}}}pPr')
        if pPr is not None:
            solid = pPr.find(f'.//{{{ns}}}solidFill')
            if solid is not None:
                return _read_color_xml(solid)
    except:
        pass
    return None


def _emu_to_px(emu, dpi=96) -> int:
    return max(0, int(emu / 914400 * dpi))


# ─── Text Wrapping ────────────────────────────────────────────────────────────

def _measure_text(text, font):
    from PIL import ImageDraw, Image
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    try:
        bb = d.textbbox((0, 0), text, font=font)
        return bb[2] - bb[0], bb[3] - bb[1]
    except:
        return len(text) * 8, 16


def _wrap_text(text, font, max_w) -> List[str]:
    if max_w <= 20 or not text.strip():
        return [text] if text.strip() else []
    
    tw, _ = _measure_text(text, font)
    if tw <= max_w:
        return [text]
    
    # تقسيم بالكلمات (مع دعم العربية التي لا تستخدم مسافات أحياناً)
    words = text.split()
    if not words:
        return [text]
    
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        tw2, _ = _measure_text(test, font)
        if tw2 <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [text]


# ─── Shape Rendering ──────────────────────────────────────────────────────────

def _render_shape(draw, img, shape, W, H, slide_bg):
    """رسم شكل واحد بشكل كامل"""
    try:
        EMU = 914400.0
        DPI = 96
        L = int((shape.left or 0) / EMU * DPI)
        T = int((shape.top or 0) / EMU * DPI)
        SW = int((shape.width or 0) / EMU * DPI)
        SH = int((shape.height or 0) / EMU * DPI)

        # ── رسم الصورة ──────────────────────────────────────────
        try:
            from pptx.enum.shapes import MSO_SHAPE_TYPE
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                try:
                    from PIL import Image as PILImage
                    img_bytes = shape.image.blob
                    pic = PILImage.open(io.BytesIO(img_bytes)).convert("RGBA")
                    pic = pic.resize((max(1, SW), max(1, SH)), PILImage.LANCZOS)
                    img.paste(pic, (L, T), pic if pic.mode == 'RGBA' else None)
                    return
                except Exception as e:
                    log.debug(f"Image render error: {e}")
                    draw.rectangle([L, T, L+SW, T+SH], fill=(220, 220, 220))
                    return
        except:
            pass

        # ── رسم الجدول ──────────────────────────────────────────
        try:
            if shape.has_table:
                _render_table(draw, shape, L, T, SW, SH, slide_bg)
                return
        except:
            pass

        # ── رسم الشكل العادي (مستطيل/دائرة/مثلث) ───────────────
        fc = _get_shape_fill(shape)
        
        # رسم الخلفية
        if fc and SW > 0 and SH > 0:
            try:
                from pptx.enum.shapes import MSO_SHAPE_TYPE
                # تحقق من نوع الشكل
                shape_name = shape.name.lower()
                
                # شكل مستدير
                if 'round' in shape_name or 'circle' in shape_name or 'oval' in shape_name:
                    _draw_rounded_rect(draw, L, T, L+SW, T+SH, radius=min(SW,SH)//2, fill=fc)
                else:
                    draw.rectangle([L, T, L+SW, T+SH], fill=fc)
            except:
                draw.rectangle([L, T, L+SW, T+SH], fill=fc)

        # ── رسم النص ─────────────────────────────────────────────
        if not shape.has_text_frame:
            return
        
        bg_for_text = fc if fc else slide_bg
        default_color = _smart_text_color(bg_for_text)
        
        # حساب padding
        pad_l = max(4, int(SW * 0.03))
        pad_t = max(4, int(SH * 0.03))
        
        y = T + pad_t
        
        for para in shape.text_frame.paragraphs:
            full_text = para.text.strip()
            if not full_text:
                y += 6
                continue
            
            # استخرج إعدادات النص
            fs = 14
            tc = None
            bold = False
            italic = False
            
            para_color = _get_para_color(para)
            if para_color:
                tc = para_color
            
            for run in para.runs:
                try:
                    if run.font.size and run.font.size > 0:
                        fs = max(7, min(int(run.font.size / 12700), 72))
                    if run.font.bold:
                        bold = True
                    if run.font.italic:
                        italic = True
                    rc = _get_text_color(run)
                    if rc:
                        tc = rc
                except:
                    pass
                break
            
            if tc is None:
                tc = default_color
            
            # تعديل الحجم بناءً على حجم الشريحة
            scale = min(W / 1280, H / 720)
            fs = max(7, int(fs * scale))
            
            font = _find_font(fs, bold)
            
            # محاذاة النص
            align = 'right'  # افتراضي للعربية
            try:
                from pptx.enum.text import PP_ALIGN
                if para.alignment == PP_ALIGN.LEFT:
                    align = 'left'
                elif para.alignment == PP_ALIGN.CENTER:
                    align = 'center'
                elif para.alignment == PP_ALIGN.RIGHT:
                    align = 'right'
            except:
                pass
            
            available_w = SW - pad_l * 2
            lines = _wrap_text(full_text, font, available_w)
            
            for line in lines:
                if y >= T + SH - 4:
                    break
                
                tw, th = _measure_text(line, font)
                
                if align == 'center':
                    x = L + (SW - tw) // 2
                elif align == 'left':
                    x = L + pad_l
                else:  # right
                    x = L + SW - tw - pad_l
                
                # ظل خفيف للنص لتحسين القراءة
                shadow_c = tuple(max(0, c - 80) for c in tc) if sum(tc) > 128*3 else tuple(min(255, c + 80) for c in tc)
                try:
                    draw.text((x+1, y+1), line, fill=shadow_c + (100,) if len(shadow_c) == 3 else shadow_c, font=font)
                except:
                    pass
                draw.text((x, y), line, fill=tc, font=font)
                y += th + 3
            
            # مسافة بين الفقرات
            y += 2

    except Exception as e:
        log.debug(f"Shape render error: {e}")


def _draw_rounded_rect(draw, x1, y1, x2, y2, radius=10, fill=None):
    """رسم مستطيل بزوايا مدورة"""
    r = min(radius, (x2-x1)//2, (y2-y1)//2)
    if r <= 0:
        draw.rectangle([x1, y1, x2, y2], fill=fill)
        return
    draw.rectangle([x1+r, y1, x2-r, y2], fill=fill)
    draw.rectangle([x1, y1+r, x2, y2-r], fill=fill)
    draw.ellipse([x1, y1, x1+2*r, y1+2*r], fill=fill)
    draw.ellipse([x2-2*r, y1, x2, y1+2*r], fill=fill)
    draw.ellipse([x1, y2-2*r, x1+2*r, y2], fill=fill)
    draw.ellipse([x2-2*r, y2-2*r, x2, y2], fill=fill)


def _render_table(draw, shape, L, T, SW, SH, slide_bg):
    """رسم جدول"""
    try:
        table = shape.table
        rows = len(table.rows)
        cols = len(table.columns)
        if rows == 0 or cols == 0:
            return
        
        cell_h = SH // rows
        cell_w = SW // cols
        
        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                cx = L + c_idx * cell_w
                cy = T + r_idx * cell_h
                cw = cell_w
                ch = cell_h
                
                # لون خلية
                cell_fill = None
                try:
                    cf = cell.fill
                    if cf.type is not None:
                        rgb = cf.fore_color.rgb
                        cell_fill = (rgb.r, rgb.g, rgb.b)
                except:
                    pass
                
                if r_idx == 0:  # صف الرأس
                    fill_c = cell_fill or (30, 60, 120)
                elif r_idx % 2 == 0:
                    fill_c = cell_fill or (240, 245, 255)
                else:
                    fill_c = cell_fill or (255, 255, 255)
                
                draw.rectangle([cx, cy, cx+cw, cy+ch], fill=fill_c, outline=(180, 180, 200))
                
                # نص الخلية
                txt = cell.text.strip()
                if txt:
                    fs = max(8, min(14, cell_h // 3))
                    font = _find_font(fs, r_idx == 0)
                    tc = _smart_text_color(fill_c)
                    tw, th = _measure_text(txt, font)
                    tx = cx + (cw - tw) // 2
                    ty = cy + (ch - th) // 2
                    draw.text((tx, ty), txt, fill=tc, font=font)
    except Exception as e:
        log.debug(f"Table render error: {e}")


# ─── Main Slide Renderer ──────────────────────────────────────────────────────

def _render_slide(slide, W: int, H: int) -> bytes:
    """يرسم شريحة كاملة بالـ Pillow ويُرجع bytes (WebP)"""
    from PIL import Image, ImageDraw
    
    img = Image.new("RGB", (W, H), (255, 255, 255))
    
    # رسم الخلفية
    _render_background(img, slide, W, H)
    
    draw = ImageDraw.Draw(img)
    slide_bg = _get_slide_bg(slide)
    
    # ترتيب الأشكال بحسب Z-order (الطبقات)
    shapes = list(slide.shapes)
    
    for shape in shapes:
        try:
            _render_shape(draw, img, shape, W, H, slide_bg)
        except Exception as e:
            log.debug(f"Shape error: {e}")
    
    return img


def _add_watermark(img) -> bytes:
    """يضيف watermark شفاف مائل"""
    from PIL import Image, ImageDraw
    W, H = img.size
    
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    
    font_size = max(18, W // 32)
    font = _find_font(font_size, bold=True)
    text = WATERMARK_TEXT
    
    try:
        bb = d.textbbox((0, 0), text, font=font)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
    except:
        tw, th = len(text) * (font_size // 2), font_size + 4
    
    pad = 30
    tl = Image.new("RGBA", (tw + pad * 2, th + pad), (0, 0, 0, 0))
    td = ImageDraw.Draw(tl)
    td.text((pad, pad // 2), text, fill=(255, 255, 255, 65), font=font)
    rot = tl.rotate(-28, expand=True)
    rw, rh = rot.size
    
    step_x = max(rw + 50, W // 3)
    step_y = max(rh + 30, H // 4)
    
    for row in range(-1, H // step_y + 2):
        for col in range(-1, W // step_x + 2):
            x = col * step_x - rw // 4
            y = row * step_y - rh // 4
            overlay.paste(rot, (x, y), rot)
    
    result = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    
    buf = io.BytesIO()
    result.save(buf, "WEBP", quality=90, method=4)
    return buf.getvalue()


# ─── Main Public API ──────────────────────────────────────────────────────────

def _generate_slides(pptx_path: str) -> List[str]:
    """يحوّل PPTX → قائمة base64 WebP مع watermark"""
    try:
        from pptx import Presentation
        
        prs = Presentation(pptx_path)
        W = max(1280, int((prs.slide_width or 9144000) / 9525))
        H = max(720, int((prs.slide_height or 5143500) / 9525))
        
        # تأكد من نسبة 16:9 أو 4:3
        aspect = prs.slide_width / max(prs.slide_height, 1)
        if abs(aspect - 16/9) < 0.1:
            W, H = 1280, 720
        elif abs(aspect - 4/3) < 0.1:
            W, H = 1024, 768
        
        log.info(f"Rendering {len(prs.slides)} slides at {W}x{H}")
        
        slides_b64 = []
        for i, slide in enumerate(prs.slides):
            try:
                img = _render_slide(slide, W, H)
                wm_bytes = _add_watermark(img)
                slides_b64.append(base64.b64encode(wm_bytes).decode())
                log.debug(f"Slide {i+1} rendered OK")
            except Exception as e:
                log.error(f"Slide {i+1} render error: {e}")
                # إنشاء صورة placeholder بدلاً من تخطي الشريحة
                from PIL import Image, ImageDraw
                ph = Image.new("RGB", (W, H), (30, 50, 100))
                d = ImageDraw.Draw(ph)
                font = _find_font(24, bold=True)
                d.text((W//2 - 60, H//2), f"شريحة {i+1}", fill=(255,255,255), font=font)
                wm_bytes = _add_watermark(ph)
                slides_b64.append(base64.b64encode(wm_bytes).decode())
        
        return slides_b64
        
    except Exception as e:
        log.error(f"_generate_slides failed: {e}")
        return []


def generate_preview_sync(presentation_id: str, pptx_path: str) -> Tuple[str, List[str]]:
    """يولّد المعاينة بشكل متزامن ويُرجع (token, slides_b64)"""
    token = create_preview_session(presentation_id)
    try:
        slides_b64 = _generate_slides(pptx_path)
        set_preview_ready(presentation_id, slides_b64)
        log.info(f"Preview ready (sync): {presentation_id} ({len(slides_b64)} slides)")
    except Exception as e:
        set_preview_error(presentation_id, str(e))
        log.error(f"Preview sync failed for {presentation_id}: {e}")
        slides_b64 = []
    return token, slides_b64


def generate_preview_async(presentation_id: str, pptx_path: str) -> str:
    """يبدأ توليد المعاينة في الخلفية ويُرجع token فوراً"""
    token = create_preview_session(presentation_id)

    def _worker():
        try:
            slides_b64 = _generate_slides(pptx_path)
            set_preview_ready(presentation_id, slides_b64)
            log.info(f"Preview ready (async): {presentation_id} ({len(slides_b64)} slides)")
        except Exception as e:
            set_preview_error(presentation_id, str(e))
            log.error(f"Preview async failed for {presentation_id}: {e}")

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
    return token


# ─── Legacy compatibility ─────────────────────────────────────────────────────

def pptx_to_preview_images(pptx_path: str, watermark: bool = True) -> List[str]:
    _, slides = generate_preview_sync("_legacy_" + str(time.time()), pptx_path)
    return slides


def get_cached_preview(pid):
    session = get_preview_session(pid)
    if session and session.get("status") == "ready":
        return session.get("slides", [])
    return None


def set_cached_preview(pid, slides):
    with _store_lock:
        if pid not in _preview_store:
            _preview_store[pid] = {
                "token": secrets.token_urlsafe(32),
                "created_at": time.time(),
            }
        _preview_store[pid]["slides"] = slides
        _preview_store[pid]["status"] = "ready"
        _preview_store[pid]["slide_count"] = len(slides)
