"""Datos del curso y ejemplo de reproducción de una recta."""

EJEMPLOS = {
    "Ejemplo del curso · x⁴": (
        "0; 0\n1; 1\n2; 16\n3; 81",
        "Ejemplo del curso: f(x) = x⁴ en los nodos 0, 1, 2 y 3.",
    ),
    "Contorno del pato": (
        "0,9; 1,3\n1,3; 1,5\n1,9; 1,85\n2,1; 2,1\n2,6; 2,6\n3; 2,7\n"
        "3,9; 2,4\n4,4; 2,15\n4,7; 2,05\n5; 2,1\n6; 2,25\n7; 2,3\n8; 2,25\n"
        "9,2; 1,95\n10,5; 1,4\n11,3; 0,9\n11,6; 0,7\n12; 0,6\n12,6; 0,5\n13; 0,4\n13,3; 0,25",
        "Aplicación: reconstrucción del contorno superior del pato con 21 puntos del material.",
    ),
    "Función · 1 / (1 + x²)": (
        "\n".join(f"{k / 5:.1f}; {1 / (1 + (k / 5) ** 2):.16g}" for k in range(6)),
        "Ejercicio del curso: seis nodos de f(x) = 1 / (1 + x²) entre 0 y 1.",
    ),
    "Datos lineales": (
        "-2; -3\n-0,5; 0\n1; 3\n4,5; 10\n8; 17",
        "Comprobación: el spline de puntos de y = 2x + 1 debe reproducir esa recta.",
    ),
}
