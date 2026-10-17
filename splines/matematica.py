"""Modelo del spline natural y comprobación de sus condiciones matemáticas.

Notación del curso: S_i(x)=a_i(x-x_i)^3+b_i(x-x_i)^2+c_i(x-x_i)+d_i.
M_i=S''(x_i). Si N es el número de nodos, existen N-1 tramos.
"""

from bisect import bisect_right
from dataclasses import dataclass
from math import isfinite

from .algebra import ErrorSistema, SolucionLineal, resolver_gauss


class ErrorSpline(ValueError):
    """Datos que no permiten construir o evaluar el spline solicitado."""


@dataclass(frozen=True)
class Tramo:
    inicio: float
    fin: float
    a: float
    b: float
    c: float
    d: float

    def evaluar(self, x: float, orden: int = 0) -> float:
        """Evalúa el polinomio o sus derivadas sin redondear los coeficientes."""
        t = x - self.inicio
        if orden == 0:
            return ((self.a * t + self.b) * t + self.c) * t + self.d
        if orden == 1:
            return (3 * self.a * t + 2 * self.b) * t + self.c
        if orden == 2:
            return 6 * self.a * t + 2 * self.b
        raise ErrorSpline("Solo se admiten órdenes de derivación 0, 1 y 2.")


@dataclass(frozen=True)
class Comprobacion:
    nombre: str
    error: float
    limite: float

    @property
    def cumple(self):
        return isfinite(self.error) and self.error <= self.limite


@dataclass(frozen=True)
class SplineNatural:
    x: tuple[float, ...]
    y: tuple[float, ...]
    h: tuple[float, ...]
    pendientes: tuple[float, ...]
    matriz: tuple[tuple[float, ...], ...]
    vector: tuple[float, ...]
    segundas: tuple[float, ...]
    tramos: tuple[Tramo, ...]
    solucion: SolucionLineal
    comprobaciones: tuple[Comprobacion, ...]

    @property
    def valido(self):
        return all(c.cumple for c in self.comprobaciones)

    @property
    def error_maximo(self):
        return max(c.error for c in self.comprobaciones)

    def indice_tramo(self, x):
        try:
            x = float(x)
        except (ValueError, TypeError, OverflowError) as exc:
            raise ErrorSpline("El valor a evaluar debe ser un número finito.") from exc
        if not isfinite(x) or not self.x[0] <= x <= self.x[-1]:
            raise ErrorSpline(f"Ingresa un valor entre {self.x[0]:g} y {self.x[-1]:g}.")
        return min(bisect_right(self.x, x) - 1, len(self.tramos) - 1)

    def evaluar(self, x, orden=0):
        indice = self.indice_tramo(x)
        return self.tramos[indice].evaluar(float(x), orden)

    def muestrear(self, por_tramo=50):
        """Genera la curva evaluando cada polinomio, sin interpolación externa."""
        if not isinstance(por_tramo, int) or por_tramo < 2:
            raise ErrorSpline("Se requieren al menos dos muestras por tramo.")
        puntos = []
        for i, tramo in enumerate(self.tramos):
            for j in range(por_tramo):
                if i and j == 0:
                    continue
                x = tramo.inicio + (tramo.fin - tramo.inicio) * j / (por_tramo - 1)
                puntos.append((x, tramo.evaluar(x)))
        if not all(isfinite(v) for punto in puntos for v in punto):
            raise ErrorSpline("No se puede representar la curva con estas magnitudes numéricas.")
        return puntos


def validar_puntos(puntos):
    datos = []
    try:
        for indice, punto in enumerate(puntos, 1):
            if len(punto) != 2:
                raise ErrorSpline(f"El punto {indice} debe contener x e y.")
            x, y = map(float, punto)
            if not isfinite(x) or not isfinite(y):
                raise ErrorSpline(f"El punto {indice} contiene un valor no finito.")
            if datos and x <= datos[-1][0]:
                raise ErrorSpline(
                    f"Punto {indice}: x debe ser mayor que {datos[-1][0]:g}. "
                    "Ordena las abscisas de menor a mayor, sin repetirlas."
                )
            datos.append((x, y))
    except (TypeError, ValueError, OverflowError) as exc:
        if isinstance(exc, ErrorSpline):
            raise
        raise ErrorSpline("Cada punto debe contener dos números finitos.") from exc
    if len(datos) < 2:
        raise ErrorSpline("Ingresa al menos dos puntos para construir un tramo.")
    return tuple(datos)


def construir_sistema(x, y):
    """Construye el mismo sistema completo A·M=B del avance original."""
    n = len(x)
    h = [x[i + 1] - x[i] for i in range(n - 1)]
    if not all(isfinite(v) and v > 0 for v in h):
        raise ErrorSpline("Las distancias entre nodos exceden el rango numérico disponible.")
    pendientes = [(y[i + 1] - y[i]) / h[i] for i in range(n - 1)]
    if not all(map(isfinite, pendientes)):
        raise ErrorSpline("Las pendientes exceden el rango numérico disponible.")
    a = [[0.0] * n for _ in range(n)]
    b = [0.0] * n
    a[0][0] = a[-1][-1] = 1.0
    for i in range(1, n - 1):
        a[i][i - 1] = h[i - 1]
        a[i][i] = 2 * (h[i - 1] + h[i])
        a[i][i + 1] = h[i]
        b[i] = 6 * (pendientes[i] - pendientes[i - 1])
    return a, b, h, pendientes


def comprobar(x, y, tramos, matriz, vector, segundas, tolerancia=1e-8):
    """Compara valores calculados con tolerancia absoluta y relativa combinada."""
    resultados = []

    def comparar(nombre, obtenido, esperado, escala=None):
        if escala is None:
            escala = max(1.0, abs(obtenido), abs(esperado))
        resultados.append(Comprobacion(nombre, abs(obtenido - esperado), tolerancia * escala))

    for i, t in enumerate(tramos):
        comparar(f"Interpolación · S{i}(x{i}) = y{i}", t.evaluar(x[i]), y[i])
        comparar(f"Interpolación · S{i}(x{i + 1}) = y{i + 1}", t.evaluar(x[i + 1]), y[i + 1])
        if i + 1 < len(tramos):
            siguiente = tramos[i + 1]
            comparar(f"Continuidad · S en x{i + 1}", t.evaluar(x[i + 1]), siguiente.evaluar(x[i + 1]))
            comparar(f"Continuidad · S' en x{i + 1}", t.evaluar(x[i + 1], 1), siguiente.evaluar(x[i + 1], 1))
            comparar(f"Continuidad · S'' en x{i + 1}", t.evaluar(x[i + 1], 2), siguiente.evaluar(x[i + 1], 2))
    comparar("Frontera natural · S''(x0) = 0", tramos[0].evaluar(x[0], 2), 0.0)
    comparar("Frontera natural · S''(x final) = 0", tramos[-1].evaluar(x[-1], 2), 0.0)
    for i, fila in enumerate(matriz):
        productos = [v * m for v, m in zip(fila, segundas)]
        comparar(f"Sistema · fila {i + 1} de A·M = B", sum(productos), vector[i],
                 max(1.0, sum(map(abs, productos)), abs(vector[i])))
    return tuple(resultados)


def calcular_spline(puntos) -> SplineNatural:
    """Construye, resuelve y valida un spline natural con listas y aritmética."""
    datos = validar_puntos(puntos)
    x, y = tuple(zip(*datos))
    try:
        matriz, vector, h, pendientes = construir_sistema(x, y)
        solucion = resolver_gauss(matriz, vector)
        m = solucion.valores
        tramos = tuple(
            Tramo(x[i], x[i + 1], (m[i + 1] - m[i]) / (6 * h[i]), m[i] / 2,
                  pendientes[i] - h[i] * (2 * m[i] + m[i + 1]) / 6, y[i])
            for i in range(len(h))
        )
        if not all(isfinite(v) for t in tramos for v in (t.a, t.b, t.c, t.d)):
            raise ErrorSpline("Los datos producen coeficientes fuera del rango numérico.")
        comprobaciones = comprobar(x, y, tramos, matriz, vector, m)
    except (ErrorSistema, OverflowError, ZeroDivisionError) as exc:
        raise ErrorSpline(f"No se pudo construir el spline: {exc}") from exc
    return SplineNatural(x, y, tuple(h), tuple(pendientes), tuple(map(tuple, matriz)),
                         tuple(vector), m, tramos, solucion, comprobaciones)
