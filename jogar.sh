#!/usr/bin/env bash
# Abre o Monstros Amigos no navegador em tela cheia (funciona com controle USB/Bluetooth).
# Uso: ./jogar.sh            -> compila se preciso, sobe o servidor e abre o navegador
#      ./jogar.sh --so-servir -> só sobe o servidor (abra a URL impressa no navegador deste PC)
# Ctrl+C encerra. Na tela cheia, Alt+F4 (ou Esc em alguns navegadores) fecha.
set -euo pipefail
cd "$(dirname "$0")"
PORTA="${PORTA:-8765}"
# porta ocupada (outro jogo aberto)? usa a próxima livre
while python3 -c "import socket,sys; s=socket.socket(); sys.exit(s.connect_ex(('127.0.0.1', $PORTA)) != 0)"; do
  PORTA=$((PORTA + 1))
done

if [ ! -f build/web/index.html ] || [ -n "$(find projeto -newer build/web/index.html -print -quit)" ]; then
  echo "Compilando..."
  ./ferramentas/compilar.sh web >/dev/null
fi

python3 -m http.server "$PORTA" --bind 127.0.0.1 --directory build/web >/dev/null 2>&1 &
SERVIDOR=$!
trap 'kill $SERVIDOR 2>/dev/null' EXIT
sleep 1
kill -0 $SERVIDOR 2>/dev/null || { echo "Não consegui abrir o servidor na porta $PORTA." >&2; exit 1; }
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
