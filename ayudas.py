# Funciones de apoyo para escribir los datos de cada negocio.
import urllib.parse

def zap(num, msg):
    """Enlace de WhatsApp con mensaje listo."""
    return f"https://wa.me/{num}?text={urllib.parse.quote(msg)}"

def rota(q):
    """Enlace de Google Maps para llegar."""
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)

def base(**k):
    """Completa los campos que se pueden deducir (búsqueda del mapa, ruta y zona horaria)."""
    k.setdefault("mapa_q", k["nome"] + ", " + k["end_curto"] + ", " + k["end_det"])
    k.setdefault("rota", rota(k["mapa_q"]))
    k.setdefault("tz", "America/Santiago")
    return k

def cores(bg, ink, muted, accent, on_accent, surface, band=None, band_ink=None, accent_text=None, star=None):
    """Paleta del sitio: fondo, texto, texto suave, acento, texto sobre acento, superficie y franja."""
    c = {"bg": bg, "ink": ink, "muted": muted, "accent": accent, "on-accent": on_accent, "surface": surface,
         "band": band or ink, "band-ink": band_ink or bg}
    if accent_text: c["accent-text"] = accent_text
    if star: c["star"] = star
    return c

F = lambda *fam: "&".join("family=" + f for f in fam)   # fuentes de Google Fonts
