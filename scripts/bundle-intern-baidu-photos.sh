#!/usr/bin/env bash
# 将源文件夹内图片按「文件名排序」重命名为 images/intern-baidu-1.jpg … N.jpg
# 依赖：macOS 的 sips（本机预装）用于把 PNG/HEIC 等转为 JPEG
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${1:-$ROOT/images/baidu-raw}"
OUT_DIR="$ROOT/images"

if [[ ! -d "$SRC" ]]; then
  echo "错误：源目录不存在: $SRC" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

# 只收集图片；按「自然序」排序，避免 图1 图2 … 图10 被排成 图1、图10、图2
files=()
while IFS= read -r line; do
  [[ -n "$line" ]] && files+=("$line")
done < <(python3 - "$SRC" <<'PY'
import os, re, sys
src = sys.argv[1]
ext_ok = re.compile(r"\.(jpe?g|png|heic|webp|gif)$", re.I)
def nkey(s):
    return [int(x) if x.isdigit() else x.lower() for x in re.split(r"(\d+)", s)]
out = []
for name in os.listdir(src):
    if not ext_ok.search(name):
        continue
    lo = name.lower()
    if lo.endswith((".txt", ".sh")):
        continue
    if name == ".DS_Store":
        continue
    out.append(os.path.join(src, name))
out.sort(key=lambda p: nkey(os.path.basename(p)) or p)
for p in out:
    print(p)
PY
)

n="${#files[@]}"
if [[ "$n" -eq 0 ]]; then
  echo "未在以下目录找到任何图片（支持 jpg/png/heic/webp/gif）:" >&2
  echo "  $SRC" >&2
  echo "" >&2
  echo "请用访达（Finder）把照片复制或拖进该文件夹，再重新运行本脚本。" >&2
  exit 1
fi

if ! command -v sips >/dev/null 2>&1; then
  echo "错误：未找到 sips。请在 macOS 上运行，或安装 ImageMagick 后自行改脚本。" >&2
  exit 1
fi

i=0
for src in "${files[@]}"; do
  i=$((i + 1))
  dst="$OUT_DIR/intern-baidu-$i.jpg"
  ext="${src##*.}"
  elc=$(printf '%s' "$ext" | tr '[:upper:]' '[:lower:]')
  if [[ "$elc" == "jpg" || "$elc" == "jpeg" ]]; then
    cp -f "$src" "$dst"
  elif sips -s format jpeg "$src" --out "$dst" >/dev/null 2>&1; then
    :
  else
    echo "警告：sips 无法转换，尝试直接复制: $(basename "$src")" >&2
    cp -f "$src" "$dst" || true
  fi
  echo "  [$i/$n] $(basename "$src") -> intern-baidu-$i.jpg"
done

echo ""
echo "完成：已写入 $OUT_DIR/intern-baidu-1.jpg … intern-baidu-$n.jpg"
echo "请在 index.html 中让 APRIL_BAIDU_CCF.files 包含上述 n 个文件名（顺序已固定为 1..$n）。"
echo "然后 ./serve.sh 用浏览器打开并强刷预览。"
