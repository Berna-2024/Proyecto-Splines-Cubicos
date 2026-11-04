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
    """Flujo de la tercera entrega; conectores repetidos evitan cruces largos."""
    partes = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="2580" viewBox="0 0 2400 2580" role="img" aria-labelledby="titulo descripcion">',
        '<title id="titulo">SplineLab · Diagrama de flujo · Semana 11</title>',
        '<desc id="descripcion">Spline natural, comparación con Lagrange y acciones. Los círculos con la misma letra conectan bloques separados.</desc>',
        '<defs><marker id="flecha" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0 0L10 4L0 8" fill="#8191AB"/></marker></defs>',
        '<rect width="2400" height="2580" fill="#F4F6FA"/>',
        '<g font-family="Segoe UI, Arial, sans-serif" fill="#172338">',
        '<text x="60" y="55" font-size="30" font-weight="bold">Del punto a la comparación</text>',
        '<text x="60" y="90" font-size="18" fill="#64748B">SplineLab · Tercera entrega de Álgebra Lineal · Semana 11</text>',
    ]

    def texto(x, y, lineas, size=17, color="#172338"):
        for i, linea in enumerate(lineas):
            py = y + (i - (len(lineas) - 1) / 2) * 24
            partes.append(f'<text x="{x}" y="{py}" text-anchor="middle" font-size="{size}" fill="{color}">{escape(linea)}</text>')

    def caja(x, y, lineas, ancho=540, alto=82, color="#FFFFFF", borde="#D5DDE9"):
        partes.append(f'<rect x="{x-ancho/2}" y="{y-alto/2}" width="{ancho}" height="{alto}" rx="13" fill="{color}" stroke="{borde}"/>')
        texto(x, y + 6, lineas)

    def decision(x, y, lineas):
        partes.append(f'<path d="M{x} {y-65}L{x+250} {y}L{x} {y+65}L{x-250} {y}Z" fill="#F0ECFA" stroke="#BFB3E1"/>')
        texto(x, y + 5, lineas, size=16)

    def flecha(d, etiqueta=None, x=0, y=0):
        partes.append(f'<path d="{d}" fill="none" stroke="#8191AB" stroke-width="1.7" marker-end="url(#flecha)"/>')
        if etiqueta:
            texto(x, y, [etiqueta], size=15, color="#64748B")

    def conector(x, y, letra):
        partes.append(f'<circle cx="{x}" cy="{y}" r="23" fill="#EAE6F8" stroke="#BFB3E1"/>')
        texto(x, y + 6, [letra], size=18)

    for x, titulo in ((400, "01 · SPLINE NATURAL"), (1200, "02 · LAGRANGE Y ACCIONES"), (2000, "03 · EVALUAR Y EXPORTAR")):
        partes.append(f'<rect x="{x-365}" y="125" width="730" height="2300" rx="18" fill="#FAFBFE" stroke="#D5DDE9"/>')
        texto(x, 167, [titulo], size=20, color="#6554C0")

    # Bloque 1: cálculo original, sin cambiar el orden de Gauss y sustitución.
    caja(400, 235, ["INICIO · Mostrar interfaz y ejemplo inicial"], color="#EAE6F8")
    caja(400, 355, ["Ingresar puntos, cargar ejemplo o importar CSV"])
    decision(400, 490, ["¿2 a 80 puntos finitos", "y x estrictamente creciente?"])
    caja(400, 625, ["Calcular distancias h y pendientes"])
    caja(400, 745, ["Construir A·M = B", "Frontera natural: M inicial = M final = 0"])
    caja(400, 865, ["Gauss con pivoteo parcial escalado"])
    decision(400, 1000, ["¿Sistema resoluble?"])
    caja(400, 1135, ["Sustitución regresiva · Obtener M"])
    caja(400, 1255, ["Calcular a, b, c y d por intervalo"])
    caja(400, 1375, ["Comprobar interpolación, continuidad,", "fronteras naturales y residuo A·M − B"])
    caja(400, 1495, ["Preparar muestras del spline"])
    decision(400, 1630, ["¿Cumple la tolerancia?"])
    for inicio, fin in ((276,314),(396,425),(555,584),(666,704),(786,824),
                        (906,935),(1065,1094),(1176,1214),(1296,1334),
                        (1416,1454),(1536,1565)):
        flecha(f"M400 {inicio}V{fin}")
    texto(430, 575, ["Sí"], size=15)
    texto(430, 1085, ["Sí"], size=15)
    caja(240, 1770, ["Estado: Verificado"], ancho=280, alto=60, color="#E9F5F4")
    caja(560, 1770, ["Estado: Revisar precisión"], ancho=300, alto=60, color="#FFF0F2")
    flecha("M150 1630H90V1770H100", "Sí", 113, 1610)
    flecha("M650 1630H710V1770H710", "No", 689, 1610)
    flecha("M240 1800V1850H400V1887")
    flecha("M560 1800V1850H400")
    conector(400, 1910, "A")
    # Los fallos se agrupan en un carril lateral exclusivo.
    flecha("M150 490H65V2000H130", "No", 106, 470)
    flecha("M150 1000H65", "No", 105, 980)
    caja(400, 2000, ["Error de entrada, sistema o magnitudes:", "invalidar ambos resultados y mostrar mensaje"], color="#FFF0F2")
    flecha("M400 2041V2077")
    conector(400, 2100, "I")
    conector(65, 355, "I")
    flecha("M88 355H130")
    texto(400, 2160, ["Errores numéricos de cálculo o muestreo", "también siguen el bloque de error."], size=16, color="#64748B")
    conector(400, 2240, "D")
    flecha("M400 2263V2294")
    caja(400, 2330, ["Editar / limpiar: invalidar ambos resultados", "Ejemplo / CSV válido: recalcular; volver a I"], alto=72)

    # Bloque 2: Lagrange es opcional; su fallo no invalida el spline.
    conector(1200, 230, "A")
    flecha("M1200 253V289")
    caja(1200, 330, ["Construir Lagrange baricéntrico", "con los mismos nodos del spline"])
    flecha("M1200 371V419")
    caja(1200, 460, ["Comprobar nodos y muestrear Lagrange:", "finitud, cancelación y magnitudes"])
    flecha("M1200 501V545")
    decision(1200, 610, ["¿Comprobaciones y muestreo", "aceptables?"])
    caja(1040, 775, ["Lagrange disponible", "Advertir con >20 nodos"], ancho=300, alto=80, color="#E9F5F4")
    caja(1380, 775, ["Advertir y desactivar", "solo Lagrange; conservar S"], ancho=330, alto=80, color="#FFF0F2")
    flecha("M1200 675V705H1040V735", "Sí", 1080, 694)
    flecha("M1450 610H1535V705H1380V735", "No / error", 1490, 590)
    flecha("M1470 330H1550V775H1545")
    texto(1505, 310, ["Error"], size=15)
    flecha("M1040 815V865H1200V899")
    flecha("M1380 815V865H1200")
    caja(1200, 940, ["Mostrar spline y nodos; Lagrange según casilla", "Mismos ejes y dominio de interpolación"])
    flecha("M1200 981V1029")
    caja(1200, 1070, ["Polinomios, procedimiento y validación", "del spline; verificación de nodos de Lagrange"])
    flecha("M1200 1111V1195")
    conector(885, 1260, "R")
    flecha("M908 1260H950")
    decision(1200, 1260, ["Acción del usuario"])
    # Opciones separadas; cada continuación se identifica por una letra.
    flecha("M1200 1325V1375")
    caja(1200, 1420, ["Mostrar / ocultar Lagrange si disponible", "Redibujar; el spline permanece visible"], alto=90)
    flecha("M1200 1465V1497")
    conector(1200, 1520, "R")
    flecha("M1450 1260H1550V1630H1500", "Otras acciones", 1480, 1235)
    caja(1200, 1630, ["Evaluar / clic → E     Exportar → X", "Cambiar datos → D     Cerrar → FIN"], ancho=600, alto=90)
    for x, letra in ((980, "E"), (1125, "X"), (1270, "D")):
        flecha(f"M{x} 1675V1727")
        conector(x, 1750, letra)
    flecha("M1420 1675V1720")
    caja(1420, 1750, ["FIN"], ancho=150, alto=60, color="#EAE6F8")
    texto(1200, 1900, ["R: volver a las acciones con el estado actual.", "Ocultar Lagrange no impide su evaluación.", "Su fallo numérico conserva el spline."], size=17, color="#64748B")
    texto(1200, 2050, ["Ejemplo e importación válida recalculan.", "CSV inválido: conservar texto e invalidar resultados.", "Cancelar diálogo: conservar estado.", "Cerrar está disponible en cualquier momento."], size=16, color="#64748B")

    # Bloque 3: evaluación y exportación, con retornos sin cruces.
    conector(2000, 230, "E")
    flecha("M2000 253V295")
    decision(2000, 360, ["¿x finito dentro del dominio?"])
    caja(2000, 490, ["Evaluar S(x); mostrar tramo y derivadas"])
    flecha("M2000 425V449", "Sí", 2030, 443)
    caja(2000, 610, ["Si x es inválido: mostrar mensaje", "y conservar los interpoladores → R"], color="#FFF0F2")
    flecha("M1750 360H1670V610H1730", "No", 1707, 340)
    flecha("M2270 490H2310V695H2000V725")
    decision(2000, 790, ["¿Lagrange disponible?"])
    flecha("M1750 790H1680V1200H1730", "No", 1706, 770)
    caja(2000, 930, ["Evaluar P(x) y diferencia absoluta |S − P|"])
    flecha("M2000 855V889", "Sí", 2030, 877)
    decision(2000, 1060, ["¿Evaluación aceptable?"])
    flecha("M2000 971V995")
    caja(2000, 1200, ["Mostrar S; si P es aceptable, mostrar P y |S − P|", "Si falla: advertir, retirar P y desactivar comparación"], alto=100)
    flecha("M2000 1125V1150", "Sí", 2030, 1140)
    flecha("M2250 1060H2320V1200H2270", "No", 2290, 1040)
    flecha("M2000 1250V1287")
    conector(2000, 1310, "R")
    conector(2000, 1420, "X")
    flecha("M2000 1443V1495")
    decision(2000, 1560, ["Formato solicitado"])
    caja(1840, 1720, ["TXT: informe", "del spline"], ancho=280, alto=80)
    caja(2180, 1720, ["SVG: spline, nodos, leyenda", "P si disponible y visible"], ancho=330, alto=80)
    flecha("M1750 1560H1685V1720H1700", "TXT", 1712, 1540)
    flecha("M2250 1560H2335V1720H2345", "SVG", 2300, 1540)
    flecha("M2180 1760V1795H2000V1835")
    decision(2000, 1900, ["¿Muestreo de P aceptable", "o P no solicitado?"])
    caja(1840, 2070, ["Guardar SVG"], ancho=280, alto=80)
    caja(2180, 2070, ["Guardar SVG solo con S", "y aviso: Lagrange omitido"], ancho=330, alto=80, color="#FFF0F2")
    flecha("M2000 1965V1990H1840V2030", "Sí", 1880, 1980)
    flecha("M2250 1900H2335V1990H2180V2030", "No", 2290, 1880)
    flecha("M1840 2110V2170H2000V2207")
    flecha("M2180 2110V2170H2000")
    flecha("M1840 1760V1790H1660V2240H1977")
    conector(2000, 2230, "R")
    texto(2000, 2310, ["Cancelar: conservar estado. Error de archivo:", "mostrar mensaje y volver a R."], size=16, color="#64748B")
    texto(1200, 2470, ["Conectores: A → Lagrange · R → acciones · E → evaluar · X → exportar · D → cambiar datos · I → entrada"], size=18)
    texto(1200, 2510, ["La diferencia entre interpolaciones no es error respecto de una función original. El muestreo no garantiza precisión uniforme."], size=17, color="#64748B")
    partes.append('</g></svg>')
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
