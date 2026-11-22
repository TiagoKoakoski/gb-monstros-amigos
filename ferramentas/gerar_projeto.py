"""Gera o projeto GB Studio 4.3.2 do Monstros Amigos em projeto/ (abre no GB Studio).

Tudo determinístico: os IDs saem de uuid5(nome), então regenerar não bagunça o projeto.
"""
import hashlib
import json
import shutil
import uuid
from pathlib import Path

from PIL import Image

import gerar_arte as A

RAIZ = Path(__file__).resolve().parent.parent
PROJ = RAIZ / "projeto"
TEMPLATE = Path.home() / "Projetos/jogos/_ferramentas/gb-studio/appData/templates/blank"
NS = uuid.UUID("6f1c2b1e-9a51-4c43-8d1f-3c0f6f0b2a77")

MONSTROS = ["dracula", "frankenstein", "mumia", "lobisomem"]
ITEM_DE = {"dracula": "morcego", "frankenstein": "flor", "mumia": "faixa", "lobisomem": "bola"}
ITENS = [ITEM_DE[m] for m in MONSTROS]  # índice+1 = valor de 'carregando'
POSICOES = A.POSICOES

VARIAVEIS = ["carregando", "ajudados"] + [f"ajudado_{m}" for m in MONSTROS] + \
    ["progresso", "fim", "guia", "ocioso", "ultimo_progresso", "px", "py"]
VAR = {n: str(i) for i, n in enumerate(VARIAVEIS)}


def ID(nome):
    return str(uuid.uuid5(NS, nome))


# ------------------------------------------------------------------ eventos

def ev(comando, children=None, **args):
    e = {"command": comando, "args": args, "id": ID(f"ev-{comando}-{json.dumps(args, sort_keys=True)}-{ev.n}")}
    ev.n += 1
    if children is not None:
        e["children"] = children
    return e


ev.n = 0


def num(v):
    return {"type": "number", "value": v}


def var(nome):
    return {"type": "variable", "value": VAR[nome]}


def igual(nome, valor):
    return {"type": "eq", "valueA": var(nome), "valueB": num(valor)}


def se(cond, entao, senao=None):
    return ev("EVENT_IF", children={"true": entao + [ev("EVENT_END")], "false": (senao or []) + [ev("EVENT_END")]},
              condition=cond, __collapseElse=senao is None, __disableElse=senao is None)


def setar(nome, valor):
    return ev("EVENT_SET_VALUE", variable=VAR[nome], value=num(valor) if isinstance(valor, int) else valor)


def somar(nome):
    return ev("EVENT_INC_VALUE", variable=VAR[nome])


def som(tipo="beep", pitch=4, frequency=200, duration=0.3):
    return ev("EVENT_SOUND_PLAY_EFFECT", type=tipo, pitch=pitch, frequency=frequency, duration=duration,
              wait=False, priority="medium")


def esperar(frames):
    return ev("EVENT_WAIT", time=num(frames / 60), frames=num(frames), units="frames")


# ------------------------------------------------------------------ recursos

def sprite_res(nome, frames, tipo="fixed"):
    """Recurso de sprite 16x16 por frame. tipo: fixed (anim 0 = todos os frames) ou multi_movement."""
    png = A.ARTE / f"{nome}.png"
    w, h = Image.open(png).size

    def quadro(i):
        sx = 16 * i
        return {"id": ID(f"{nome}-q{i}"), "tiles": [
            {"id": ID(f"{nome}-q{i}-t{k}"), "x": 8 * k, "y": 0, "sliceX": sx + 8 * k, "sliceY": 0,
             "flipX": False, "flipY": False, "palette": 0, "paletteIndex": 0, "objPalette": "OBP0",
             "priority": False} for k in (0, 1)]}

    vazio = lambda a: {"id": ID(f"{nome}-a{a}-v"), "tiles": []}
    if tipo == "multi_movement":
        # ordem do GB Studio: parado dir, esq, cima, baixo; andando dir, esq, cima, baixo
        # jogador.png: baixo(0,1) direita(2,3) cima(4,5) esquerda(6,7)
        mapa = [[2], [], [4], [0], [3, 2], [], [5, 4], [1, 0]]
    else:
        mapa = [list(range(frames))] + [[]] * 7
    anims = []
    for a, idx in enumerate(mapa):
        anims.append({"id": ID(f"{nome}-a{a}"), "frames": [quadro(i) for i in idx] or [vazio(a)]})
    return {
        "_resourceType": "sprite", "id": ID(f"sprite-{nome}"), "name": nome, "symbol": f"sprite_{nome}",
        "numTiles": 2 * frames, "canvasOriginX": 0, "canvasOriginY": 0, "canvasWidth": 16, "canvasHeight": 16,
        "boundsX": 0, "boundsY": -8, "boundsWidth": 16, "boundsHeight": 16, "animSpeed": 15,
        "filename": png.name, "width": w, "height": h,
        "checksum": hashlib.sha1(png.read_bytes()).hexdigest(),
        "states": [{"id": ID(f"{nome}-estado"), "name": "", "animationType": tipo,
                    "flipLeft": tipo == "multi_movement", "animations": anims}],
    }


def colisoes_str(col):
    plano = [0x0F if c else 0 for linha in col for c in linha]
    out, ultimo, n = "", -1, 0

    def fechar():
        return "!" if n == 1 else (f"{n:x}+" if n > 0 else "")
    for v in plano:
        if v != ultimo:
            out += fechar()
            n, ultimo = 0, v
            out += f"{v:02x}"
        n += 1
    return out + fechar()


def ator(nome, sprite, x, y, idx, script=None, start=None, update=None, animar=False):
    return {
        "_resourceType": "actor", "id": ID(f"ator-{nome}"), "_index": idx, "symbol": f"actor_{nome}",
        "prefabId": "", "name": nome, "coordinateType": "tiles", "x": x, "y": y + 1, "frame": 0,
        "animate": animar, "spriteSheetId": ID(f"sprite-{sprite}"), "paletteId": "", "direction": "down",
        "moveSpeed": 1, "animSpeed": 15, "isPinned": False, "persistent": False, "collisionGroup": "",
        "collisionExtraFlags": [], "prefabScriptOverrides": {},
        "script": script or [], "startScript": start or [], "updateScript": update or [],
        "hit1Script": [], "hit2Script": [], "hit3Script": [],
    }


def gatilho(nome, x, y, w, h, idx, script):
    return {"_resourceType": "trigger", "id": ID(f"gat-{nome}"), "_index": idx, "symbol": f"trigger_{nome}",
            "prefabId": "", "name": nome, "x": x, "y": y, "width": w, "height": h,
            "prefabScriptOverrides": {}, "script": script, "leaveScript": []}


def a(nome):
    """id de ator para usar em eventos"""
    return ID(f"ator-{nome}")


# ------------------------------------------------------------------ lógica (preenchida nas tasks 4-6)

def scripts_cena():
    return []


def montar_atores():
    atores, gats = [], []
    i = 0
    for m in MONSTROS:
        x, y = POSICOES[m]
        atores.append(ator(m, m, x, y, i)); i += 1
        it = ITEM_DE[m]
        atores.append(ator(f"balao_{m}", f"balao_{it}", x, y - 2, i)); i += 1
    for it in ITENS:
        x, y = POSICOES[it]
        atores.append(ator(f"item_{it}", f"item_{it}", x, y, i)); i += 1
    return atores, gats


# ------------------------------------------------------------------ escrita

def escrever(caminho, dado):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(dado, indent=2, ensure_ascii=False))


def main():
    A.main()
    if PROJ.exists():
        shutil.rmtree(PROJ)
    shutil.copytree(TEMPLATE, PROJ)
    # tira os placeholders do template que não usamos
    for p in (PROJ / "assets/sprites").glob("*"):
        p.unlink()
    for p in (PROJ / "assets/backgrounds").glob("*"):
        p.unlink()

    escrever(PROJ / "project.gbsproj", {"_resourceType": "project", "name": "Monstros Amigos",
                                         "author": "Tiago", "notes": "Gerado por ferramentas/gerar_projeto.py",
                                         "_version": "4.2.0", "_release": "10"})

    sprites = [("jogador", 8, "multi_movement")] + [(m, 2, "fixed") for m in MONSTROS] + \
        [(f"item_{i}", 1, "fixed") for i in ITENS] + [(f"balao_{i}", 1, "fixed") for i in ITENS] + \
        [("vagalume", 2, "fixed")]
    for nome, frames, tipo in sprites:
        shutil.copy(A.ARTE / f"{nome}.png", PROJ / "assets/sprites" / f"{nome}.png")
        escrever(PROJ / "assets/sprites" / f"{nome}.png.gbsres", sprite_res(nome, frames, tipo))

    shutil.copy(A.ARTE / "jardim.png", PROJ / "assets/backgrounds/jardim.png")
    escrever(PROJ / "assets/backgrounds/jardim.png.gbsres", {
        "_resourceType": "background", "id": ID("bg-jardim"), "name": "jardim", "symbol": "bg_jardim",
        "tileColors": "", "filename": "jardim.png", "width": A.LARG, "height": A.ALT,
        "imageWidth": A.LARG * 8, "imageHeight": A.ALT * 8, "autoColor": False})

    escrever(PROJ / "project/variables.gbsres", {
        "_resourceType": "variables",
        "variables": [{"id": VAR[n], "name": n, "symbol": f"var_{n}"} for n in VARIAVEIS],
        "constants": []})

    cfg = json.loads((PROJ / "project/settings.gbsres").read_text())
    jx, jy = POSICOES["jogador"]
    cfg.update(startSceneId=ID("cena-jardim"), startX=jx, startY=jy + 1, startDirection="down",
               startMoveSpeed=1, colorMode="none", sgbEnabled=False)
    cfg["defaultPlayerSprites"] = {k: ID("sprite-jogador") for k in cfg.get("defaultPlayerSprites", {}) or
                                   ["TOPDOWN", "PLATFORM", "ADVENTURE", "SHMUP", "POINTNCLICK", "LOGO"]}
    escrever(PROJ / "project/settings.gbsres", cfg)

    col = json.loads((A.ARTE / "colisao.json").read_text())
    cena_dir = PROJ / "project/scenes/jardim"
    escrever(cena_dir / "scene.gbsres", {
        "_resourceType": "scene", "id": ID("cena-jardim"), "_index": 0, "type": "TOPDOWN", "name": "Jardim",
        "symbol": "scene_jardim", "x": 100, "y": 100, "width": A.LARG, "height": A.ALT,
        "backgroundId": ID("bg-jardim"), "tilesetId": "", "colorModeOverride": "none",
        "paletteIds": [], "spritePaletteIds": [], "autoFadeSpeed": 1, "script": scripts_cena(),
        "playerHit1Script": [], "playerHit2Script": [], "playerHit3Script": [],
        "collisions": colisoes_str(col)})
    atores, gats = montar_atores()
    for at in atores:
        escrever(cena_dir / "actors" / f"{at['name']}.gbsres", at)
    for g in gats:
        escrever(cena_dir / "triggers" / f"{g['name']}.gbsres", g)


if __name__ == "__main__":
    main()
