"""Roda a ROM no PyBoy sem janela, aperta botões e lê variáveis do GB Studio."""
import re
from pathlib import Path
from pyboy import PyBoy

BOTOES = {"up", "down", "left", "right", "a", "b", "start", "select"}


class Emu:
    def __init__(self, rom, noi, variaveis=None):
        rom, noi = Path(rom), Path(noi)
        self.simbolos = {}
        for linha in noi.read_text().splitlines():
            m = re.match(r"DEF (\S+) 0x([0-9A-Fa-f]+)", linha)
            if m:
                self.simbolos[m.group(1)] = int(m.group(2), 16)
        self.globais = {}
        g = noi.with_suffix(".globals")
        if g.exists():
            for m in re.finditer(r"(VAR_\w+) = (\d+)", g.read_text()):
                self.globais[m.group(1)] = int(m.group(2))
        self.pb = PyBoy(str(rom), window="null", sound_emulated=False)

    def tick(self, frames=1):
        for _ in range(frames):
            self.pb.tick()

    def segurar(self, botao, frames):
        assert botao in BOTOES, botao
        self.pb.button_press(botao)
        self.tick(frames)
        self.pb.button_release(botao)
        self.tick(1)

    def endereco(self, simbolo):
        return self.simbolos[simbolo]

    def var(self, nome):
        idx = self.globais["VAR_" + nome.upper()]
        a = self.endereco("_script_memory") + 2 * idx
        v = self.pb.memory[a] | (self.pb.memory[a + 1] << 8)
        return v - 0x10000 if v >= 0x8000 else v

    def foto(self, caminho):
        Path(caminho).parent.mkdir(parents=True, exist_ok=True)
        self.pb.screen.image.save(str(caminho))

    def fechar(self):
        self.pb.stop(save=False)
