# Textos del video de cada negocio. Cada línea: (texto, peso b/r, tamaño, color B/S/D, espacio después).
# Estructura usada: problema, consecuencia, solución.
def fim(titulo, detalle, pregunta):
    return (26.0, 30.0, [(titulo, "b", 84, "B", 50), (detalle, "r", 50, "S", 70), (pregunta, "b", 72, "D", 0)])

TEXTOS = {
"panaderia-la-esquina": dict(legenda="Preparé una versión para ustedes:", cores=((42, 30, 22), (240, 228, 212), (232, 150, 90), (14, 10, 8)), cenas=[
    (0.0, 3.8, [("El problema:", "b", 70, "D", 20), ("tus clientes te buscan en Google antes de salir de casa.", "b", 78, "B", 0)]),
    (3.8, 8.0, [("La panadería tiene 210 reseñas.", "b", 80, "B", 40), ("Pero no tiene página web.", "b", 76, "D", 0)]),
    (8.0, 12.2, [("La consecuencia:", "b", 70, "D", 20), ("quien quiere ver el pan y el horario termina en otro lugar.", "b", 74, "B", 0)]),
    (12.2, 13.6, [("La solución:", "b", 96, "B", 0)]),
    fim("La página de La Esquina.", "Con los panes, el café, el horario y el botón para pedir por WhatsApp.", "¿Quieres verla en tu celular?")]),
}
