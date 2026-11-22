from caminhos import ir, sair

ROTEIRO = [("morcego", "dracula"), ("flor", "frankenstein"), ("faixa", "mumia"), ("bola", "lobisomem")]


def jogar_tudo(emu, fotos=None):
    for i, (item, dono) in enumerate(ROTEIRO):
        ir(emu, item)
        if fotos:
            emu.foto(f"{fotos}/{i}a_pegou_{item}.png")
        sair(emu)
        ir(emu, dono)
        emu.tick(30)
        if fotos:
            emu.foto(f"{fotos}/{i}b_entregou_{dono}.png")
        if i < len(ROTEIRO) - 1:
            sair(emu)
