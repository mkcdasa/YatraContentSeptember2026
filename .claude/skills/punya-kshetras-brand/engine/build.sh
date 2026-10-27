#!/usr/bin/env bash
# Build brochure PDF, poster (PNG/JPG/PDF) and yatri itinerary PDF for one package, optionally in other languages.
# Usage: bash build.sh <workdir> [te] [hi] [kn] [ta]
#   <workdir> holds package.py, rows.json, imgmap.json, img/, optional restaurants.json and i18n/<lang>.json
# Output: <workdir>/out/<slug>-Brochure.pdf, -Poster.jpg/.png/.pdf, -Yatri-Itinerary.pdf, and out/<Language>/...
set -euo pipefail
ENG="$(cd "$(dirname "$0")" && pwd)"; ASSETS="$ENG/../assets"
W="$(cd "$1" && pwd)"; shift; LANGS_REQ=("$@")
B="$W/build"; O="$W/out"; mkdir -p "$B/img" "$O"
cp "$ASSETS/style.css" "$B/"; cp -r "$ASSETS/fonts" "$ASSETS/brand" "$B/"; cp "$ASSETS"/img/* "$B/img/"
[ -d "$W/img" ] && cp -r "$W"/img/. "$B/img/"
export PYTHONPATH="$ENG" PYTHONDONTWRITEBYTECODE=1; PKG="$W/package.py"
cd "$B"
python3 -c "import json,brand;json.dump(brand.CONTACT,open('brand.json','w'))"
SLUG=$(python3 -c "from common import load_pkg;print(load_pkg('$PKG')['slug'])")
HAS_IT=$(python3 -c "from common import load_pkg;print(1 if load_pkg('$PKG')['itinerary']['days'] else 0)")

python3 "$ENG/gen.py" "$PKG"; python3 "$ENG/poster.py" "$PKG"; [ "$HAS_IT" = 1 ] && python3 "$ENG/yatri.py" "$PKG"
python3 "$ENG/i18n.py" extract

render() { # $1 suffix ("" or _te), $2 out dir, $3 name suffix
  local s="$1" od="$2" ns="$3"; mkdir -p "$od"
  node "$ENG/chk.js" "brochure$s.html" || echo "WARNING: overflowing brochure pages above – shorten text or split content"
  node "$ENG/render.js" "brochure$s.html" "$od/$SLUG-Brochure$ns.pdf" "prev_brochure$s"
  node "$ENG/rposter.js" "poster$s.html" "$od/$SLUG-Poster$ns.png" "$od/$SLUG-Poster$ns.pdf"
  python3 -c "from PIL import Image;Image.open('$od/$SLUG-Poster$ns.png').convert('RGB').save('$od/$SLUG-Poster$ns.jpg',quality=90)"
  if [ "$HAS_IT" = 1 ]; then node "$ENG/ryatri.js" "itinerary$s.html" "$od/$SLUG-Yatri-Itinerary$ns.pdf"; fi
}
render "" "$O" ""
for L in "${LANGS_REQ[@]}"; do
  NAME=$(python3 -c "import brand;print(brand.LANGS['$L'])")
  if [ ! -f "$W/i18n/$L.json" ]; then
    echo "TRANSLATION NEEDED: write $W/i18n/$L.json mapping every string in $W/i18n/en.json to $NAME, then re-run."; continue
  fi
  rm -f "$W/i18n/missing_$L.json"; python3 "$ENG/i18n.py" apply "$L"
  if [ -f "$W/i18n/missing_$L.json" ]; then echo "WARNING: $W/i18n/missing_$L.json lists English strings still untranslated in $NAME"; fi
  render "_$L" "$O/$NAME" "-$NAME"
done
echo "Done. Files in $O"; ls -R "$O"
