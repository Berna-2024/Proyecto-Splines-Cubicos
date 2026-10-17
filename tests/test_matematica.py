"""Casos conocidos y propiedades matemáticas; solo biblioteca estándar."""

import ast
import importlib
import random
import subprocess
import sys
import unittest
from pathlib import Path

from splines.algebra import ErrorSistema, resolver_gauss
from splines.ejemplos import EJEMPLOS
from splines.entrada import leer_puntos
from splines.matematica import ErrorSpline, calcular_spline, comprobar
from splines.presentacion import informe, polinomio


class AlgebraTests(unittest.TestCase):
    def test_intercambio_de_filas_y_solucion(self):
        a = [[0, 2], [1, 3]]
        b = [4, 7]
        solucion = resolver_gauss(a, b)
        self.assertEqual(solucion.valores, (1.0, 2.0))
        self.assertTrue(any("Intercambiar" in p for p in solucion.pasos))
        self.assertEqual(a, [[0, 2], [1, 3]])
        self.assertEqual(b, [4, 7])

    def test_pivoteo_con_filas_de_distinta_escala(self):
        solucion = resolver_gauss([[1e-18, 0], [0, 1e18]], [2e-18, 3e18])
        self.assertEqual(solucion.valores, (2.0, 3.0))

    def test_singular_no_se_resuelve_silenciosamente(self):
        with self.assertRaises(ErrorSistema):
            resolver_gauss([[1, 2], [2, 4]], [3, 6])

    def test_sistema_invalido(self):
        for matriz, vector in (([], []), ([[1, 2]], [1]), ([[float("nan")]], [1])):
            with self.subTest(matriz=matriz), self.assertRaises(ErrorSistema):
                resolver_gauss(matriz, vector)


class SplineTests(unittest.TestCase):
    def test_ejemplo_x4_del_curso(self):
        s = calcular_spline([(0, 0), (1, 1), (2, 16), (3, 81)])
        esperados = [(0.4, 0, 0.6, 0), (12, 1.2, 1.8, 1), (-12.4, 37.2, 40.2, 16)]
        for t, esperado in zip(s.tramos, esperados):
            for obtenido, valor in zip((t.a, t.b, t.c, t.d), esperado):
                self.assertAlmostEqual(obtenido, valor, places=11)
        for obtenido, valor in zip(s.segundas, (0, 2.4, 74.4, 0)):
            self.assertAlmostEqual(obtenido, valor, places=11)
        self.assertAlmostEqual(s.evaluar(1.5), 3.7, places=11)
        self.assertTrue(s.valido)

    def test_tres_nodos_con_solucion_a_mano(self):
        s = calcular_spline([(0, 0), (1, 1), (2, 0)])
        self.assertEqual(s.segundas, (0, -3, 0))
        self.assertAlmostEqual(s.evaluar(.5), .6875)
        self.assertAlmostEqual(s.evaluar(1.5), .6875)
        self.assertEqual(s.evaluar(1, 1), 0)

    def test_dos_puntos_producen_recta(self):
        s = calcular_spline([(1, 3), (4, 9)])
        self.assertEqual(s.segundas, (0, 0))
        self.assertEqual(s.evaluar(2), 5)
        self.assertEqual(s.evaluar(2, 1), 2)
        self.assertEqual(s.evaluar(2, 2), 0)
        self.assertTrue(s.valido)

    def test_constante_y_no_uniforme(self):
        for funcion in (lambda x: 7, lambda x: 2 * x + 1):
            xs = [-2, -.5, 1, 4.5, 8]
            s = calcular_spline([(x, funcion(x)) for x in xs])
            for x in (-2, -1, 0, 3, 8):
                self.assertAlmostEqual(s.evaluar(x), funcion(x))
            self.assertTrue(s.valido)

    def test_todos_los_ejemplos(self):
        for nombre, (texto, _) in EJEMPLOS.items():
            with self.subTest(nombre=nombre):
                s = calcular_spline(leer_puntos(texto))
                self.assertTrue(s.valido)
                for x, y in zip(s.x, s.y):
                    self.assertAlmostEqual(s.evaluar(x), y, places=10)

    def test_propiedades_en_datos_no_uniformes(self):
        azar = random.Random(331)
        for _ in range(12):
            x = 0
            puntos = []
            for _ in range(9):
                x += azar.uniform(.1, 2)
                puntos.append((x, azar.uniform(-10, 10)))
            s = calcular_spline(puntos)
            self.assertTrue(s.valido)
            for i, t in enumerate(s.tramos[:-1]):
                for orden in (0, 1, 2):
                    self.assertAlmostEqual(t.evaluar(t.fin, orden),
                                           s.tramos[i + 1].evaluar(t.fin, orden), places=9)

    def test_se_detectan_resultados_alterados(self):
        from dataclasses import replace
        s = calcular_spline([(0, 0), (1, 1), (2, 16), (3, 81)])
        tramos = (replace(s.tramos[0], a=1.2),) + s.tramos[1:]
        checks = comprobar(s.x, s.y, tramos, s.matriz, s.vector, s.segundas)
        self.assertFalse(all(c.cumple for c in checks))

    def test_se_rechazan_datos_invalidos(self):
        casos = [[], [(0, 1)], [(0, 0), (0, 1)], [(1, 1), (0, 0)],
                 [(0, 0), (1, float("nan"))], [(0, 0), (float("inf"), 1)],
                 [(0, "abc"), (1, 1)], [(0, 1, 2), (1, 2)],
                 [(-1e308, 0), (1e308, 1)]]
        for puntos in casos:
            with self.subTest(puntos=puntos), self.assertRaises(ErrorSpline):
                calcular_spline(puntos)

    def test_no_se_extrapola_y_se_admite_el_extremo_final(self):
        s = calcular_spline([(0, 0), (1, 1), (2, 0)])
        self.assertEqual(s.evaluar(2), 0)
        for x in (-.1, 2.1, float("nan"), "texto"):
            with self.subTest(x=x), self.assertRaises(ErrorSpline):
                s.evaluar(x)

    def test_muestras_sin_duplicar_nodos_compartidos(self):
        s = calcular_spline([(0, 0), (1, 1), (2, 16)])
        puntos = s.muestrear(10)
        self.assertEqual(len(puntos), 19)
        self.assertEqual(puntos[0], (0, 0))
        self.assertAlmostEqual(puntos[-1][1], 16)
        self.assertEqual(sum(x == 1 for x, _ in puntos), 1)

    def test_limite_de_interfaz_80_puntos(self):
        s = calcular_spline([(i / 10, (i % 7) / 3) for i in range(80)])
        self.assertEqual(len(s.tramos), 79)
        self.assertTrue(s.valido)


class EntradaYPresentacionTests(unittest.TestCase):
    def test_coma_decimal_cabecera_y_columnas(self):
        self.assertEqual(leer_puntos("x;y\n-1,5; 2,5\n\n0; 3"), ((-1.5, 2.5), (0, 3)))
        self.assertEqual(leer_puntos("0\t1\n2 3"), ((0, 1), (2, 3)))

    def test_errores_de_texto_indican_linea(self):
        for texto in ("0;0\n1;abc", "0;0\n1;nan", "0;0\n1;2;3"):
            with self.assertRaisesRegex(ErrorSpline, "Línea 2"):
                leer_puntos(texto)

    def test_polinomio_con_nodo_negativo_y_signos(self):
        s = calcular_spline([(-2, 3), (0, -1)])
        texto = polinomio(s.tramos[0], 0)
        self.assertIn("(x + 2)", texto)
        self.assertNotIn("+ −", texto)

    def test_informe_incluye_datos_y_verificacion(self):
        s = calcular_spline([(0, 0), (1, 1), (2, 0)])
        texto = informe(s)
        for parte in ("VERIFICADO", "A·M = B", "GAUSS", "COEFICIENTES", "DETALLE DE COMPROBACIONES"):
            self.assertIn(parte, texto)

    def test_importar_entrada_no_inicia_programa(self):
        modulo = importlib.import_module("spline_cubico")
        self.assertTrue(callable(modulo.main))

    def test_consola_valida_entrada_y_resuelve(self):
        raiz = Path(__file__).resolve().parents[1]
        resultado = subprocess.run([sys.executable, str(raiz / "spline_cubico.py"), "--consola"],
                                   input="1\n2\n0\n0\n1\n1\n", capture_output=True,
                                   encoding="utf-8", timeout=15)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("mayor o igual a 2", resultado.stdout)
        self.assertIn("VERIFICADO", resultado.stdout)

    def test_calculo_solo_usa_biblioteca_estandar(self):
        carpeta = Path(__file__).resolve().parents[1] / "splines"
        prohibidos = {"numpy", "scipy", "sympy", "pandas"}
        for ruta in carpeta.rglob("*.py"):
            for nodo in ast.walk(ast.parse(ruta.read_text(encoding="utf-8"))):
                if isinstance(nodo, ast.Import):
                    nombres = [a.name.split(".")[0] for a in nodo.names]
                elif isinstance(nodo, ast.ImportFrom):
                    nombres = [(nodo.module or "").split(".")[0]]
                else:
                    continue
                self.assertTrue(prohibidos.isdisjoint(nombres), str(ruta))


if __name__ == "__main__":
    unittest.main()
