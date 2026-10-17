"""Integración de controles, navegación y errores de la interfaz Tkinter."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from splines.ejemplos import EJEMPLOS
from splines.ui.app import AplicacionSpline


class InterfazTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = AplicacionSpline(cargar_inicial=False)
        cls.errores = []
        cls.app.report_callback_exception = lambda *error: cls.errores.append(error)

    @classmethod
    def tearDownClass(cls):
        cls.app.destroy()

    def setUp(self):
        self.app.ejemplo.current(0)
        self.app.cargar_ejemplo()
        self.app.update()

    def tearDown(self):
        self.assertEqual(self.errores, [], "No debe haber errores en callbacks de Tkinter.")

    def test_todos_los_ejemplos_y_pestanas(self):
        for nombre in EJEMPLOS:
            self.app.ejemplo.set(nombre)
            self.app.cargar_ejemplo()
            self.app.update()
            self.assertTrue(self.app.spline.valido)
            self.assertEqual(len(self.app.tabla_coef.get_children()), len(self.app.spline.tramos))
            self.assertEqual(len(self.app.tabla_validacion.get_children()), len(self.app.spline.comprobaciones))
            for indice in range(4):
                self.app.pestanas.select(indice)
                self.app.update()
                self.assertEqual(self.app.pestanas.index("current"), indice)
        self.app.pestanas.select(0)

    def test_evaluacion_y_fuera_de_dominio(self):
        self.app._seleccionar_x(1.5)
        self.assertIn("3.7", self.app.resultado_consulta.cget("text"))
        self.assertEqual(self.app.grafica.seleccion, 1.5)
        self.app.consulta_x.delete(0, "end")
        self.app.consulta_x.insert(0, "4")
        self.app.evaluar()
        self.assertIn("entre 0 y 3", self.app.resultado_consulta.cget("text"))
        self.assertIsNone(self.app.grafica.seleccion)

    def test_editar_invalida_resultado_anterior(self):
        self.app.entrada.insert("end", "\n4;256")
        self.app.update()
        self.assertIsNone(self.app.spline)
        self.assertEqual(str(self.app.exportar_boton.cget("state")), "disabled")
        self.assertEqual(self.app.tabla_coef.get_children(), ())

    def test_error_y_recuperacion(self):
        self.app._reemplazar_datos("0;0\n0;1")
        self.app.calcular()
        self.assertIsNone(self.app.spline)
        self.assertIn("sin repetir", self.app.mensaje.cget("text"))
        self.app.cargar_ejemplo()
        self.assertTrue(self.app.spline.valido)
        self.assertEqual(self.app.mensaje.cget("text"), "")

    def test_limite_de_puntos(self):
        self.app._reemplazar_datos("\n".join(f"{i};{i}" for i in range(81)))
        self.app.calcular()
        self.assertIsNone(self.app.spline)
        self.assertIn("80", self.app.mensaje.cget("text"))

    def test_importar_y_exportar_archivos(self):
        base = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory(dir=base, prefix="prueba_") as carpeta:
            self.assertTrue(Path(carpeta).resolve().is_relative_to(base))
            entrada = Path(carpeta) / "puntos.csv"
            salida = Path(carpeta) / "informe.txt"
            entrada.write_text("x;y\n0;0\n1;1\n2;0", encoding="utf-8")
            with patch("splines.ui.app.filedialog.askopenfilename", return_value=str(entrada)):
                self.app.importar()
            self.assertEqual(len(self.app.spline.x), 3)
            with patch("splines.ui.app.filedialog.asksaveasfilename", return_value=str(salida)):
                self.app.exportar()
            self.assertIn("VERIFICADO", salida.read_text(encoding="utf-8"))
            figura = Path(carpeta) / "grafica.svg"
            with patch("splines.ui.app.filedialog.asksaveasfilename", return_value=str(figura)):
                self.app.guardar_grafica()
            import xml.etree.ElementTree as xml
            raiz = xml.fromstring(figura.read_text(encoding="utf-8"))
            self.assertEqual(len(raiz.findall(".//{http://www.w3.org/2000/svg}circle")), 3)

    def test_controles_visibles_en_tamano_minimo(self):
        self.app.pestanas.select(0)
        self.app.geometry("1100x710")
        self.app.update()
        for widget in (self.app.entrada, self.app.grafica, self.app.consulta_x, self.app.estado):
            with self.subTest(widget=widget):
                x = widget.winfo_rootx() - self.app.winfo_rootx()
                y = widget.winfo_rooty() - self.app.winfo_rooty()
                self.assertTrue(widget.winfo_ismapped())
                self.assertGreaterEqual(x, 0)
                self.assertGreaterEqual(y, 0)
                self.assertLessEqual(x + widget.winfo_width(), self.app.winfo_width())
                self.assertLessEqual(y + widget.winfo_height(), self.app.winfo_height())
        self.app.geometry("1380x900")


if __name__ == "__main__":
    unittest.main()
