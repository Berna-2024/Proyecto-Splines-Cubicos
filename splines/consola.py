"""Modo de consola conservado para practicar el procedimiento sin interfaz."""

import sys

from .entrada import numero
from .matematica import ErrorSpline, calcular_spline
from .presentacion import informe


def iniciar():
    # Mantiene legibles los símbolos también al redirigir la salida a un archivo.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print("SPLINELAB · SPLINE CÚBICO NATURAL")
    try:
        while True:
            try:
                cantidad = int(input("Cantidad de puntos (mínimo 2): "))
                if cantidad < 2:
                    raise ValueError
                break
            except ValueError:
                print("Escribe un número entero mayor o igual a 2.")
        puntos = []
        for i in range(cantidad):
            while True:
                try:
                    x = numero(input(f"x{i}: "))
                    y = numero(input(f"y{i}: "))
                    if puntos and x <= puntos[-1][0]:
                        raise ErrorSpline("x debe ser mayor que la abscisa anterior.")
                    puntos.append((x, y))
                    break
                except ErrorSpline as exc:
                    print(exc)
        spline = calcular_spline(puntos)
        print(informe(spline))
    except ErrorSpline as exc:
        print(f"No se pudo calcular: {exc}")
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nIngreso cancelado.")
        return 0
    return 0
