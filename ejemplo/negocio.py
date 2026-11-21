# Negocio FICTICIO de ejemplo: nombre, teléfono, reseñas e imágenes son inventados.
import motor as M
from motor import agenda
from ayudas import base, cores, F, zap

def panaderia():
    M.BI = False; M.LANG = "es"; f = "panaderia/"
    return base(id="panaderia-la-esquina", lang="es", lang_html="es-CL", tz="America/Santiago",
     nome="Panadería La Esquina (ejemplo ficticio)", marca="La Esquina",
     titulo="Panadería La Esquina · Ejemplo del generador",
     desc="Sitio de ejemplo generado con el generador de sitios para negocios locales. Negocio ficticio.",
     fontes=F("Fraunces:opsz,wght@9..144,500;9..144,700", "Karla:wght@400;500;700"), fh="'Fraunces',serif", fb="'Karla'",
     vars="--hw:700;--hs:-.02em;--hl:1;--r:4px;--rp:999px",
     cores=cores("#FAF5EE", "#2A1E16", "#6E5F54", "#A4471E", "#FFFFFF", "#F0E4D4", band="#2A1E16", band_ink="#FAF5EE", star="#D08A1E"),
     nota="4,8", avals_n=210, tel="+56900000000", tel_vis="+56 9 0000 0000",
     zap_link=zap("56900000000", "¡Hola! Quiero hacer un pedido."), acao=("zap", "Pedir por WhatsApp"),
     end_curto="Calle Ejemplo 123", end_det="Valparaíso, Chile", mapa_q="Valparaíso, Chile",
     credito="Negocio, reseñas e imágenes ficticios, creados solo para mostrar el generador.",
     horas=[("0,1,2,3,4,5", "Lunes a sábado", "7:00 a 20:00"), ("6", "Domingo", "8:00 a 14:00")],
     agenda=agenda("0-5 07:00-20:00; 6 08:00-14:00"),
     menu=[("panes", "Panes"), ("cafe", "Café"), ("avaliacoes", "Reseñas"), ("visita", "Visítanos")],
     hero=dict(tipo="split", lado="dir", fotos=[(f + "hogazas.jpg", "Ilustración de hogazas"), (f + "marraquetas.jpg", "Ilustración de marraquetas")],
        h1="Pan del día en el barrio, desde las 7",
        lead="Hogazas, marraquetas y pastelería hechas cada mañana. Pide por WhatsApp y pasa a buscar."),
     secoes=[
      dict(tipo="servicos", id="panes", h2="Lo que sale del horno",
           itens=[dict(t="Hogazas", d="Masa de fermentación lenta.", foto=f + "hogazas.jpg"),
                  dict(t="Marraquetas", d="Crujientes, para el desayuno y la once.", foto=f + "marraquetas.jpg"),
                  dict(t="Pastelería", d="Dulces para acompañar el café.", foto=f + "dulces.jpg"),
                  dict(t="Pedidos por encargo", d="Cajas para reuniones y cumpleaños.")]),
      dict(tipo="destaque", lado="esq", faixa=True, id="cafe", fotos=[(f + "cafe.jpg", "Ilustración de café"), (f + "vitrina.jpg", "Ilustración de vitrina")],
           h2="Un café para quedarse un rato", ps=["Café de grano y mesas para tomarlo con calma."],
           citacao=("Reseña de ejemplo: el pan de siempre, recién hecho.", "Cliente ficticio")),
      dict(tipo="avaliacoes", h2="Lo que dicen los clientes (ejemplo)",
           itens=[("Reseña de ejemplo: atención cercana y pan siempre fresco.", "Cliente ficticio 1"),
                  ("Reseña de ejemplo: las marraquetas salen calentitas a las 7.", "Cliente ficticio 2"),
                  ("Reseña de ejemplo: el café está muy bueno.", "Cliente ficticio 3")]),
      dict(tipo="visita", h2="De lunes a domingo")])

TODOS = [panaderia]
