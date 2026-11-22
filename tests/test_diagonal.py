"""Criança segurando diagonal contra monstro/parede não pode ficar congelada."""
import pytest
from caminhos import _ir_eixo


def segurar_dois(jogo, primeiro, segundo, frames):
    """Segura as duas direções; devolve as posições no meio e no fim (tem que seguir andando)."""
    jogo.pb.button_press(primeiro)
    jogo.tick(4)
    jogo.pb.button_press(segundo)
    jogo.tick(frames // 2)
    meio = jogo.pos_jogador()
    jogo.tick(frames // 2)
    fim = jogo.pos_jogador()
    jogo.pb.button_release(primeiro)
    jogo.pb.button_release(segundo)
    jogo.tick(2)
    return meio, fim


@pytest.mark.parametrize("primeiro,segundo", [("right", "up"), ("up", "right"), ("left", "up"), ("up", "left")])
def test_diagonal_contra_monstro_desliza(jogo, primeiro, segundo):
    jogo.tick(90)
    _ir_eixo(jogo, 1, 18.0)
    _ir_eixo(jogo, 0, 8.0)
    _ir_eixo(jogo, 1, 10.0)          # logo abaixo do Drácula
    meio, fim = segurar_dois(jogo, primeiro, segundo, 40)
    assert meio != fim, (primeiro, segundo, meio, fim)


@pytest.mark.parametrize("primeiro,segundo", [("up", "left"), ("left", "up"), ("down", "left"), ("left", "down")])
def test_diagonal_contra_parede_desliza(jogo, primeiro, segundo):
    jogo.tick(90)
    _ir_eixo(jogo, 0, 2.0)           # encostado nas árvores da esquerda, no meio da altura
    meio, fim = segurar_dois(jogo, primeiro, segundo, 40)
    assert meio != fim, (primeiro, segundo, meio, fim)
