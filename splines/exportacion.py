"""Figuras SVG para el informe, generadas sin bibliotecas externas."""

from html import escape


def grafica_svg(spline, titulo="Spline cúbico natural"):
    puntos = spline.muestrear(60)
    xmin, xmax = spline.x[0], spline.x[-1]
    ymin, ymax = min(y for _, y in puntos), max(y for _, y in puntos)
    margen = (ymax - ymin) * .12 if ymax != ymin else max(1, abs(ymin) * .12)
    ymin, ymax = ymin - margen, ymax + margen

    def pantalla(x, y):
        return 90 + (x - xmin) / (xmax - xmin) * 930, 470 - (y - ymin) / (ymax - ymin) * 340

    partes = ['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="560" viewBox="0 0 1100 560" role="img">',
              f'<title>{escape(titulo)}</title>', '<rect width="1100" height="560" fill="#fff"/>',
              '<g font-family="Segoe UI, Arial, sans-serif">',
              f'<text x="60" y="50" font-size="25" font-weight="bold" fill="#172338">{escape(titulo)}</text>',
              f'<text x="60" y="80" font-size="14" fill="#64748B">{len(spline.x)} nodos · {len(spline.tramos)} tramos · Frontera natural</text>']
    for i in range(6):
        x = xmin + (xmax - xmin) * i / 5
        y = ymin + (ymax - ymin) * i / 5
        px, _ = pantalla(x, ymin)
        _, py = pantalla(xmin, y)
        partes += [f'<path d="M90 {py:.2f}H1020 M{px:.2f} 130V470" fill="none" stroke="#E8EDF5"/>',
                   f'<text x="75" y="{py + 5:.2f}" text-anchor="end" font-size="12" fill="#64748B">{y:.4g}</text>',
                   f'<text x="{px:.2f}" y="495" text-anchor="middle" font-size="12" fill="#64748B">{x:.4g}</text>']
    partes.append('<path d="M90 130V470H1020" fill="none" stroke="#A8B6CA"/>')
    coords = " ".join(f"{px:.3f},{py:.3f}" for px, py in (pantalla(x, y) for x, y in puntos))
    partes.append(f'<polyline points="{coords}" fill="none" stroke="#6554C0" stroke-width="3" stroke-linejoin="round"/>')
    for x, y in zip(spline.x, spline.y):
        px, py = pantalla(x, y)
        partes.append(f'<circle cx="{px:.3f}" cy="{py:.3f}" r="5" fill="#087F8C" stroke="white" stroke-width="2"><title>({x:g}; {y:g})</title></circle>')
    partes += ['<text x="1028" y="475" fill="#64748B" font-size="14">x</text>',
               '<text x="77" y="121" fill="#64748B" font-size="14">y</text>',
               '<text x="60" y="535" font-size="13" fill="#64748B">SplineLab · Curva evaluada con los polinomios calculados por el programa.</text>',
               '</g></svg>']
    return "\n".join(partes)
