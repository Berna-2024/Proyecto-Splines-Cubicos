"""Ejecuta las pruebas y conserva su salida real como evidencia."""

import io
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))


def main():
    salida = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(RAIZ / "tests"), top_level_dir=str(RAIZ))
    resultado = unittest.TextTestRunner(stream=salida, verbosity=2).run(suite)
    carpeta = RAIZ / "docs" / "evidencias"
    carpeta.mkdir(parents=True, exist_ok=True)
    texto = salida.getvalue()
    (carpeta / "pruebas.txt").write_text(texto, encoding="utf-8")
    print(texto)
    return 0 if resultado.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
