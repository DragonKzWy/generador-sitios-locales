# Video vertical de presentación (1080x1920, 30 s): escenas de texto, el sitio desplazándose dentro de un celular y la invitación final.
# Textos en ejemplo/textos_video.py. Uso: python3 video.py <id> <carpeta_con_pagina.png_musica.wav_secoes.json> <salida.mp4>
# Fuentes: variables FUENTE_BOLD y FUENTE_REG (archivos .ttf); si no existen, usa DejaVu Sans.
import sys, subprocess, pathlib
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 30.0
nome, pasta, saida = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3]
import os
_B = os.environ.get("FUENTE_BOLD", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf")
_R = os.environ.get("FUENTE_REG", "/usr/share/fonts/TTF/DejaVuSans.ttf")
f_bold = lambda s: ImageFont.truetype(_B, s)
f_reg = lambda s: ImageFont.truetype(_R, s)
BRANCO = (255, 255, 255)

def bloco(linhas, larg=900):
    medida = ImageDraw.Draw(Image.new("RGBA", (1, 1))); rend = []
    for txt, fonte, cor, esp in linhas:
        atual, out = "", []
        for p in txt.split():
            teste = (atual + " " + p).strip()
            if medida.textlength(teste, font=fonte) <= larg: atual = teste
            else: out.append(atual); atual = p
        out.append(atual); alt = int(fonte.size * 1.18)
        for i, l in enumerate(out): rend.append((l, fonte, cor, alt + (esp if i == len(out) - 1 else 0)))
    img = Image.new("RGBA", (larg, sum(r[3] for r in rend)), (0, 0, 0, 0)); d = ImageDraw.Draw(img); y = 0
    for l, fonte, cor, alt in rend: d.text((0, y), l, font=fonte, fill=cor); y += alt
    return img

import json
sys.path.insert(0, str(pathlib.Path(__file__).parent / "ejemplo"))
from textos_video import TEXTOS
cfg = TEXTOS[nome]
FUNDO, SUAVE, DEST, MOLD = cfg["cores"]
fb = {"b": f_bold, "r": f_reg}
cenas = [(a, b, bloco([(txt, fb[peso](tam), {"B": BRANCO, "S": SUAVE, "D": DEST}[cor], esp) for txt, peso, tam, cor, esp in linhas])) for a, b, linhas in cfg["cenas"]]
sec = [y * 2 for _, y in json.loads((pasta / "secoes.json").read_text())]
alvo = [0] + sec[1:5]
while len(alvo) < 5: alvo.append(alvo[-1])
chaves = [(14.6, alvo[0]), (16.0, alvo[0]), (17.0, alvo[1]), (18.8, alvo[1]), (19.8, alvo[2]), (21.4, alvo[2]), (22.4, alvo[3]), (24.0, alvo[3]), (25.0, alvo[4]), (26.0, alvo[4])]

pagina = Image.open(pasta / "pagina.png").convert("RGB")
SCR_W, SCR_H = 780, 1460
chaves = [(t, min(y, pagina.height - SCR_H)) for t, y in chaves]

def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)
def fade(t, a, b, f=0.45):
    if t < a or t > b: return 0.0
    return min(1.0, (t - a) / f, (b - t) / f)
def rolagem(t):
    if t <= chaves[0][0]: return 0
    for (t0, y0), (t1, y1) in zip(chaves, chaves[1:]):
        if t0 <= t <= t1: return y0 + (y1 - y0) * ease((t - t0) / (t1 - t0))
    return chaves[-1][1]

legenda_tel = bloco([(cfg.get("legenda", "Montei uma versão para vocês:"), f_bold(60), BRANCO, 0)])
BX, BY, BW, BH, R = (W - 840) // 2, 330, 840, 1520, 70
mold = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))
ImageDraw.Draw(mold).rounded_rectangle((0, 0, BW - 1, BH - 1), R, fill=MOLD + (255,))
mascara = Image.new("L", (SCR_W, SCR_H), 0)
ImageDraw.Draw(mascara).rounded_rectangle((0, 0, SCR_W - 1, SCR_H - 1), 46, fill=255)
SX, SY = BX + 30, BY + 30

fundo = Image.new("RGB", (W, H), FUNDO)
proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                         "-i", str(pasta / "musica.wav"), "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                         "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", saida], stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)):
    t = n / FPS; quadro = fundo.copy()
    for a, b, img in cenas:
        al = fade(t, a, b)
        if al > 0:
            sub = int((1 - ease(min(1, (t - a) / 0.6))) * 40)
            camada = img.copy(); camada.putalpha(camada.getchannel("A").point(lambda v: int(v * al)))
            quadro.paste(camada, (90, (H - img.height) // 2 + sub), camada)
    al = fade(t, 13.6, 26.0, 0.6)
    if al > 0:
        dy = int((1 - ease((t - 13.6) / 0.8)) * 500); ry = int(rolagem(t))
        tela = pagina.crop((0, ry, SCR_W, ry + SCR_H))
        camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        camada.paste(mold, (BX, BY + dy), mold); camada.paste(tela, (SX, SY + dy), mascara)
        camada.paste(legenda_tel, (90, 150 + dy), legenda_tel)
        camada.putalpha(camada.getchannel("A").point(lambda v: int(v * al)))
        quadro.paste(camada, (0, 0), camada)
    proc.stdin.write(quadro.tobytes())
proc.stdin.close(); proc.wait()
print("ok", saida)
