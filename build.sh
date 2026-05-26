#!/bin/bash
# مذكرتي Pro v21 — Build Script
# No set -e: optional steps shouldn't abort the build

echo "==> Python: $(python3 --version)"

echo "==> [1/4] System packages + LibreOffice + poppler..."
apt-get update -qq 2>/dev/null && \
  apt-get install -y -qq \
    fontconfig fonts-noto-core \
    libreoffice-impress libreoffice-calc libreoffice-writer \
    poppler-utils \
    2>/dev/null && echo "    ✅ LibreOffice + poppler installed" || \
  echo "    WARNING: apt-get failed (normal on some platforms)"

echo "==> [2/4] Arabic font..."
FONT_DIR="${HOME}/.fonts/cairo"
mkdir -p "$FONT_DIR" 2>/dev/null || { FONT_DIR="/tmp/fonts/cairo"; mkdir -p "$FONT_DIR"; }

if fc-list 2>/dev/null | grep -qi "cairo"; then
  echo "    ✅ Cairo already present"
else
  FONT_URL="https://github.com/google/fonts/raw/main/ofl/cairo/Cairo%5Bslnt%2Cwght%5D.ttf"
  if curl -fsSL --max-time 30 "$FONT_URL" -o "$FONT_DIR/Cairo.ttf" 2>/dev/null; then
    fc-cache -fv "$FONT_DIR" 2>/dev/null || true
    echo "    ✅ Cairo downloaded"
  else
    curl -fsSL --max-time 30 \
      "https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Regular.ttf" \
      -o "$FONT_DIR/Amiri-Regular.ttf" 2>/dev/null && \
      echo "    ✅ Amiri fallback installed" || \
      echo "    ⚠️  No Arabic font"
    fc-cache -fv "$FONT_DIR" 2>/dev/null || true
  fi
fi

echo "==> [3/4] LibreOffice smoke test..."
if command -v soffice &>/dev/null; then
  echo "    ✅ soffice found: $(soffice --version 2>/dev/null || echo 'version unknown')"
else
  echo "    ⚠️  soffice not found — preview will use Pillow fallback"
fi

if command -v pdftoppm &>/dev/null; then
  echo "    ✅ pdftoppm found"
else
  echo "    ⚠️  pdftoppm not found"
fi

echo "==> [4/4] Python dependencies..."
pip install --no-cache-dir -r requirements.txt

echo ""
echo "════════════════════════════════"
echo "  Build Complete — v21"
echo "  Python  : $(python3 --version)"
echo "  soffice : $(command -v soffice || echo 'not found')"
echo "  pdftoppm: $(command -v pdftoppm || echo 'not found')"
echo "  Cairo   : $(fc-list 2>/dev/null | grep -ic cairo) file(s)"
echo "════════════════════════════════"
