"""Valores independientes y protección numérica de la comparación."""

import unittest
import xml.etree.ElementTree as xml
from types import SimpleNamespace
from unittest.mock import MagicMock

from splines.lagrange import calcular_lagrange
from splines.matematica import ErrorSpline, calcular_spline
from splines.exportacion import grafica_svg
from splines.ui.app import AplicacionSpline


class LagrangeTests(unittest.TestCase):
    def test_cuatro_nodos(self):
        datos = [(0, 0), (1, 1), (2, 0), (3, 1)]
        s, p = calcular_spline(datos), calcular_lagrange(datos)
        self.assertEqual((s.x, s.y), (p.x, p.y))
        for x, y in datos:
            self.assertAlmostEqual(s.evaluar(x), y)
            self.assertEqual(p.evaluar(x), y)
        for x, esperado_s, esperado_p in ((.5, .75, 1), (1.5, .5, .5), (2.5, .25, 0)):
            self.assertAlmostEqual(s.evaluar(x), esperado_s)
            self.assertAlmostEqual(p.evaluar(x), esperado_p)
        for k in range(61):
            x = k / 20
            self.assertAlmostEqual(p.evaluar(x), (2/3)*x**3 - 3*x*x + (10/3)*x)
        self.assertTrue(all(c.cumple for c in p.comprobaciones))

    def test_recta(self):
        datos = [(i, 2*i+1) for i in range(5)]
        for modelo in (calcular_spline(datos), calcular_lagrange(datos)):
            for k in range(81):
                x = k / 20
                self.assertAlmostEqual(modelo.evaluar(x), 2*x+1)

    def test_x4(self):
        datos = [(i, i**4) for i in range(4)]
        s, p = calcular_spline(datos), calcular_lagrange(datos)
        for x, y in datos:
            self.assertAlmostEqual(s.evaluar(x), y)
            self.assertEqual(p.evaluar(x), y)
        # x^4 - x(x-1)(x-2)(x-3) = 6x^3 - 11x^2 + 6x.
        for x in (.5, 1.5, 2.5):
            self.assertAlmostEqual(p.evaluar(x), 6*x**3 - 11*x*x + 6*x)
        self.assertAlmostEqual(s.evaluar(1.5), 3.7)

    def test_invalidos_y_dominio(self):
        for datos in ([(0, 1), (0, 2)], [(0, 1), (1, float('nan'))],
                      [(0, 1), (float('inf'), 1)]):
            with self.assertRaises(ErrorSpline):
                calcular_lagrange(datos)
        p = calcular_lagrange([(0, 0), (1, 1)])
        for x in (-1, 2, float('nan'), 'abc', None):
            with self.assertRaises(ErrorSpline):
                p.evaluar(x)

    def test_cancelacion_con_80_nodos(self):
        datos = [(i, i % 7) for i in range(80)]
        self.assertTrue(calcular_spline(datos).valido)
        with self.assertRaises(ErrorSpline):
            calcular_lagrange(datos).evaluar(.5)

    def test_svg_comparativo(self):
        datos = [(0, 0), (1, 1), (2, 0), (3, 1)]
        s, p = calcular_spline(datos), calcular_lagrange(datos)
        raiz = xml.fromstring(grafica_svg(s, lagrange=p))
        ns = '{http://www.w3.org/2000/svg}'
        curvas = raiz.findall(f'{ns}g/{ns}polyline')
        self.assertEqual(len(curvas), 2)
        self.assertEqual(curvas[1].get('stroke-dasharray'), '7 4')
        self.assertEqual(len(raiz.findall(f'.//{ns}circle')), 4)

    def test_svg_inestable_exporta_spline(self):
        datos = [(i, i % 7) for i in range(80)]
        texto = grafica_svg(calcular_spline(datos), lagrange=calcular_lagrange(datos))
        xml.fromstring(texto)
        self.assertIn('Lagrange omitido', texto)


class ControladorSinVentanaTests(unittest.TestCase):
    """Ejecuta los métodos reales con controles simulados, sin requerir Tcl."""

    def setUp(self):
        self.app = SimpleNamespace(**{nombre: MagicMock() for nombre in (
            'mensaje', 'entrada', 'control_lagrange', 'resultado_consulta',
            'contexto_label', 'grafica', 'tabla_coef', 'tabla_validacion',
            'pasos', 'resumen_validacion', 'exportar_boton', 'evaluar_boton',
            'guardar_grafica_boton', 'consulta_x', 'estado', 'expresion',
            'mostrar_lagrange')})
        self.app.metricas = [MagicMock() for _ in range(3)]
        self.app.contexto = ''
        self.app._texto = MagicMock()
        self.app._ver_polinomio = MagicMock()
        self.app._invalidar = lambda: AplicacionSpline._invalidar(self.app)

    def calcular(self, texto):
        self.app.entrada.get.return_value = texto
        AplicacionSpline.calcular(self.app)

    def test_calculo_y_evaluacion_comparativa(self):
        self.calcular('0;0\n1;1\n2;16\n3;81')
        self.assertEqual(self.app.spline.x, self.app.lagrange.x)
        self.app.consulta_x.get.return_value = '1.5'
        AplicacionSpline.evaluar(self.app)
        texto = self.app.resultado_consulta.configure.call_args.kwargs['text']
        for esperado in ('3.7', 'P(x) = 4.5', '0.8', "S'", "S''"):
            self.assertIn(esperado, texto)

    def test_entrada_invalida_borra_comparacion(self):
        self.calcular('0;0\n1;1')
        self.assertIsNotNone(self.app.lagrange)
        self.calcular('0;0\n0;1')
        self.assertIsNone(self.app.lagrange)
        self.assertIsNone(self.app.spline)
        self.app.grafica.establecer.assert_called_with(None)

    def test_80_nodos_solo_desactiva_comparacion(self):
        self.calcular('\n'.join(f'{i};{i % 7}' for i in range(80)))
        self.assertTrue(self.app.spline.valido)
        self.assertIsNone(self.app.lagrange)
        self.assertIn('desactivada', self.app.mensaje.configure.call_args.kwargs['text'])
