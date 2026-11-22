#!/usr/bin/env bash
# Abre o Monstros Amigos no navegador em tela cheia (funciona com controle USB/Bluetooth).
# Uso: ./jogar.sh            -> compila se preciso, sobe o servidor e abre o navegador
#      ./jogar.sh --so-servir -> só sobe o servidor (pra abrir de outro aparelho na rede)
# Ctrl+C encerra. Na tela cheia, Alt+F4 (ou Esc em alguns navegadores) fecha.
set -euo pipefail
cd "$(dirname "$0")"
PORTA="${PORTA:-8765}"

if [ ! -f build/web/index.html ] || [ -n "$(find projeto -newer build/web/index.html -print -quit)" ]; then
  echo "Compilando..."
  ./ferramentas/compilar.sh web >/dev/null
fi

python3 -m http.server "$PORTA" --bind 127.0.0.1 --directory build/web >/dev/null 2>&1 &
SERVIDOR=$!
trap 'kill $SERVIDOR 2>/dev/null' EXIT
sleep 1
URL="http://127.0.0.1:$PORTA/"

if [ "${1:-}" != "--so-servir" ]; then
  for nav in chromium google-chrome-stable; do
    if command -v "$nav" >/dev/null; then
      "$nav" --kiosk --app="$URL" --user-data-dir="$PWD/build/navegador" >/dev/null 2>&1 &
      break
    fi
  done
fi
echo "Jogo em $URL — Ctrl+C pra encerrar."
wait $SERVIDOR
