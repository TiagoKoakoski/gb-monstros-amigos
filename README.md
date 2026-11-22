# Monstros Amigos — versão Game Boy

O mesmo jogo do `~/Projetos/jogos/monstros-amigos` (Godot), refeito no **GB Studio 4.3.2**.
Jardim com quatro monstros fofos, cada um perdeu uma coisa; a criança leva cada item
ao dono. Sem texto, sem inimigos, sem tempo, sem perder.

## Como jogar

- **Na TV / no PC:** `./jogar.sh` — abre o navegador em tela cheia. Controle USB/Bluetooth
  funciona direto; no teclado são as setas (ou WASD). Ctrl+C no terminal encerra.
- **Em emulador:** `build/monstros-amigos.gb` roda em qualquer emulador de Game Boy
  (mGBA, RetroArch...). Gerar com `./ferramentas/compilar.sh rom`.

Regras:
- **Andar:** direcional / analógico. **Nenhum botão é obrigatório**: pegar e entregar é só encostar.
- Drácula quer o **morceguinho de pelúcia**, Frankenstein a **flor**, a Múmia o **rolo de faixa**,
  o Lobisomem a **bola**. O balão em cima de cada um mostra o desenho do que ele quer.
- O item pego flutua em cima da cabeça. Carrega um por vez; encostar em outro item não troca.
- Levar pro monstro errado não tira nada: ele faz "?" e balança.
- 5 segundos sem conseguir avançar: um **vaga-lume** aparece, voa um pouco na direção do próximo
  objetivo, pisca e some. Se a criança continuar parada, ele volta e guia mais um trecho.
- Ajudou os quatro: os monstros dançam com uma musiquinha. Depois dela, **A, B, Start ou Select** recomeça.

## Abrir e mexer no GB Studio

Abra `projeto/project.gbsproj` no GB Studio (menu de aplicativos → GB Studio) e aperte Play.
O projeto é **gerado** por `ferramentas/gerar_projeto.py`: mudanças feitas só na interface do
GB Studio somem na próxima geração. Para algo definitivo, mude os scripts e gere de novo.

## Gerar, compilar e testar

```bash
V=~/Projetos/jogos/_ferramentas/venv/bin
$V/python ferramentas/gerar_arte.py       # arte/ (sprites e jardim em 4 tons, desenhados em código)
$V/python ferramentas/gerar_projeto.py    # projeto/ (cena, atores, gatilhos, eventos)
./ferramentas/compilar.sh rom             # build/monstros-amigos.gb
./ferramentas/compilar.sh web             # build/web/
$V/pytest tests -q                        # 29 testes: rodam a ROM no emulador PyBoy
$V/python ferramentas/jogar_sozinho.py    # joga a partida inteira e fotografa em build/fotos/
```

`compilar.sh` usa a CLI do GB Studio montada a partir do código-fonte v4.3.2 em
`~/Projetos/jogos/_ferramentas/gb-studio` (Node 21.7.1 em `_ferramentas/node21`). Os testes leem as
variáveis do jogo direto da memória do emulador (`ferramentas/emu.py`).

## Teste com a criança (o que observar)

Isso nenhum teste automático mede:
1. O navegador reconhece o controle? (Às vezes precisa apertar um botão do controle uma vez.)
2. Ele entende o balão como "o que o monstro quer"?
3. Percebe o vaga-lume e segue?
4. Fica preso em algum lugar ou se frustra?
5. O volume e o ritmo dos bipes estão confortáveis?

## Estrutura

- `ferramentas/gerar_arte.py` — todos os sprites como texto (1 letra por pixel) + o mapa do jardim.
- `ferramentas/gerar_projeto.py` — monta o projeto GB Studio; a lógica fica em `script_item`,
  `script_monstro`, `script_relogio` (vaga-lume) e `festa`.
- `ferramentas/compilar.sh`, `ferramentas/emu.py`, `ferramentas/jogar_sozinho.py`.
- `tests/` — regras (missão), vaga-lume, festa/recomeço, arte, build web.
- `docs/` — design e plano.

Arte e sons 100% próprios (sons são os bipes sintetizados do próprio motor).
