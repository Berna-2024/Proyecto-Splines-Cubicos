"""Interpolación global de Lagrange en forma baricéntrica, sin dependencias."""

from dataclasses import dataclass
from math import exp, fsum, isfinite, log

from .matematica import Comprobacion, ErrorSpline, validar_puntos


@dataclass(frozen=True)
class Lagrange:
    x: tuple[float, ...]
    y: tuple[float, ...]
    log_pesos: tuple[float, ...]

    def evaluar(self, x):
        try:
            x = float(x)
            if not isfinite(x) or not self.x[0] <= x <= self.x[-1]:
                raise ErrorSpline(f"Ingresa un valor entre {self.x[0]:g} y {self.x[-1]:g}.")
            for nodo, valor in zip(self.x, self.y):
                if x == nodo:
                    return valor
            # w_i = 1 / producto(x_i-x_j). Se normalizan los términos
            # en logaritmos para evitar desbordamientos y subdesbordamientos.
            logs = [w - log(abs(x - nodo)) for w, nodo in zip(self.log_pesos, self.x)]
            mayor = max(logs)
            terminos = [exp(v - mayor) * (-1 if (len(self.x) - 1 - i) % 2 else 1)
                        * (1 if x > nodo else -1)
                        for i, (v, nodo) in enumerate(zip(logs, self.x))]
            denominador = fsum(terminos)
            if abs(denominador) <= 1e-10 * fsum(map(abs, terminos)):
                raise ErrorSpline("Lagrange no es fiable: cancelación numérica excesiva.")
            escala = max(map(abs, self.y)) or 1.0
            resultado = (fsum(t * (y / escala) for t, y in zip(terminos, self.y))
                         / denominador) * escala
            if not isfinite(resultado):
                raise ErrorSpline("Lagrange excede el rango numérico disponible.")
            return resultado
        except (ValueError, TypeError, OverflowError, ZeroDivisionError) as exc:
            if isinstance(exc, ErrorSpline):
                raise
            raise ErrorSpline("No se puede evaluar Lagrange con estas magnitudes numéricas.") from exc

    @property
    def comprobaciones(self):
        return tuple(Comprobacion(f"Lagrange · P(x{i}) = y{i}", abs(self.evaluar(x) - y),
                                  1e-8 * max(1, abs(y)))
                     for i, (x, y) in enumerate(zip(self.x, self.y)))

    def muestrear(self, abscisas):
        puntos = [(x, self.evaluar(x)) for x in abscisas]
        # Reserva margen para la transformación a píxeles y los límites.
        if any(abs(y) > 1e150 for _, y in puntos):
            raise ErrorSpline("Las magnitudes de Lagrange no permiten una gráfica fiable.")
        return puntos


def calcular_lagrange(puntos):
    datos = validar_puntos(puntos)
    x, y = tuple(zip(*datos))
    try:
        pesos = tuple(-fsum(log(abs(xi - xj)) for j, xj in enumerate(x) if i != j)
                      for i, xi in enumerate(x))
        if not all(map(isfinite, pesos)):
            raise ErrorSpline("Las distancias entre nodos exceden el rango de Lagrange.")
    except (OverflowError, ValueError) as exc:
        raise ErrorSpline("No se pueden construir los pesos de Lagrange.") from exc
    return Lagrange(x, y, pesos)
