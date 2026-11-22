from pathlib import Path
from conftest import compilar

RAIZ = Path(__file__).resolve().parent.parent


def test_build_web(rom_jogo, tmp_path):
    compilar("web", saida=tmp_path)
    index = tmp_path / "web/index.html"
    assert index.exists()
    arquivos = {p.name for p in (tmp_path / "web").rglob("*")}
    assert any(n.endswith(".gb") for n in arquivos) or any(n.endswith(".js") for n in arquivos)
