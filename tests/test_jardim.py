import json
from pathlib import Path
from PIL import Image, ImageChops

RAIZ = Path(__file__).resolve().parent.parent


def test_projeto_compila(rom_jogo):
    rom, noi = rom_jogo
    assert rom.stat().st_size >= 32768
    assert "_script_memory" in noi.read_text()


def test_jardim_aparece(jogo, tmp_path):
    jogo.tick(120)
    jogo.foto(tmp_path / "a.png")
    im = Image.open(tmp_path / "a.png").convert("RGB")
    assert len(set(im.getdata())) >= 3


def test_jogador_anda(jogo, tmp_path):
    jogo.tick(120)
    jogo.foto(tmp_path / "a.png")
    jogo.segurar("down", 40)
    jogo.foto(tmp_path / "b.png")
    a = Image.open(tmp_path / "a.png").convert("RGB")
    b = Image.open(tmp_path / "b.png").convert("RGB")
    assert ImageChops.difference(a, b).getbbox() is not None


def test_sem_bloqueio_em_volta():
    from gerar_arte import POSICOES
    col = json.loads((RAIZ / "arte/colisao.json").read_text())
    for nome, (x, y) in POSICOES.items():
        for yy in range(y - 1, y + 3):
            for xx in range(x - 1, x + 3):
                assert col[yy][xx] == 0, (nome, xx, yy)


def test_sem_texto(rom_jogo):
    for f in (RAIZ / "projeto").rglob("*.gbsres"):
        t = f.read_text()
        assert "EVENT_TEXT" not in t and "EVENT_CHOICE" not in t and "EVENT_MENU" not in t, f
