#!/usr/bin/env bash
# 在「本脚本所在目录」启动静态服务，避免在上一级目录开 python 导致 /images/ 实际 404
set -euo pipefail
cd "$(dirname "$0")"
echo "根目录: $(pwd)"

# 可传端口：./serve.sh 9000
# 未传时从 8080 起找第一个未被监听的端口（避免「Address already in use」）
if [[ -n "${1:-}" ]]; then
  PORT="$1"
else
  PORT=""
  for p in 8080 8081 8082 8083 8084 8085; do
    if ! lsof -i TCP:"$p" -s TCP:LISTEN -t >/dev/null 2>&1; then
      PORT=$p
      break
    fi
  done
  if [[ -z "$PORT" ]]; then
    echo "错误：8080–8085 均被占用。请结束旧服务或执行: $0 9000" >&2
    exit 1
  fi
  if [[ "$PORT" != "8080" ]]; then
    echo "提示：8080 已被占用，已改用端口 $PORT" >&2
  fi
fi

echo "浏览器打开: http://127.0.0.1:${PORT}/index.html  （或根路径目录列表里点 index.html）"
echo "按 Ctrl+C 结束"
exec python3 -m http.server "$PORT"
