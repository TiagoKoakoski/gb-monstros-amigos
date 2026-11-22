#!/usr/bin/env bash
# Compila o projeto GB Studio pela CLI (montada do fonte v4.3.2).
# Uso: compilar.sh [rom|web]   (env opcional: PROJETO=.../project.gbsproj, SAIDA=dir)
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
FERR="$HOME/Projetos/jogos/_ferramentas"
export PATH="$FERR/node21/node-v21.7.1-linux-x64/bin:$PATH"
CLI="$FERR/gb-studio/out/cli/gb-studio-cli.js"
ALVO="${1:-rom}"
PROJETO="${PROJETO:-$RAIZ/projeto/project.gbsproj}"
SAIDA="${SAIDA:-$RAIZ/build}"
mkdir -p "$SAIDA"
# cache de ferramentas velho (sem o GBDK) quebra o build silenciosamente
rm -rf /tmp/_gbstools
case "$ALVO" in
  rom)
    node "$CLI" make:rom "$PROJETO" "$SAIDA/monstros-amigos.gb"
    cp "$(ls /tmp/_gbsbuild/build/rom/*.noi | head -1)" "$SAIDA/monstros-amigos.noi"
    cp /tmp/_gbsbuild/include/data/game_globals.i "$SAIDA/monstros-amigos.globals"
    ;;
  web)
    rm -rf "$SAIDA/web"
    node "$CLI" make:web "$PROJETO" "$SAIDA/web"
    ;;
  *) echo "uso: compilar.sh [rom|web]" >&2; exit 2 ;;
esac
