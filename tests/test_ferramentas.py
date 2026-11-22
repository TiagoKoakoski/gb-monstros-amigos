import shutil
from conftest import compilar, TEMPLATE_EXEMPLO


def test_compila_template_blank(tmp_path):
    proj = tmp_path / "blank"
    shutil.copytree(TEMPLATE_EXEMPLO, proj)
    saida = tmp_path / "out"
    compilar("rom", projeto=proj / "project.gbsproj", saida=saida)
    rom = saida / "monstros-amigos.gb"
    noi = saida / "monstros-amigos.noi"
    assert rom.stat().st_size == 262144
    assert "_script_memory" in noi.read_text()


def test_emu_roda_e_le_variavel(tmp_path):
    from emu import Emu
    proj = tmp_path / "blank"
    shutil.copytree(TEMPLATE_EXEMPLO, proj)
    saida = tmp_path / "out"
    compilar("rom", projeto=proj / "project.gbsproj", saida=saida)
    e = Emu(saida / "monstros-amigos.gb", saida / "monstros-amigos.noi", variaveis=None)
    e.tick(60)
    e.segurar("right", 10)
    assert e.endereco("_script_memory") > 0
    e.foto(tmp_path / "f.png")
    assert (tmp_path / "f.png").exists()
    e.fechar()
