"""Punto de entrada. Ejecutar sin argumentos abre la interfaz gráfica."""

import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(description="SplineLab: interpolación cúbica natural sin NumPy.")
    parser.add_argument("--consola", action="store_true", help="Usar la entrada interactiva de consola.")
    opciones = parser.parse_args(argv)
    if opciones.consola:
        from splines.consola import iniciar
        return iniciar()
    from splines.ui.app import iniciar
    iniciar()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
