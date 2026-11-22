"""Joga a partida inteira sozinho no emulador e fotografa cada etapa em build/fotos/.

Uso: venv/bin/python ferramentas/jogar_sozinho.py   (compile antes com ferramentas/compilar.sh)
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(RAIZ / "ferramentas"), str(RAIZ / "tests")]
from emu import Emu  # noqa: E402
from partida import jogar_tudo  # noqa: E402


def main():
    fotos = RAIZ / "build/fotos"
    fotos.mkdir(parents=True, exist_ok=True)
    e = Emu(RAIZ / "build/monstros-amigos.gb", RAIZ / "build/monstros-amigos.noi")
    e.tick(90)
    e.foto(fotos / "00_inicio.png")
    jogar_tudo(e, fotos=str(fotos))
    e.tick(150)
    e.foto(fotos / "90_festa.png")
    ok = e.var("fim") == 1
    e.tick(90)  # espera a musiquinha acabar: só então o jogo aceita o botão
    e.segurar("a", 5)
    e.tick(120)
    e.foto(fotos / "99_recomecou.png")
    ok = ok and e.var("ajudados") == 0
    e.fechar()
    print("partida completa e recomeço: OK" if ok else "FALHOU")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
