"""Genera informes y figuras de ejecuciones reales del modelo matemático.

No genera ni simula capturas de la interfaz de escritorio.
"""

import json
import sys
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from splines.ejemplos import EJEMPLOS
from splines.entrada import leer_puntos
from splines.exportacion import grafica_svg
from splines.matematica import calcular_spline
from splines.presentacion import informe


def diagrama_svg():
    """Diagrama vectorial del cálculo y las acciones de exploración."""
    partes = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1340" height="1840" viewBox="0 0 1340 1840" role="img">',
        '<title>Diagrama de flujo de SplineLab</title>',
        '<defs><marker id="flecha" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0 0L10 4L0 8" fill="#8191AB"/></marker></defs>',
        '<rect width="1340" height="1840" fill="#F4F6FA"/>',
        '<g font-family="Segoe UI, Arial, sans-serif" fill="#172338">',
        '<text x="70" y="55" font-size="29" font-weight="bold">Del punto a la curva</text>',
        '<text x="70" y="85" font-size="15" fill="#64748B">SplineLab · Flujo del cálculo natural, verificación y exploración de resultados</text>',
    ]

    def texto(x, y, lineas, color="#172338", size=15):
        for i, linea in enumerate(lineas):
            partes.append(f'<text x="{x}" y="{y + (i - (len(lineas)-1)/2)*21:.1f}" text-anchor="middle" font-size="{size}" fill="{color}">{escape(linea)}</text>')

    def caja(x, y, lineas, ancho=390, alto=64, color="#FFFFFF", borde="#D5DDE9", redondo=13):
        partes.append(f'<rect x="{x-ancho/2}" y="{y-alto/2}" width="{ancho}" height="{alto}" rx="{redondo}" fill="{color}" stroke="{borde}"/>')
        texto(x, y+5, lineas)

    def decision(x, y, lineas):
        partes.append(f'<path d="M{x} {y-48}L{x+190} {y}L{x} {y+48}L{x-190} {y}Z" fill="#F0ECFA" stroke="#BFB3E1"/>')
        texto(x, y+4, lineas, size=14)

    def flecha(d, etiqueta=None, x=0, y=0):
        partes.append(f'<path d="{d}" fill="none" stroke="#8191AB" stroke-width="1.7" marker-end="url(#flecha)"/>')
        if etiqueta:
            partes.append(f'<text x="{x}" y="{y}" font-size="13" fill="#64748B">{escape(etiqueta)}</text>')

    x = 520
    caja(x, 140, ["INICIO"], ancho=180, alto=42, color="#EAE6F8", redondo=21)
    caja(x, 220, ["Mostrar interfaz y ejemplo inicial"])
    caja(x, 320, ["Ingresar puntos, cargar ejemplo", "o importar un archivo CSV"])
    decision(x, 430, ["¿2 a 80 puntos finitos", "y x estrictamente creciente?"])
    caja(x, 540, ["Calcular distancias h y pendientes m"])
    caja(x, 640, ["Construir A·M = B", "Frontera natural: M inicial = M final = 0"])
    caja(x, 740, ["Eliminación de Gauss", "con pivoteo parcial escalado"])
    decision(x, 850, ["¿Sistema resoluble?"])
    caja(x, 960, ["Sustitución regresiva", "Obtener segundas derivadas M"])
    caja(x, 1060, ["Calcular a, b, c y d por intervalo"])
    caja(x, 1160, ["Comprobar interpolación, continuidad,", "fronteras naturales y residuo del sistema"])
    decision(x, 1270, ["¿Cumple la tolerancia?"])
    caja(x, 1390, ["Mostrar curva, polinomios,", "procedimiento y estado de validación"])
    caja(x, 1500, ["Explorar resultados o cambiar datos"], color="#E9F5F4", borde="#A8D2CE")
    caja(x, 1740, ["Cerrar aplicación · FIN"], ancho=270, alto=46, color="#EAE6F8", redondo=23)

    conexiones = [(161,188),(252,288),(352,382),(478,508),(572,608),(672,708),(772,802),
                  (898,928),(992,1028),(1092,1128),(1192,1222),(1422,1468)]
    for inicio, fin in conexiones:
        flecha(f"M{x} {inicio}V{fin}")
    texto(544, 500, ["Sí"], size=12)
    texto(544, 917, ["Sí"], size=12)
    flecha("M520 1532V1717", "Cerrar", 535, 1660)

    caja(1030, 430, ["Mostrar el error de entrada", "y permitir corregir"], ancho=360, color="#FFF0F2", borde="#EDC7CF")
    flecha("M710 430H850", "No", 765, 420)
    flecha("M1030 398V320H715", "Corregir", 1050, 355)
    caja(1030, 850, ["Informar sistema inválido", "y revisar los datos"], ancho=360, color="#FFF0F2", borde="#EDC7CF")
    flecha("M710 850H850", "No", 765, 840)
    flecha("M1210 850H1260V320H1210", "Volver a la entrada", 1040, 785)
    # La flecha de regreso utiliza el margen derecho y conecta con el ciclo de entrada.
    flecha("M1210 320H715")

    caja(1030, 1230, ["Estado: Verificado"], ancho=360, alto=50, color="#E9F5F4", borde="#A8D2CE")
    caja(1030, 1330, ["Estado: Revisar precisión"], ancho=360, alto=50, color="#FFF0F2", borde="#EDC7CF")
    flecha("M710 1270H790V1230H850", "Sí", 762, 1250)
    flecha("M520 1318V1330H850", "No", 760, 1320)
    flecha("M1210 1230H1260V1390H715")
    flecha("M1030 1355V1390H715")

    caja(1030, 1480, ["Evaluar x dentro del dominio", "Mostrar valor, tramo y derivadas"], ancho=360)
    caja(1030, 1580, ["Exportar informe TXT", "o gráfica vectorial SVG"], ancho=360)
    flecha("M715 1500H790V1480H850", "Evaluar", 750, 1465)
    flecha("M790 1500V1580H850", "Exportar", 790, 1550)
    flecha("M1210 1480H1260V1660H740V1525H715")
    flecha("M1210 1580H1260V1660H740V1525H715")
    caja(135, 1500, ["Modificar datos", "Invalidar resultados", "y volver a calcular"], ancho=240, alto=88)
    flecha("M325 1500H255", "Editar", 265, 1488)
    flecha("M135 1456V320H325")
    partes += ['<text x="70" y="1800" font-size="13" fill="#64748B">En una consulta fuera del dominio se muestra un mensaje y se conserva el spline calculado.</text>',
               '</g></svg>']
    return "\n".join(partes)


def main():
    salida = RAIZ / "docs" / "evidencias"
    salida.mkdir(parents=True, exist_ok=True)
    resumen = []
    nombres = ["ejemplo_x4", "contorno_pato", "funcion_racional", "datos_lineales"]
    for nombre_archivo, (nombre, (texto, _)) in zip(nombres, EJEMPLOS.items()):
        spline = calcular_spline(leer_puntos(texto))
        (salida / f"{nombre_archivo}.txt").write_text(informe(spline), encoding="utf-8")
        (salida / f"{nombre_archivo}.svg").write_text(grafica_svg(spline, nombre), encoding="utf-8")
        resumen.append({"ejemplo": nombre, "nodos": len(spline.x), "tramos": len(spline.tramos),
                        "condiciones": len(spline.comprobaciones), "verificado": spline.valido,
                        "error_absoluto_maximo": spline.error_maximo})
    (salida / "resumen.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    (RAIZ / "docs" / "diagrama_flujo.svg").write_text(diagrama_svg(), encoding="utf-8")
    print("Generados cuatro informes, cuatro gráficas, resumen y diagrama de flujo.")
    return 0 if all(e["verificado"] for e in resumen) else 1


if __name__ == "__main__":
    raise SystemExit(main())
