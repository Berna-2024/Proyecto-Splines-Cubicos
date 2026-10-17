"""Formato compartido entre interfaz, consola e informe exportable."""

from datetime import datetime


def formato(valor, precision=7):
    # Solo se redondea el texto; los cálculos conservan todos los decimales.
    if valor == 0:
        return "0"
    return f"{valor:.{precision}g}"


def polinomio(tramo, indice):
    base = f"(x − {formato(tramo.inicio)})" if tramo.inicio >= 0 else f"(x + {formato(-tramo.inicio)})"
    terminos = []
    for coeficiente, factor in ((tramo.a, f"{base}³"), (tramo.b, f"{base}²"),
                                (tramo.c, base), (tramo.d, "")):
        if coeficiente == 0:
            continue
        termino = f"{formato(abs(coeficiente))}{factor}"
        if not terminos:
            terminos.append(("−" if coeficiente < 0 else "") + termino)
        else:
            terminos.append((" − " if coeficiente < 0 else " + ") + termino)
    return f"S{indice}(x) = {''.join(terminos) or '0'}"


def matriz_texto(matriz, vector):
    return "\n".join("[ " + " ".join(f"{v:11.6g}" for v in fila) + f" ] | {b:12.6g}"
                     for fila, b in zip(matriz, vector))


def procedimiento(spline):
    lineas = [
        "01  DATOS Y DISTANCIAS ENTRE NODOS",
        "N nodos definen N − 1 tramos. Las abscisas deben ser estrictamente crecientes.",
        "hᵢ = xᵢ₊₁ − xᵢ     mᵢ = (yᵢ₊₁ − yᵢ) / hᵢ", "",
        "  i           xᵢ           yᵢ           hᵢ           mᵢ",
    ]
    for i, (x, y) in enumerate(zip(spline.x, spline.y)):
        extra = f"{spline.h[i]:13.6g}{spline.pendientes[i]:13.6g}" if i < len(spline.h) else "       —            —"
        lineas.append(f"{i:3d}{x:13.6g}{y:13.6g}{extra}")
    lineas += ["", "02  SISTEMA A·M = B", "Mᵢ representa S''(xᵢ).",
               "Frontera natural: M₀ = M final = 0.",
               "Interior: hᵢ₋₁Mᵢ₋₁ + 2(hᵢ₋₁ + hᵢ)Mᵢ + hᵢMᵢ₊₁ = 6(mᵢ − mᵢ₋₁).", "",
               matriz_texto(spline.matriz, spline.vector), "", "03  ELIMINACIÓN DE GAUSS",
               "Se elige el mayor pivote relativo a la escala de su fila.",
               "Después de eliminar, se aplica sustitución regresiva.", ""]
    lineas.extend(spline.solucion.pasos)
    lineas += ["", "Sistema triangular [U | b]:", "",
               matriz_texto(spline.solucion.triangular, spline.solucion.terminos), "",
               "04  SEGUNDAS DERIVADAS EN LOS NODOS"]
    lineas.extend(f"M{i} = {formato(v, 12)}" for i, v in enumerate(spline.segundas))
    lineas += ["", "05  COEFICIENTES POR INTERVALO", "Sᵢ(x) = aᵢ(x−xᵢ)³ + bᵢ(x−xᵢ)² + cᵢ(x−xᵢ) + dᵢ",
               "aᵢ = (Mᵢ₊₁ − Mᵢ)/(6hᵢ)       bᵢ = Mᵢ/2",
               "cᵢ = mᵢ − hᵢ(2Mᵢ + Mᵢ₊₁)/6   dᵢ = yᵢ", ""]
    for i, tramo in enumerate(spline.tramos):
        lineas += [f"Intervalo {i}: [{formato(tramo.inicio)}, {formato(tramo.fin)}]", polinomio(tramo, i), ""]
    lineas += ["06  VALIDACIÓN", "Se comprueba interpolación, continuidad de S, S' y S'',",
               "las dos fronteras naturales y el residuo del sistema A·M − B.",
               "Criterio: error ≤ 10⁻⁸ × escala. La escala es al menos 1.",
               "En A·M = B se utiliza la suma de magnitudes de los términos de cada fila.",
               "Los valores mostrados se redondean; la validación usa los valores completos."]
    return "\n".join(lineas)


def informe(spline):
    lineas = ["SPLINELAB · INFORME DE EJECUCIÓN", datetime.now().astimezone().isoformat(timespec="seconds"),
               "Método: spline cúbico natural / Gauss con pivoteo parcial escalado.",
               "Cálculo realizado con listas, ciclos y aritmética de Python.",
               f"Nodos: {len(spline.x)} | Tramos: {len(spline.tramos)}",
               f"Estado: {'VERIFICADO' if spline.valido else 'REVISAR PRECISIÓN'}", "", procedimiento(spline),
               "", "DETALLE DE COMPROBACIONES", ""]
    for c in spline.comprobaciones:
        lineas.append(f"{'OK' if c.cumple else 'FALLA'} | {c.nombre} | error={c.error:.12g} | límite={c.limite:.12g}")
    return "\n".join(lineas) + "\n"
