from caminhos import ir, sair


def iniciar(jogo):
    jogo.tick(90)


def test_pega_item(jogo):
    iniciar(jogo)
    ir(jogo, "morcego")
    assert jogo.var("carregando") == 1
    assert jogo.var("progresso") == 1


def test_entrega_certa(jogo):
    iniciar(jogo)
    ir(jogo, "morcego")
    sair(jogo)
    ir(jogo, "dracula")
    assert jogo.var("ajudados") == 1
    assert jogo.var("ajudado_dracula") == 1
    assert jogo.var("carregando") == 0
    assert jogo.var("progresso") == 2


def test_entrega_errada(jogo):
    iniciar(jogo)
    ir(jogo, "morcego")
    sair(jogo)
    ir(jogo, "frankenstein")
    assert jogo.var("carregando") == 1
    assert jogo.var("ajudados") == 0


def test_segundo_item_ignorado(jogo):
    iniciar(jogo)
    ir(jogo, "morcego")
    sair(jogo)
    ir(jogo, "flor")
    assert jogo.var("carregando") == 1
    assert jogo.var("progresso") == 1


def test_monstro_ajudado_ignora(jogo):
    iniciar(jogo)
    ir(jogo, "morcego"); sair(jogo)
    ir(jogo, "dracula"); sair(jogo)
    ir(jogo, "flor"); sair(jogo)
    ir(jogo, "dracula")
    assert jogo.var("ajudados") == 1
    assert jogo.var("carregando") == 2
