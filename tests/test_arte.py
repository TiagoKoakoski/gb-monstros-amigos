import json, subprocess, sys
from pathlib import Path
import pytest
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
ARTE = RAIZ / "arte"
MONSTROS = ["dracula", "frankenstein", "mumia", "lobisomem"]
ITENS = ["morcego", "flor", "faixa", "bola"]


@pytest.fixture(scope="module", autouse=True)
def gerar():
    subprocess.run([sys.executable, str(RAIZ / "ferramentas/gerar_arte.py")], check=True)


def cores(p):
    im = Image.open(p).convert("RGB")
    return {"#%02X%02X%02X" % c for c in im.getdata()}


def sprites():
    return [p for p in ARTE.glob("*.png") if p.name not in ("jardim.png", "previa.png")]


def test_cores():
    from gerar_arte import CORES_FUNDO, CORES_SPRITE
    assert cores(ARTE / "jardim.png") <= set(CORES_FUNDO)
    assert len(sprites()) >= 14
    for p in sprites():
        assert cores(p) <= set(CORES_SPRITE), p.name


def test_tamanhos():
    tam = lambda n: Image.open(ARTE / n).size
    assert tam("jardim.png") == (320, 288)
    assert tam("jogador.png") == (128, 16)
    for m in MONSTROS:
        assert tam(f"{m}.png") == (32, 16)
    for i in ITENS:
        assert tam(f"item_{i}.png") == (16, 16)
        assert tam(f"balao_{i}.png") == (16, 16)
    assert tam("vagalume.png") == (32, 16)


def tiles_unicos(p):
    im = Image.open(p).convert("RGB")
    w, h = im.size
    return {im.crop((x, y, x + 8, y + 8)).tobytes() for x in range(0, w, 8) for y in range(0, h, 8)}


def test_tiles_unicos_jardim():
    assert len(tiles_unicos(ARTE / "jardim.png")) <= 192


def test_borda_fechada():
    col = json.loads((ARTE / "colisao.json").read_text())
    assert len(col) == 36 and all(len(l) == 40 for l in col)
    assert all(col[0]) and all(col[-1])
    assert all(l[0] and l[-1] for l in col)


def test_monstros_distintos():
    ims = {m: Image.open(ARTE / f"{m}.png").convert("RGB").crop((0, 0, 16, 16)).tobytes() for m in MONSTROS}
    for a in MONSTROS:
        for b in MONSTROS:
            if a < b:
                dif = sum(x != y for x, y in zip(ims[a], ims[b])) / len(ims[a])
                assert dif >= 0.30 * 1, (a, b, dif)
