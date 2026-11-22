"""Gera toda a arte do jogo em 4 tons (Game Boy). Nada de terceiros.

Sprites: '.' transparente, 'w' claro, 'g' médio, 'k' escuro.
Fundo:   '0' claro, '1' médio-claro, '2' médio-escuro, '3' escuro.
"""
import json
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
ARTE = RAIZ / "arte"

CORES_FUNDO = ["#E0F8CF", "#86C06C", "#306850", "#071821"]
CORES_SPRITE = ["#65FF00", "#E0F8CF", "#86C06C", "#071821"]  # 1ª = transparente

COR_SPRITE = {".": CORES_SPRITE[0], "w": CORES_SPRITE[1], "g": CORES_SPRITE[2], "k": CORES_SPRITE[3]}
COR_FUNDO = {str(i): c for i, c in enumerate(CORES_FUNDO)}

LARG, ALT = 40, 36  # jardim em tiles de 8px

# ---------------------------------------------------------------- sprites 16x16

JOGADOR_BAIXO = [
    "................",
    ".....kkkkkk.....",
    "....kkkkkkkk....",
    "....kkwwwwkk....",
    "....kwkwwkwk....",
    "....kwwwwwwk....",
    ".....kwkkwk.....",
    "......kwwk......",
    "....kggggggk....",
    "...kwggggggwk...",
    "...kwkggggkwk...",
    "....kkggggkk....",
    ".....kkkkkk.....",
    ".....kg..gk.....",
    ".....kk..kk.....",
    "................",
]
JOGADOR_BAIXO_2 = JOGADOR_BAIXO[:12] + [
    ".....kkkkkk.....",
    ".....kg...kk....",
    ".....kk.........",
    "................",
]
JOGADOR_DIREITA = [
    "................",
    ".....kkkkkk.....",
    "....kkkkkkkk....",
    "....kkkwwwwk....",
    "....kkwwwkwk....",
    "....kkwwwwwk....",
    ".....kwwwkk.....",
    "......kwwk......",
    ".....kggggk.....",
    ".....kggwwk.....",
    ".....kggwwk.....",
    ".....kggggk.....",
    ".....kkkkkk.....",
    "......kgk.......",
    "......kkk.......",
    "................",
]
JOGADOR_DIREITA_2 = JOGADOR_DIREITA[:12] + [
    ".....kkkkkk.....",
    ".....kg..kgk....",
    ".....kk..kkk....",
    "................",
]
JOGADOR_CIMA = [
    "................",
    ".....kkkkkk.....",
    "....kkkkkkkk....",
    "....kkkkkkkk....",
    "....kkkkkkkk....",
    "....kkkkkkkk....",
    ".....kkkkkk.....",
    "......kwwk......",
    "....kggggggk....",
    "...kwggggggwk...",
    "...kwkggggkwk...",
    "....kkggggkk....",
    ".....kkkkkk.....",
    ".....kg..gk.....",
    ".....kk..kk.....",
    "................",
]
JOGADOR_CIMA_2 = JOGADOR_CIMA[:12] + [
    ".....kkkkkk.....",
    "....kk...gk.....",
    ".........kk.....",
    "................",
]

DRACULA = [
    "......kkkk......",
    ".....kkkkkk.....",
    "....kkk..kkk....",
    "....kwwkkwwk....",
    "....kwkwwkwk....",
    "....kwwwwwwk....",
    "....kwwkkwwk....",
    "..k..kwwwwk..k..",
    ".kgk.wkwwkw.kgk.",
    "kggkkkwkkwkkkggk",
    "kgggkkkwwkkkgggk",
    "kggggkkkkkkggggk",
    ".kgggkkkkkkgggk.",
    "..kkkkkkkkkkkk..",
    "....kk....kk....",
    "....kk....kk....",
]
FRANKENSTEIN = [
    "...kkkkkkkkkk...",
    "...kkkkkkkkkk...",
    "...kggggggggk...",
    "...kgkkggkkgk...",
    "kkkkgkwggwkgkkkk",
    "kkkkggggggggkkkk",
    "...kggkkkkggk...",
    "...kggggggggk...",
    "..kkkkkkkkkkkk..",
    ".kkkkkwkkwkkkkk.",
    ".kgkkkwkkwkkkgk.",
    ".kgkkkkkkkkkkgk.",
    ".kk.kkkkkkkk.kk.",
    "....kkk..kkk....",
    "...kkkk..kkkk...",
    "...kkkk..kkkk...",
]
MUMIA = [
    ".....kkkkkk.....",
    "....kwwwwwwk....",
    "....kgwwwwgk....",
    "....kkkwwkkk....",
    "....kwkwwkwk....",
    "....kwwgwwwk....",
    "....kgwwwwgk....",
    ".kk..kwwwwk..kk.",
    "kwwkkwgwwgwkkwwk",
    "kgwwwwwgwwwwwwgk",
    ".kkkwwwwgwwwkkk.",
    "....kgwwwwwk....",
    "....kwwgwwgk....",
    "....kwwkkwwk....",
    "....kgwkkwgk....",
    "....kkkk.kkk....",
]
LOBISOMEM = [
    "...k........k...",
    "..kgk......kgk..",
    "..kggkkkkkkggk..",
    "..kgggggggggk...",
    "..kgwkggggkwgk..",
    "..kgkkggggkkgk..",
    "..kggggwwggggk..",
    "...kgwwkkwwgk...",
    "...kgwwwwwwgk...",
    "..kggkwwwwkggk..",
    ".kgggggggggggk..",
    ".kgkgggggggkgk..",
    ".kk.kggggggk.kk.",
    "....kggkkggk....",
    "...kkgk..kgkk...",
    "...kkkk..kkkk...",
]

# itens em 12x12 (centrados no 16x16; cabem dentro do balão)
ITENS12 = {
    "morcego": [
        "............",
        "k..........k",
        "kk...kk...kk",
        "kgk.kkkk.kgk",
        "kggkkwkwkggk",
        "kgggkkkkgggk",
        "kgkgkwwkgkgk",
        "kk.kkkkkk.kk",
        "k....kk....k",
        "............",
        "............",
        "............",
    ],
    "flor": [
        "....kkkk....",
        "...kwwwwk...",
        "..kwwkkwwk..",
        "..kwkggkwk..",
        "..kwkggkwk..",
        "..kwwkkwwk..",
        "...kwwwwk...",
        "....kkgk....",
        ".kk..kgk....",
        "kggk.kgk.kk.",
        ".kggkkgkkggk",
        "..kkkkgkkkk.",
    ],
    "faixa": [
        "............",
        "...kkkkkk...",
        "..kwwwwwwk..",
        ".kwwkkkkwwk.",
        ".kwkggggkwk.",
        ".kwkgkkgkwk.",
        ".kwkgkkgkwk.",
        ".kwkggggkwk.",
        ".kwwkkkkwwkk",
        "..kwwwwwwkwk",
        "...kkkkkkkwk",
        "..........kk",
    ],
    "bola": [
        "....kkkk....",
        "..kkwwwwkk..",
        ".kwwwwwwwwk.",
        ".kwwkkkkwwk.",
        "kwwkggggkwwk",
        "kkkggggggkkk",
        "kgggggggggkk",
        "kwwkggggkwwk",
        ".kwwkkkkwwk.",
        ".kwwwwwwwwk.",
        "..kkwwwwkk..",
        "....kkkk....",
    ],
}

VAGALUME_ACESO = [
    "................",
    "................",
    "................",
    "................",
    "......g..g......",
    ".....gwggwg.....",
    "......gkkg......",
    ".....gwkkwg.....",
    "....gwwwwwwg....",
    ".....gwwwwg.....",
    "......gwwg......",
    ".......gg.......",
    "................",
    "................",
    "................",
    "................",
]
VAGALUME_APAGADO = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "......k..k......",
    "......gkkg......",
    "......gkkg......",
    ".......gg.......",
    ".......gg.......",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]


def espelhar(linhas):
    return [l[::-1] for l in linhas]


def subir(linhas, n=1):
    vazio = "." * len(linhas[0])
    return linhas[n:] + [vazio] * n


def centralizar12(linhas):
    vazio = "." * 16
    return [vazio, vazio] + ["..%s.." % l for l in linhas] + [vazio, vazio]


def balao(item12):
    base = [
        "..kkkkkkkkkkkk..",
        ".kwwwwwwwwwwwwk.",
    ] + [".kw" + "w" * 12 + "k."] * 0
    corpo = []
    for l in item12:
        corpo.append(".k" + "".join("w" if c == "." else c for c in l) + "k.")
    fim = [
        ".kwwwwwwwwwwwwk.",
        "..kkkkkkkkkkkk..",
    ]
    linhas = [base[0]] + corpo + fim  # 1 + 12 + 2 = 15
    linhas.append(".......kk.......")  # rabinho
    assert len(linhas) == 16
    return linhas


def folha(frames):
    """Junta frames 16x16 lado a lado numa imagem."""
    for f in frames:
        assert len(f) == 16 and all(len(l) == 16 for l in f), f
    im = Image.new("RGB", (16 * len(frames), 16))
    for i, f in enumerate(frames):
        for y, l in enumerate(f):
            for x, c in enumerate(l):
                im.putpixel((16 * i + x, y), hex_rgb(COR_SPRITE[c]))
    return im


def hex_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


# ---------------------------------------------------------------- cenário

TILES = {
    "grama": [
        "00000000",
        "00000000",
        "00010000",
        "00000000",
        "00000000",
        "00000010",
        "00000000",
        "00000000",
    ],
    "grama2": [
        "00000000",
        "01000000",
        "00000000",
        "00000100",
        "00000000",
        "00000000",
        "00100000",
        "00000000",
    ],
    "trilha": [
        "11111111",
        "11112111",
        "11111111",
        "12111111",
        "11111111",
        "11111121",
        "11111111",
        "11211111",
    ],
    "florzinha": [
        "00000000",
        "00030000",
        "00313000",
        "00030000",
        "00020000",
        "00020000",
        "00000000",
        "00000000",
    ],
}
# árvore 16x16 (4 tiles)
ARVORE = [
    "0000333333330000",
    "0003222222223000",
    "0032222122222300",
    "0322212222212230",
    "3222222222222223",
    "3221222221222223",
    "3222222222212223",
    "3222122222222223",
    "0322222212222230",
    "0032222222222300",
    "0003332222333000",
    "0000003113000000",
    "0000003113000000",
    "0000003113000000",
    "0000033113300000",
    "0000000000000000",
]
MOITA = [
    "0000000000000000",
    "0000033333300000",
    "0003322222233000",
    "0032222122222300",
    "0322122222212230",
    "0322222222222230",
    "3222222212222223",
    "3221222222221223",
    "3222222222222223",
    "3222212222122223",
    "0322222222222230",
    "0322222122222230",
    "0033222222223300",
    "0000333333330000",
    "0000000000000000",
    "0000000000000000",
]

# posições em tiles (canto superior esquerdo do sprite 16x16 = 2x2 tiles)
POSICOES = {
    "jogador": (19, 17),
    "dracula": (8, 7),
    "frankenstein": (30, 7),
    "mumia": (8, 27),
    "lobisomem": (30, 27),
    "morcego": (34, 17),
    "flor": (5, 17),
    "faixa": (19, 6),
    "bola": (19, 29),
}
MOITAS = [(13, 12), (25, 12), (13, 22), (25, 22)]


def mapa_jardim():
    """Devolve (grade de nomes de tile por célula, colisão)."""
    grade = [["grama" if (x * 7 + y * 3) % 5 else "grama2" for x in range(LARG)] for y in range(ALT)]
    col = [[0] * LARG for _ in range(ALT)]
    # trilhas em cruz
    for x in range(2, LARG - 2):
        grade[18][x] = grade[19][x] = "trilha"
    for y in range(2, ALT - 2):
        grade[y][20] = grade[y][21] = "trilha"
    # florzinhas decorativas (só onde é grama)
    for (x, y) in [(4, 4), (11, 3), (16, 9), (27, 4), (35, 10), (5, 31), (14, 31), (33, 32), (24, 15), (10, 24)]:
        if grade[y][x].startswith("grama"):
            grade[y][x] = "florzinha"
    blocos = []  # (x, y, desenho 16x16)
    for x in range(0, LARG, 2):
        for y in (0, ALT - 2):
            blocos.append((x, y, ARVORE))
    for y in range(2, ALT - 2, 2):
        for x in (0, LARG - 2):
            blocos.append((x, y, ARVORE))
    for (x, y) in MOITAS:
        blocos.append((x, y, MOITA))
    for (x, y, _) in blocos:
        for dy in (0, 1):
            for dx in (0, 1):
                col[y + dy][x + dx] = 1
                grade[y + dy][x + dx] = None
    return grade, col, blocos


def desenhar_jardim():
    grade, col, blocos = mapa_jardim()
    im = Image.new("RGB", (LARG * 8, ALT * 8), hex_rgb(CORES_FUNDO[0]))
    for y in range(ALT):
        for x in range(LARG):
            nome = grade[y][x]
            if nome:
                for yy, l in enumerate(TILES[nome]):
                    for xx, c in enumerate(l):
                        im.putpixel((x * 8 + xx, y * 8 + yy), hex_rgb(COR_FUNDO[c]))
    for (x, y, d) in blocos:
        for yy, l in enumerate(d):
            for xx, c in enumerate(l):
                im.putpixel((x * 8 + xx, y * 8 + yy), hex_rgb(COR_FUNDO[c]))
    return im, col


def main():
    ARTE.mkdir(exist_ok=True)
    jardim, col = desenhar_jardim()
    jardim.save(ARTE / "jardim.png")
    (ARTE / "colisao.json").write_text(json.dumps(col))

    folha([JOGADOR_BAIXO, JOGADOR_BAIXO_2, JOGADOR_DIREITA, JOGADOR_DIREITA_2,
           JOGADOR_CIMA, JOGADOR_CIMA_2, espelhar(JOGADOR_DIREITA), espelhar(JOGADOR_DIREITA_2)]
          ).save(ARTE / "jogador.png")
    for nome, d in [("dracula", DRACULA), ("frankenstein", FRANKENSTEIN), ("mumia", MUMIA), ("lobisomem", LOBISOMEM)]:
        folha([d, subir(d)]).save(ARTE / f"{nome}.png")
    for nome, d in ITENS12.items():
        assert len(d) == 12 and all(len(l) == 12 for l in d), nome
        folha([centralizar12(d)]).save(ARTE / f"item_{nome}.png")
        folha([balao(d)]).save(ARTE / f"balao_{nome}.png")
    folha([VAGALUME_ACESO, VAGALUME_APAGADO]).save(ARTE / "vagalume.png")

    # prévia ampliada pra conferir no olho
    nomes = ["jogador", "dracula", "frankenstein", "mumia", "lobisomem", "vagalume"] + \
            [f"item_{i}" for i in ITENS12] + [f"balao_{i}" for i in ITENS12]
    ims = [Image.open(ARTE / f"{n}.png") for n in nomes]
    larg = max(i.width for i in ims) * 4
    prev = Image.new("RGB", (larg + 8, sum(i.height * 4 + 4 for i in ims)), (255, 255, 255))
    y = 0
    for i in ims:
        prev.paste(i.resize((i.width * 4, i.height * 4), Image.NEAREST), (4, y))
        y += i.height * 4 + 4
    prev.save(ARTE / "previa.png")


if __name__ == "__main__":
    main()
