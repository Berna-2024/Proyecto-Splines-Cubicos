"""Eliminación de Gauss con pivoteo parcial escalado y sustitución regresiva.

No se modifica el sistema recibido. La escala de cada fila permite comparar
pivotes aunque las ecuaciones utilicen magnitudes diferentes.
"""

from dataclasses import dataclass
from math import isfinite


class ErrorSistema(ValueError):
    """Sistema inválido, singular o numéricamente no resoluble."""


@dataclass(frozen=True)
class SolucionLineal:
    valores: tuple[float, ...]
    triangular: tuple[tuple[float, ...], ...]
    terminos: tuple[float, ...]
    pasos: tuple[str, ...]


def resolver_gauss(matriz, vector) -> SolucionLineal:
    """Resuelve A·z=b mediante operaciones elementales escritas en Python."""
    n = len(vector)
    if not n or len(matriz) != n or any(len(fila) != n for fila in matriz):
        raise ErrorSistema("El sistema debe ser cuadrado y no vacío.")
    a = [list(map(float, fila)) for fila in matriz]
    b = list(map(float, vector))
    if not all(isfinite(v) for fila in a for v in fila) or not all(map(isfinite, b)):
        raise ErrorSistema("El sistema contiene valores no finitos.")
    escalas = [max(map(abs, fila)) for fila in a]
    if any(escala == 0 for escala in escalas):
        raise ErrorSistema("El sistema no tiene solución única: hay una fila nula.")
    pasos = []
    omitidos = 0

    def registrar(texto):
        nonlocal omitidos
        if len(pasos) < 250:
            pasos.append(texto)
        else:
            omitidos += 1

    for k in range(n):
        pivote = max(range(k, n), key=lambda i: abs(a[i][k]) / escalas[i])
        if abs(a[pivote][k]) / escalas[pivote] < 1e-14:
            raise ErrorSistema("El sistema es singular o tiene un pivote demasiado pequeño.")
        if pivote != k:
            a[k], a[pivote] = a[pivote], a[k]
            b[k], b[pivote] = b[pivote], b[k]
            escalas[k], escalas[pivote] = escalas[pivote], escalas[k]
            registrar(f"Intercambiar F{k + 1} y F{pivote + 1}.")
        for i in range(k + 1, n):
            if a[i][k] == 0:
                continue
            factor = a[i][k] / a[k][k]
            a[i][k] = 0.0
            for j in range(k + 1, n):
                a[i][j] -= factor * a[k][j]
            b[i] -= factor * b[k]
            registrar(f"F{i + 1} ← F{i + 1} − ({factor:.8g}) F{k + 1}.")

    z = [0.0] * n
    for i in range(n - 1, -1, -1):
        suma = sum(a[i][j] * z[j] for j in range(i + 1, n))
        z[i] = (b[i] - suma) / a[i][i]
        registrar(f"M{i} = ({b[i]:.8g} − ({suma:.8g})) / ({a[i][i]:.8g}) = {z[i]:.8g}")
    if not all(map(isfinite, z)):
        raise ErrorSistema("Las magnitudes de los datos exceden la precisión disponible.")
    if omitidos:
        pasos.append(f"Se omitieron {omitidos} operaciones de la vista detallada por tamaño.")
    return SolucionLineal(tuple(z), tuple(map(tuple, a)), tuple(b), tuple(pasos))
