from caminhos import ir, sair

ITEM = {"morcego": 1, "flor": 2, "faixa": 3, "bola": 4}
DONO = {"dracula": 11, "frankenstein": 12, "mumia": 13, "lobisomem": 14}


def esperar_guia(jogo, frames=60 * 8):
    for _ in range(frames):
        jogo.tick(1)
        if jogo.var("guia") == 1:
            return True
    return False


def test_vagalume_aparece_parado(jogo):
    jogo.tick(90)
    assert esperar_guia(jogo)


def test_vagalume_nao_aparece_se_tem_progresso(jogo):
    jogo.tick(90)
    ir(jogo, "morcego")  # progresso no meio do caminho zera o contador
    for _ in range(60 * 3):
        jogo.tick(1)
        assert jogo.var("guia") == 0


def test_vagalume_vai_ao_item(jogo):
    jogo.tick(90)
    assert esperar_guia(jogo)
    assert jogo.var("guia_alvo") == ITEM["morcego"]


def test_vagalume_pula_monstro_ja_ajudado(jogo):
    jogo.tick(90)
    ir(jogo, "morcego"); sair(jogo)
    ir(jogo, "dracula"); sair(jogo)
    assert esperar_guia(jogo)
    assert jogo.var("guia_alvo") == ITEM["flor"]


def test_vagalume_vai_ao_dono(jogo):
    jogo.tick(90)
    ir(jogo, "bola"); sair(jogo)
    assert esperar_guia(jogo)
    assert jogo.var("guia_alvo") == DONO["lobisomem"]


def test_jogador_anda_com_vagalume_voando(jogo):
    jogo.tick(90)
    assert esperar_guia(jogo)
    antes = jogo.pos_jogador()
    jogo.segurar("down", 16)
    assert jogo.pos_jogador() != antes


def test_vagalume_unico_e_fora_da_festa(jogo):
    jogo.tick(90)
    jogo.set_var("fim", 1)
    for _ in range(60 * 8):
        jogo.tick(1)
        assert jogo.var("guia") == 0
    jogo.set_var("fim", 0)
    assert esperar_guia(jogo)
    for _ in range(60 * 4):
        jogo.tick(1)
        assert jogo.var("guia") in (0, 1)


def test_vagalume_fica_na_tela(jogo):
    """Alvo longe: o vaga-lume para a no máximo 6 tiles (x) / 4 tiles (y) do jogador, visível."""
    jogo.tick(90)
    assert esperar_guia(jogo)
    jogo.tick(5)
    px, py = jogo.var("vx"), jogo.var("vy")
    assert abs(jogo.var("gx") - px) <= 6
    assert abs(jogo.var("gy") - py) <= 4
