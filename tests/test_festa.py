from PIL import Image, ImageChops
from partida import jogar_tudo

VARS = ["carregando", "ajudados", "ajudado_dracula", "ajudado_frankenstein", "ajudado_mumia",
        "ajudado_lobisomem", "progresso", "fim", "guia"]  # 'ocioso' volta a contar sozinho


def estrutura(p):
    """Troca cada cor pelo seu posto de brilho: ignora variação de tom do fade."""
    im = Image.open(p).convert("RGB")
    cores = sorted(set(im.getdata()), key=lambda c: sum(c))
    posto = {c: i for i, c in enumerate(cores)}
    return [posto[c] for c in im.getdata()]


def diferentes(p1, p2):
    return estrutura(p1) != estrutura(p2)


def test_partida_completa(jogo):
    jogo.tick(90)
    inicio = jogo.pb.frame_count
    jogar_tudo(jogo)
    jogo.tick(90)  # emote de coração segura o script ~1 s antes da festa
    assert jogo.var("fim") == 1
    assert jogo.var("ajudados") == 4
    assert jogo.pb.frame_count - inicio < 60 * 180


def test_festa(jogo, tmp_path):
    jogo.tick(90)
    jogar_tudo(jogo)
    jogo.tick(90)
    assert jogo.var("fim") == 1
    jogo.tick(120)
    assert jogo.var("guia") == 0
    # lobisomem está logo acima do jogador: recorte da área dele em vários momentos
    recortes = set()
    for k in range(8):
        jogo.tick(8)
        jogo.foto(tmp_path / f"f{k}.png")
        recortes.add(Image.open(tmp_path / f"f{k}.png").convert("RGB").crop((56, 32, 104, 72)).tobytes())
    assert len(recortes) >= 2  # monstro dançando (alterna frames)


def test_recomeco_limpo(jogo, tmp_path):
    jogo.tick(90)
    jogo.foto(tmp_path / "inicio.png")
    jogar_tudo(jogo)
    jogo.tick(240)
    jogo.segurar("a", 5)
    jogo.tick(120)
    for v in VARS:
        assert jogo.var(v) == 0, v
    jogo.foto(tmp_path / "depois.png")
    assert not diferentes(tmp_path / "inicio.png", tmp_path / "depois.png")
