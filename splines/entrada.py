"""Lectura de puntos con separador explícito y coma decimal opcional."""

import re
from math import isfinite

from .matematica import ErrorSpline, validar_puntos


def numero(texto):
    try:
        valor = float(str(texto).strip().replace(",", "."))
    except (ValueError, TypeError, OverflowError) as exc:
        raise ErrorSpline("Ingresa un número válido; puedes usar punto o coma decimal.") from exc
    if not isfinite(valor):
        raise ErrorSpline("Ingresa un número finito; no se admite NaN ni infinito.")
    return valor


def leer_puntos(texto):
    """Acepta x;y, columnas con espacios o tabuladores y cabecera x;y."""
    puntos = []
    for linea, contenido in enumerate(texto.splitlines(), 1):
        contenido = contenido.strip()
        if not contenido:
            continue
        partes = contenido.split(";") if ";" in contenido else re.split(r"\s+", contenido)
        if not puntos and [p.strip().lower() for p in partes] == ["x", "y"]:
            continue
        if len(partes) != 2:
            raise ErrorSpline(f"Línea {linea}: escribe dos valores separados por ; o por un espacio.")
        try:
            puntos.append((numero(partes[0]), numero(partes[1])))
        except ErrorSpline as exc:
            raise ErrorSpline(f"Línea {linea}: {exc}") from exc
    return validar_puntos(puntos)
