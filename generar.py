# Genera los sitios en salida/<id>/index.html. Uso: python3 generar.py [nombre_de_funcion ...]
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent / "ejemplo"))
import motor, negocio
for fn in negocio.TODOS:
    if len(sys.argv) > 1 and fn.__name__ not in sys.argv[1:]: continue
    c = fn(); print(f'{c["id"]:32} {motor.gravar(c)} MB')
