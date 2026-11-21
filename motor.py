# Motor del generador (nov/2026). Genera un HTML de un solo archivo con las fotos incrustadas.
# Comentarios internos en portugués (idioma original del proyecto).
import base64, io, json, pathlib, re, urllib.parse
from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parent / "ejemplo"      # carpeta con fotos/<cliente>/
SAIDA = pathlib.Path(__file__).resolve().parent / "salida"
BI = False                                                      # bilíngue (cliente dos EUA)
LANG = "pt"                                                     # "es" = site só em espanhol (América Latina)

def T(pt, en=None):
    if BI and en is not None:
        return f'<span lang="pt">{pt}</span><span lang="en">{en}</span>'
    return pt

def L(pt, en, es=None):  # rótulos do próprio motor
    if LANG == "es" and es is not None: return es
    return T(pt, en) if BI else pt

def esc(s): return s.replace('"', '&quot;')

# ---------- fotos ----------
_cache = {}
def b64(rel, lado=1500):
    k = (rel, lado)
    if k not in _cache:
        im = Image.open(RAIZ / "fotos" / rel).convert("RGB")
        im.thumbnail((lado, lado))
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=74, optimize=True, progressive=True)
        _cache[k] = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    return _cache[k]

def img(rel, alt="", cls="", lado=1400, eager=False, pos=None):
    st = f' style="object-position:{pos}"' if pos else ""
    return (f'<img src="{b64(rel, lado)}" alt="{esc(alt)}"{(" class=%s" % chr(34)+cls+chr(34)) if cls else ""}'
            f'{"" if eager else " loading=" + chr(34) + "lazy" + chr(34)} decoding="async"{st}>')

# ---------- ícones (traço simples, funcionais) ----------
ZAP = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.46 1.32 4.97L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91A9.85 9.85 0 0 0 12.04 2Zm5.8 14.13c-.24.68-1.42 1.3-1.95 1.38-.5.07-1.13.1-1.82-.12-.42-.13-.96-.31-1.65-.61-2.9-1.25-4.8-4.17-4.94-4.36-.15-.2-1.18-1.57-1.18-3s.75-2.13 1.01-2.42c.27-.29.58-.36.78-.36h.56c.18 0 .42-.07.66.5.24.58.82 2 .89 2.15.07.15.12.32.02.51-.1.2-.15.32-.29.49-.15.17-.31.38-.44.51-.15.15-.3.3-.13.6.17.29.76 1.25 1.63 2.02 1.12 1 2.06 1.3 2.35 1.45.29.15.46.12.63-.07.17-.2.73-.85.92-1.14.2-.29.39-.24.66-.15.27.1 1.7.8 1.99.95.29.15.49.22.56.34.07.12.07.7-.17 1.38Z"/></svg>'
TEL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>'
PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg>'
ESTRELA = '<svg viewBox="0 0 20 20" aria-hidden="true"><path fill="currentColor" d="M10 1.5l2.6 5.5 6 .7-4.4 4.1 1.2 5.9L10 14.8l-5.4 2.9 1.2-5.9L1.4 7.7l6-.7z"/></svg>'

def estrelas(nota):
    v = float(str(nota).replace(",", "."))
    def cls(i):
        if v >= i + .75: return "on"
        if v >= i + .25: return "meio"
        return ""
    return '<span class="estrelas" aria-hidden="true">' + "".join(
        f'<i class="{cls(i)}">{ESTRELA}{ESTRELA if cls(i) == "meio" else ""}</i>' for i in range(5)) + "</span>"

# ---------- botões ----------
def b_zap(c, pt="Chamar no WhatsApp", en="Message on WhatsApp", cls="btn pri"):
    return f'<a class="{cls}" href="{c["zap_link"]}" target="_blank" rel="noopener">{ZAP}{T(pt, en)}</a>'
def b_tel(c, pt="Ligar", en="Call", cls="btn sec"):
    return f'<a class="{cls}" href="tel:{c["tel"]}">{TEL}{T(pt, en)}</a>'
def b_rota(c, cls="btn sec"):
    return f'<a class="{cls}" href="{c["rota"]}" target="_blank" rel="noopener">{PIN}{L("Ver rota", "Get directions", "Cómo llegar")}</a>'
def b_acao(c, cls="btn pri"):
    a = c["acao"]
    if a[0] == "zap": return b_zap(c, a[1], a[2] if len(a) > 2 else None, cls)
    return b_tel(c, a[1], a[2] if len(a) > 2 else None, cls)

# ---------- seções ----------
def nota_linha(c):
    if not c.get("nota"): return ""
    return (f'<p class="nota">{estrelas(c["nota"])}<b>{c["nota"]}</b>'
            f'<span>{L("no Google, com", "on Google,", "en Google, con")} {c["avals_n"]} {L("avaliações", "reviews", "reseñas")}</span></p>')

def hero(c, h):
    v = h.get("tipo", "split")
    fotos = h["fotos"]
    acoes = f'<div class="acoes">{b_acao(c)}{h.get("sec") or b_rota(c)}</div>'
    txt = (f'<div class="h-txt">{nota_linha(c)}<h1>{h["h1"]}</h1><p class="lead">{h["lead"]}</p>{acoes}'
           f'<p class="agora" data-agora hidden></p></div>')
    if v == "cheio":
        f = fotos[0]
        return (f'<section class="hero cheio" id="inicio"><div class="h-foto">{img(f[0], f[1], lado=1800, eager=True, pos=h.get("pos"))}</div>'
                f'<div class="wrap">{txt}</div></section>')
    lado = h.get("lado", "dir")
    if len(fotos) == 1:
        fx = f'<div class="h-foto um">{img(fotos[0][0], fotos[0][1], lado=1700, eager=True, pos=h.get("pos"))}</div>'
    else:
        fx = '<div class="h-foto duo">' + "".join(
            f'<figure>{img(p, a, lado=1400, eager=True)}</figure>' for p, a in fotos[:2]) + "</div>"
    return f'<section class="hero split {lado}" id="inicio">{txt}{fx}</section>'

def cab(h2, lead=None, extra=""):
    return f'<div class="cab"><h2>{h2}</h2>{f"<p class=lead>{lead}</p>" if lead else ""}{extra}</div>'

def servicos(c, s):
    itens = s["itens"]
    fotos = [i for i in itens if i.get("foto")]
    painel = "".join(f'<figure data-i="{k}"{" class=on" if k == 0 else ""}>{img(i["foto"], i.get("alt", ""), lado=1100)}</figure>'
                     for k, i in enumerate(fotos))
    linhas, k = "", 0
    for i in itens:
        di = ""
        thumb = ""
        if i.get("foto"):
            di = f' data-i="{k}"'; thumb = f'<span class="thumb" data-de="{k}"></span>'; k += 1
        tag = "a" if i.get("link") else "div"
        href = f' href="{i["link"]}" target="_blank" rel="noopener"' if i.get("link") else ' tabindex="0"'
        linhas += f'<{tag} class="linha"{di}{href}>{thumb}<span class="lt"><h3>{i["t"]}</h3><p>{i["d"]}</p></span></{tag}>'
    return (f'<section class="serv{" sem-foto" if not fotos else ""}" id="{s.get("id", "servicos")}"><div class="wrap">{cab(s["h2"], s.get("lead"))}'
            f'<div class="serv-g"><div class="lista">{linhas}</div>'
            f'{f"<div class=painel aria-hidden=true>{painel}</div>" if fotos else ""}</div>{s.get("nota_rodape", "")}</div></section>')

def tira(c, s):
    figs = "".join(f'<figure tabindex="0">{img(p, a, lado=960)}</figure>' for p, a in s["fotos"])
    return (f'<section class="tira-s" id="{s.get("id", "trabalhos")}"><div class="wrap">{cab(s["h2"], s.get("lead"))}</div>'
            f'<div class="tira">{figs}</div></section>')

def mosaico(c, s):
    figs = "".join(f'<figure class="m{k}">{img(p, a, lado=1300)}</figure>' for k, (p, a) in enumerate(s["fotos"]))
    n = len(s["fotos"])
    return (f'<section class="mos-s" id="{s.get("id", "espaco")}"><div class="wrap">{cab(s["h2"], s.get("lead"))}'
            f'<div class="mosaico n{n}">{figs}</div></div></section>')

def destaque(c, s):
    lista = ""
    if s.get("lista"):
        tag = "ol" if s.get("ordem") else "ul"
        lista = f'<{tag} class="pontos">' + "".join(f"<li>{x}</li>" for x in s["lista"]) + f"</{tag}>"
    q = ""
    if s.get("citacao"):
        q = f'<blockquote class="cit"><p>{s["citacao"][0]}</p><cite>{s["citacao"][1]}</cite></blockquote>'
    botao = s.get("botao", "")
    fotos = s["fotos"]
    fx = "".join(f'<figure>{img(p, a, lado=1400)}</figure>' for p, a in fotos)
    return (f'<section class="dest {s.get("lado", "esq")}{" faixa" if s.get("faixa") else ""}" id="{s.get("id", "")}"><div class="wrap dest-g">'
            f'<div class="d-foto n{len(fotos)}">{fx}</div>'
            f'<div class="d-txt"><h2>{s["h2"]}</h2>{"".join(f"<p class=lead>{p}</p>" for p in s.get("ps", []))}{lista}{q}{botao}</div></div></section>')

def passos(c, s):
    li = "".join(f'<li><span class="pn">{k+1}</span><h3>{t}</h3><p>{d}</p></li>' for k, (t, d) in enumerate(s["itens"]))
    return (f'<section class="passos-s" id="{s.get("id", "como")}"><div class="wrap">{cab(s["h2"], s.get("lead"))}'
            f'<ol class="passos n{len(s["itens"])}">{li}</ol>{s.get("rodape", "")}</div></section>')

def faixa(c, s):
    return (f'<section class="faixa-s" id="{s.get("id", "")}"><div class="wrap faixa-g"><div><h2>{s["h2"]}</h2>'
            f'{"".join(f"<p class=lead>{p}</p>" for p in s.get("ps", []))}{s.get("botao", "")}</div>'
            f'<div class="faixa-dir">{s["dir"]}</div></div></section>')

def avaliacoes(c, s):
    av = s["itens"]
    prim, resto = av[0], av[1:]
    q = lambda a, cls: f'<blockquote class="{cls}"><p>{a[0]}</p><cite>{a[1]}</cite></blockquote>'
    placar = ""
    if c.get("nota"):
        placar = (f'<div class="placar"><b>{c["nota"]}</b>{estrelas(c["nota"])}'
                  f'<span>{c["avals_n"]} {L("avaliações no Google", "Google reviews", "reseñas en Google")}</span></div>')
    return (f'<section class="aval-s" id="avaliacoes"><div class="wrap"><div class="aval-top">{placar}'
            f'<div><h2>{s["h2"]}</h2>{q(prim, "grande")}</div></div>'
            f'<div class="aval-g n{len(resto)}">{"".join(q(a, "peq") for a in resto)}</div></div></section>')

def faq(c, s):
    d = "".join(f'<details><summary>{p}</summary><p>{r}</p></details>' for p, r in s["itens"])
    return f'<section class="faq-s" id="duvidas"><div class="wrap faq-g">{cab(s["h2"], s.get("lead"))}<div class="faq">{d}</div></div></section>'

def visita(c, s):
    hor = "".join(f'<tr data-dias="{d}"><td>{a}</td><td>{b}</td></tr>' for d, a, b in c["horas"])
    foto = f'<figure class="v-foto">{img(s["foto"][0], s["foto"][1], lado=1300)}</figure>' if s.get("foto") else ""
    mapa = (f'<div class="mapa"><iframe title="{"Mapa / Map" if BI else "Mapa"}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
            f'src="https://www.google.com/maps?q={urllib.parse.quote(c["mapa_q"])}&amp;output=embed"></iframe></div>')
    extra = s.get("extra", "")
    return (f'<section class="vis-s" id="visita"><div class="wrap vis-g"><div class="v-txt"><h2>{s["h2"]}</h2>'
            f'<p class="endereco">{c["end_curto"]}</p><p class="end-det">{c["end_det"]}</p>'
            f'<table class="horas"><caption>{L("Horário", "Hours", "Horario")}</caption>{hor}</table>'
            f'<div class="acoes">{b_acao(c)}{b_rota(c)}</div>{extra}</div>'
            f'<div class="v-dir{" com-foto" if foto else ""}">{foto}{mapa}</div></div></section>')

def html_livre(c, s): return s["html"]

SECOES = dict(servicos=servicos, tira=tira, mosaico=mosaico, destaque=destaque, passos=passos,
              faixa=faixa, avaliacoes=avaliacoes, faq=faq, visita=visita, livre=html_livre)

# ---------- página ----------
CSS = (pathlib.Path(__file__).parent / "estilo.css").read_text
JS = (pathlib.Path(__file__).parent / "script.js").read_text

def pagina(c):
    global BI, LANG
    BI = c.get("bi", False); LANG = c.get("lang", "pt")
    corpo = hero(c, c["hero"]) + "".join(SECOES[s["tipo"]](c, s) for s in c["secoes"])
    links = "".join(f'<a href="#{i}">{n}</a>' for i, n in c["menu"])
    lang = ('<div class="lang" role="group" aria-label="Idioma / Language"><button type="button" data-l="pt" aria-pressed="true">PT</button>'
            '<button type="button" data-l="en" aria-pressed="false">EN</button></div>') if BI else ""
    demo = L(f'Versão de demonstração feita para {c["nome"]}.', f'Demo version made for {c["nome"]}.', f'Versión de demostración hecha para {c["nome"]}.')
    rod_cont = " ".join(x for x in [
        f'<a href="{c["zap_link"]}" target="_blank" rel="noopener">WhatsApp</a>' if c.get("zap_link") else "",
        f'<a href="tel:{c["tel"]}">{c["tel_vis"]}</a>' if c.get("tel") else "",
        f'<a href="{c["insta"]}" target="_blank" rel="noopener">Instagram</a>' if c.get("insta") else ""] if x)
    sec_barra = (b_tel(c, "Llamar", None, "btn sec") if LANG == "es" else b_tel(c, "Ligar", "Call", "btn sec")) if c["acao"][0] == "zap" and c.get("tel") else b_rota(c, "btn sec")
    agenda = json.dumps(c.get("agenda", {}))
    marca = c.get("marca_html") or f'<span class="m-nome">{c["marca"]}</span>'
    return f"""<!doctype html>
<html lang="{ {"es": c.get("lang_html", "es")}.get(LANG, "pt-BR") }" data-lang="{LANG}" data-type="place">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{c["titulo"]}</title>
<meta name="description" content="{esc(c["desc"])}">
<meta name="robots" content="noindex,nofollow">
<meta name="page-type" content="place"><meta name="site-kind" content="other"><meta name="page-kind" content="place">
<meta name="theme-color" content="{c["cores"]["bg"]}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{c["fontes"]}&display=swap" rel="stylesheet">
<style>:root{{{";".join(f"--{k}:{v}" for k, v in c["cores"].items())};--fh:{c["fh"]};--fb:{c["fb"]};{c.get("vars", "")}}}
{CSS()}
{c.get("css", "")}</style>
</head>
<body class="{c.get("classe", "")}">
<a class="pular" href="#inicio">{L("Pular para o conteúdo", "Skip to content", "Saltar al contenido")}</a>
<div class="demo">{demo}</div>
<header class="topo"><div class="wrap topo-g"><a class="marca" href="#inicio">{marca}</a>
<nav class="menu">{links}</nav><div class="dir">{lang}{b_acao(c, "btn pri peq")}</div></div></header>
<main>{corpo}</main>
<footer class="rodape"><div class="wrap rod-g"><div><p class="r-nome">{c["nome"]}</p><p>{c["end_curto"]}, {c["end_det"]}</p></div>
<div class="r-cont">{rod_cont}</div>
<p class="r-cred">{c.get("credito") or L("Fotos e avaliações do perfil público no Google, usadas só nesta demonstração.", "Photos and reviews from the public Google profile, used only in this demo.", "Fotos y reseñas del perfil público en Google, usadas solo en esta demostración.")}</p></div></footer>
<div class="barra">{b_acao(c, "btn pri")}{sec_barra}</div>
<script>window.AGENDA={agenda};window.TZ="{c.get("tz", "America/Fortaleza")}";{"window.H24=true;" if c.get("h24") else ""}</script>
<script>{JS()}</script>
</body></html>"""

def agenda(spec):
    """'0-4 08:00-18:00; 5 08:00-12:00' -> {dia(0=seg): [[ini,fim],...]}"""
    out = {}
    for parte in spec.split(";"):
        parte = parte.strip()
        if not parte: continue
        dias, *faixas = parte.split()
        if "-" in dias: a, b = map(int, dias.split("-")); ds = range(a, b + 1)
        else: ds = [int(x) for x in dias.split(",")]
        for d in ds:
            out.setdefault(str(d), []).extend([f.split("-") for f in faixas])
    return out

def gravar(c):
    pasta = SAIDA / c["id"]; pasta.mkdir(parents=True, exist_ok=True)
    h = pagina(c)
    (pasta / "index.html").write_text(h)
    return round(len(h) / 1e6, 2)
