# Genera el sitio de ejemplo leyendo los textos de panel/contenido.json (lo que se edita en el panel).
# Uso: python3 panel/construir.py  ->  salida/panaderia-la-esquina/index.html
# El diseño sigue en motor.py y estilo.css; el panel solo cambia el contenido.
import html, json, pathlib, sys
RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path[:0] = [str(RAIZ), str(RAIZ / "ejemplo")]
import motor, negocio

d = json.loads((RAIZ / "panel" / "contenido.json").read_text(encoding="utf-8"))
e = lambda t: html.escape(str(t or "").strip(), quote=False)

c = negocio.panaderia()
c["hero"]["h1"], c["hero"]["lead"] = e(d["titulo"]), e(d["texto"])
servicios = next(s for s in c["secoes"] if s["tipo"] == "servicos")
fotos = [i.get("foto") for i in servicios["itens"]]
servicios["itens"] = [dict(t=e(p["nombre"]), d=e(p["descripcion"]), **({"foto": fotos[k]} if k < len(fotos) and fotos[k] else {}))
                      for k, p in enumerate(d["productos"])]
next(s for s in c["secoes"] if s.get("id") == "cafe")["ps"] = [e(d["cafe"])]
print(c["id"], motor.gravar(c), "MB")
