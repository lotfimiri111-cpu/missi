"""
core/preview.py v8 — معاينة شريحتين فقط بجودة 100% حقيقية
الأولى + الأخيرة — عبر LibreOffice → PDF → PNG
مع Pillow fallback إذا لم يكن LibreOffice متاحاً
"""
import base64
import hmac
import io
import logging
import os
import secrets
import shutil
import subprocess
import tempfile
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

log = logging.getLogger(__name__)

# ─── Config ───────────────────────────────────────────────────────────────────
_preview_store: Dict[str, dict] = {}
_store_lock = threading.Lock()

PREVIEW_TTL    = 3 * 3600
PREVIEW_DPI    = 180          # جودة عالية
PREVIEW_SLIDES = 2            # الأولى + الأخيرة فقط
WATERMARK_TEXT = "مذكرتي Pro — معاينة فقط"


# ─── Session Management ───────────────────────────────────────────────────────

def create_preview_session(pid: str) -> str:
    token = secrets.token_urlsafe(32)
    with _store_lock:
        _preview_store[pid] = {
            "token": token, "slides": [],
            "status": "pending", "created_at": time.time(), "slide_count": 0,
        }
    return token

def get_preview_session(pid: str) -> Optional[dict]:
    _cleanup_expired()
    with _store_lock:
        return _preview_store.get(pid)

def get_preview_slides(pid: str, token: str) -> Optional[List[str]]:
    s = get_preview_session(pid)
    if not s or not hmac.compare_digest(s["token"], token):
        return None
    return s.get("slides", [])

def set_preview_ready(pid: str, slides: List[str]):
    with _store_lock:
        if pid in _preview_store:
            _preview_store[pid].update({"slides": slides, "status": "ready", "slide_count": len(slides)})

def set_preview_error(pid: str, msg: str):
    with _store_lock:
        if pid in _preview_store:
            _preview_store[pid].update({"status": "error", "error": msg})

def _cleanup_expired():
    now = time.time()
    with _store_lock:
        for k in [k for k, v in _preview_store.items() if now - v.get("created_at", 0) > PREVIEW_TTL]:
            del _preview_store[k]

def get_cached_preview(pid):
    s = get_preview_session(pid)
    return s.get("slides", []) if s and s.get("status") == "ready" else None

def set_cached_preview(pid, slides):
    with _store_lock:
        if pid not in _preview_store:
            _preview_store[pid] = {"token": secrets.token_urlsafe(32), "created_at": time.time()}
        _preview_store[pid].update({"slides": slides, "status": "ready", "slide_count": len(slides)})


# ─── LibreOffice: PPTX → PDF → PNG ───────────────────────────────────────────

def _find_soffice() -> Optional[str]:
    """يجد soffice في المسارات المعتادة"""
    for c in ["soffice", "libreoffice"]:
        p = shutil.which(c)
        if p:
            return p
    for p in [
        "/usr/bin/soffice", "/usr/lib/libreoffice/program/soffice",
        "/opt/libreoffice7.6/program/soffice", "/opt/libreoffice/program/soffice",
    ]:
        if os.path.exists(p):
            return p
    return None


def _pptx_to_pdf(pptx_path: str, out_dir: str) -> Optional[str]:
    """يحوّل PPTX → PDF باستخدام LibreOffice"""
    soffice = _find_soffice()
    if not soffice:
        return None
    try:
        env = os.environ.copy()
        env["HOME"] = tempfile.gettempdir()   # يمنع crash من HOME permissions
        result = subprocess.run(
            [soffice, "--headless", "--norestore", "--nofirststartwizard",
             "--convert-to", "pdf", "--outdir", out_dir, pptx_path],
            capture_output=True, text=True, timeout=120, env=env
        )
        log.info(f"soffice stdout: {result.stdout[:300]}")
        if result.returncode != 0:
            log.warning(f"soffice stderr: {result.stderr[:300]}")
        pdfs = sorted(Path(out_dir).glob("*.pdf"))
        return str(pdfs[0]) if pdfs else None
    except Exception as e:
        log.warning(f"LibreOffice failed: {e}")
        return None


def _pdf_page_to_png(pdf_path: str, page: int, out_dir: str, dpi: int) -> Optional[str]:
    """يحوّل صفحة واحدة من PDF → PNG"""
    prefix = os.path.join(out_dir, f"page{page}")
    try:
        result = subprocess.run(
            ["pdftoppm", "-png", "-r", str(dpi),
             "-f", str(page), "-l", str(page),
             pdf_path, prefix],
            capture_output=True, timeout=30
        )
        pngs = sorted(Path(out_dir).glob(f"page{page}*.png"))
        return str(pngs[0]) if pngs else None
    except Exception as e:
        log.warning(f"pdftoppm page {page} failed: {e}")
        return None


def _pdf_page_count(pdf_path: str) -> int:
    """يُرجع عدد صفحات PDF"""
    try:
        r = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True, timeout=10)
        for line in r.stdout.splitlines():
            if line.startswith("Pages:"):
                return int(line.split(":")[1].strip())
    except:
        pass
    try:
        r = subprocess.run(
            ["pdftoppm", "-png", "-r", "10", pdf_path, "/tmp/_count_test"],
            capture_output=True, timeout=15
        )
        pages = sorted(Path("/tmp").glob("_count_test*.png"))
        for p in pages:
            p.unlink(missing_ok=True)
        return len(pages)
    except:
        pass
    return 1


# ─── Watermark ────────────────────────────────────────────────────────────────

def _add_watermark(img_path: str) -> bytes:
    """يضيف watermark شفاف مائل على الصورة ويُرجع WebP bytes"""
    from PIL import Image, ImageDraw, ImageFont

    img = Image.open(img_path).convert("RGBA")
    W, H = img.size

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # خط
    font_size = max(18, W // 34)
    font = _find_font(font_size, bold=True)
    text = WATERMARK_TEXT

    try:
        bb = d.textbbox((0, 0), text, font=font)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
    except:
        tw, th = len(text) * (font_size // 2), font_size + 4

    pad = 30
    tile = Image.new("RGBA", (tw + pad * 2, th + pad), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    td.text((pad, pad // 2), text, fill=(255, 255, 255, 62), font=font)
    rot = tile.rotate(-28, expand=True)
    rw, rh = rot.size

    sx = max(rw + 50, W // 3)
    sy = max(rh + 30, H // 4)

    for row in range(-1, H // sy + 2):
        for col in range(-1, W // sx + 2):
            overlay.paste(rot, (col * sx - rw // 4, row * sy - rh // 4), rot)

    result = Image.alpha_composite(img, overlay).convert("RGB")
    buf = io.BytesIO()
    result.save(buf, "WEBP", quality=92, method=4)
    return buf.getvalue()


def _find_font(size=16, bold=False):
    from PIL import ImageFont
    candidates = [
        os.path.expanduser("~/.fonts/cairo/Cairo.ttf"),
        "/root/.fonts/cairo/Cairo.ttf",
        "/tmp/fonts/cairo/Cairo.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()


# ─── Pillow Fallback (جودة محدودة — للطوارئ فقط) ─────────────────────────────

def _pillow_render_slide(slide, W: int, H: int) -> bytes:
    """رسم شريحة بالـ Pillow — fallback فقط"""
    from PIL import Image, ImageDraw
    from pptx.enum.shapes import MSO_SHAPE_TYPE

    img = Image.new("RGB", (W, H), (255, 255, 255))

    # خلفية
    try:
        bg_elem = slide.background._element
        ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'
        for child in bg_elem.iter():
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if tag == 'srgbClr':
                val = child.get('val', '')
                if val and len(val) == 6:
                    r, g, b = int(val[0:2],16), int(val[2:4],16), int(val[4:6],16)
                    img = Image.new("RGB", (W, H), (r, g, b))
                    break
    except:
        pass

    draw = ImageDraw.Draw(img)

    for shape in slide.shapes:
        try:
            L = int((shape.left or 0) / 914400 * 96)
            T = int((shape.top or 0) / 914400 * 96)
            SW = int((shape.width or 0) / 914400 * 96)
            SH = int((shape.height or 0) / 914400 * 96)

            # صورة
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                try:
                    pic = Image.open(io.BytesIO(shape.image.blob)).convert("RGBA")
                    pic = pic.resize((max(1,SW), max(1,SH)), Image.LANCZOS)
                    img.paste(pic, (L, T), pic)
                except:
                    pass
                continue

            # شكل ملون
            fc = None
            try:
                ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'
                solid = shape._element.find(f'.//{{{ns}}}solidFill')
                if solid is not None:
                    for c in solid.iter():
                        tag = c.tag.split('}')[-1] if '}' in c.tag else c.tag
                        if tag == 'srgbClr':
                            v = c.get('val','')
                            if len(v)==6:
                                fc = (int(v[0:2],16),int(v[2:4],16),int(v[4:6],16))
                            break
            except:
                pass

            if fc and SW > 0 and SH > 0:
                draw.rectangle([L, T, L+SW, T+SH], fill=fc)

            # نص
            if shape.has_text_frame:
                y = T + 4
                bg_lum = (0.299*(fc[0] if fc else 255)+0.587*(fc[1] if fc else 255)+0.114*(fc[2] if fc else 255))
                tc = (255,255,255) if bg_lum < 128 else (10,10,10)
                for para in shape.text_frame.paragraphs:
                    txt = para.text.strip()
                    if not txt:
                        y += 6
                        continue
                    fs = 14
                    for run in para.runs:
                        try:
                            if run.font.size:
                                fs = max(8, min(int(run.font.size/12700), 60))
                        except:
                            pass
                        break
                    fs = max(7, int(fs * min(W/1280, H/720)))
                    font = _find_font(fs)
                    draw.text((L+6, y), txt, fill=tc, font=font)
                    y += fs + 4
        except:
            pass

    buf = io.BytesIO()
    img.save(buf, "PNG")
    buf.seek(0)
    # حفظ مؤقت للـ watermark
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp.write(buf.getvalue())
    tmp.close()
    return tmp.name


# ─── Core: توليد شريحتين فقط ─────────────────────────────────────────────────

def _generate_two_slides(pptx_path: str) -> List[str]:
    """
    يُرجع شريحتين فقط: الأولى + الأخيرة
    بجودة 100% حقيقية عبر LibreOffice → PDF → PNG
    """
    from pptx import Presentation

    prs = Presentation(pptx_path)
    total = len(prs.slides)
    # الشريحة الأولى (1) والأخيرة
    target_pages = [1]
    if total > 1:
        target_pages.append(total)

    log.info(f"Generating preview: {len(target_pages)} slides from {total} total")

    with tempfile.TemporaryDirectory() as tmpdir:

        # ── محاولة LibreOffice ────────────────────────────────────────────────
        pdf_path = _pptx_to_pdf(pptx_path, tmpdir)

        if pdf_path and os.path.exists(pdf_path):
            log.info(f"LibreOffice OK → {pdf_path}")
            slides_b64 = []
            for page in target_pages:
                png = _pdf_page_to_png(pdf_path, page, tmpdir, PREVIEW_DPI)
                if png and os.path.exists(png):
                    wm = _add_watermark(png)
                    slides_b64.append(base64.b64encode(wm).decode())
                    log.info(f"Slide {page} → OK ({len(wm)//1024}KB)")
                else:
                    log.warning(f"pdftoppm failed for page {page}")
            if slides_b64:
                return slides_b64

        # ── Pillow Fallback ───────────────────────────────────────────────────
        log.warning("LibreOffice unavailable — using Pillow fallback")
        W = max(1280, int((prs.slide_width or 9144000) / 9525))
        H = max(720,  int((prs.slide_height or 5143500) / 9525))

        slides_b64 = []
        indices = [0] + ([total - 1] if total > 1 else [])
        for i in indices:
            try:
                tmp_png = _pillow_render_slide(prs.slides[i], W, H)
                wm = _add_watermark(tmp_png)
                os.unlink(tmp_png)
                slides_b64.append(base64.b64encode(wm).decode())
            except Exception as e:
                log.error(f"Pillow fallback slide {i}: {e}")

        return slides_b64


# ─── Public API ───────────────────────────────────────────────────────────────

def generate_preview_sync(pid: str, pptx_path: str) -> Tuple[str, List[str]]:
    """يُولّد المعاينة (شريحتان) بشكل متزامن"""
    token = create_preview_session(pid)
    try:
        slides = _generate_two_slides(pptx_path)
        set_preview_ready(pid, slides)
        log.info(f"Preview ready (sync): {pid} — {len(slides)} slides")
    except Exception as e:
        set_preview_error(pid, str(e))
        log.error(f"Preview sync failed {pid}: {e}")
        slides = []
    return token, slides


def generate_preview_async(pid: str, pptx_path: str) -> str:
    """يُولّد المعاينة في الخلفية"""
    token = create_preview_session(pid)
    def _w():
        try:
            slides = _generate_two_slides(pptx_path)
            set_preview_ready(pid, slides)
        except Exception as e:
            set_preview_error(pid, str(e))
    threading.Thread(target=_w, daemon=True).start()
    return token


def pptx_to_preview_images(pptx_path: str, watermark: bool = True) -> List[str]:
    _, slides = generate_preview_sync("_legacy_" + str(time.time()), pptx_path)
    return slides
