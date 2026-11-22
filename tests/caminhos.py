"""Leva o jogador até posições do jardim lendo a posição real na memória.

Rota: vai na vertical até a 'avenida' (linha 17), anda na horizontal até a coluna
do alvo e desce/sobe até ele. Assim não esbarra nas moitas nem em outros itens.
"""
from gerar_arte import POSICOES

AVENIDA = 18.0  # fileira (do pé do jogador) da linha 17 do mapa


def alvo(nome):
    """Tile onde o pé do jogador deve parar para encostar em `nome`."""
    x, y = POSICOES[nome]
    if nome in ("dracula", "frankenstein", "mumia", "lobisomem"):
        if y + 1 > AVENIDA:
            return float(x), float(y - 1)   # monstro de baixo: chega por cima
        return float(x), float(y + 3)       # monstro de cima: chega por baixo
    return float(x), float(y + 1)       # em cima do item


def _ir_eixo(emu, eixo, destino, limite=900):
    for _ in range(limite):
        atual = emu.pos_jogador()[eixo]
        d = destino - atual
        if abs(d) < 0.2:
            return
        botao = ("right" if d > 0 else "left") if eixo == 0 else ("down" if d > 0 else "up")
        emu.pb.button_press(botao)
        emu.tick(1)
        emu.pb.button_release(botao)
    raise AssertionError(f"preso indo no eixo {eixo} até {destino}, parado em {emu.pos_jogador()}")


def ir(emu, para):
    x, y = alvo(para)
    _ir_eixo(emu, 1, AVENIDA)
    _ir_eixo(emu, 0, x)
    _ir_eixo(emu, 1, y)
    emu.tick(20)


def sair(emu):
    """Volta pra avenida (sai de qualquer gatilho)."""
    _ir_eixo(emu, 1, AVENIDA)
    emu.tick(10)
