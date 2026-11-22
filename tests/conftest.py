import os, shutil, subprocess, sys
from pathlib import Path
import pytest

RAIZ = Path(__file__).resolve().parent.parent
FERR = Path.home() / "Projetos/jogos/_ferramentas"
TEMPLATE_BLANK = FERR / "gb-studio/appData/templates/blank"
TEMPLATE_EXEMPLO = FERR / "gb-studio/appData/templates/gbs2"  # só p/ testar ferramentas
sys.path.insert(0, str(RAIZ / "ferramentas"))


def compilar(alvo="rom", projeto=None, saida=None):
    env = dict(os.environ)
    if projeto:
        env["PROJETO"] = str(projeto)
    if saida:
        env["SAIDA"] = str(saida)
    r = subprocess.run([str(RAIZ / "ferramentas/compilar.sh"), alvo], env=env,
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]
    return r


@pytest.fixture(scope="session")
def rom_jogo():
    """Gera e compila o jogo uma vez por sessão."""
    subprocess.run([sys.executable, str(RAIZ / "ferramentas/gerar_arte.py")], check=True)
    subprocess.run([sys.executable, str(RAIZ / "ferramentas/gerar_projeto.py")], check=True)
    compilar("rom")
    return RAIZ / "build/monstros-amigos.gb", RAIZ / "build/monstros-amigos.noi"


@pytest.fixture
def jogo(rom_jogo):
    from emu import Emu
    e = Emu(*rom_jogo, variaveis=RAIZ / "projeto/project/variables.gbsres")
    yield e
    e.fechar()
