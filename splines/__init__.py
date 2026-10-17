"""Interpolación con splines cúbicos naturales, sin paquetes de cálculo."""

from .matematica import ErrorSpline, SplineNatural, calcular_spline

__all__ = ["ErrorSpline", "SplineNatural", "calcular_spline"]
