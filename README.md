# SplineLab · Splines cúbicos naturales

Proyecto de Álgebra Lineal para construir curvas por tramos y mostrar cómo se obtiene cada resultado. El cálculo utiliza exclusivamente listas, ciclos y aritmética de Python. No necesita NumPy, SciPy, SymPy, Matplotlib ni paquetes instalados con pip.

## Ejecutar

Requisito: Python 3.10 o posterior, con Tcl/Tk. En Windows, la instalación de Python debe incluir el componente Tcl/Tk e IDLE.

Desde la carpeta del proyecto:

```console
python spline_cubico.py
```

También puedes abrir `iniciar.cmd` en Windows. `iniciar.pyw` permite abrir la aplicación sin consola si la extensión está asociada a Python. No se incluye un binario `.exe`; el programa se ejecuta con Python.

Para conservar el ingreso por consola del primer avance:

```console
python spline_cubico.py --consola
```

## Utilizar la interfaz

1. Selecciona un ejemplo o escribe un punto por línea en el formato `x ; y`.
2. Mantén las abscisas en orden estrictamente creciente. Se admiten de 2 a 80 puntos en la interfaz.
3. Pulsa **Calcular spline** o **Ctrl + Enter**.
4. Revisa las pestañas **Gráfica**, **Polinomios**, **Procedimiento** y **Validación**.
5. Escribe una abscisa dentro del dominio y pulsa **Evaluar**. También puedes hacer clic en la curva.
6. Usa **Exportar informe** para guardar datos, sistema, operaciones de Gauss, coeficientes y comprobaciones en texto. **Guardar gráfica** crea un SVG que se puede insertar en el informe sin perder nitidez.

Se admiten punto o coma decimal. Los puntos también pueden separarse en dos columnas con espacios o tabuladores. Los archivos CSV deben usar punto y coma como separador, con cabecera opcional `x;y` y codificación UTF-8. Hay ejemplos en `ejemplos/`.

```text
x;y
0;0
1;1
2;16
3;81
```

Modificar los datos invalida los resultados anteriores y desactiva la exportación hasta recalcular. El programa rechaza valores no finitos, puntos repetidos, desordenados y consultas fuera del dominio. Una importación incorrecta conserva los datos anteriores.

## Estructura

```text
spline_cubico.py          Entrada principal: interfaz o consola
iniciar.pyw              Inicio gráfico sin consola
iniciar.cmd              Inicio con doble clic en Windows
splines/
  algebra.py             Gauss y sustitución regresiva
  matematica.py          Tramos, sistema natural, evaluación y comprobaciones
  entrada.py             Lectura de datos y mensajes de validación
  ejemplos.py            Datos de los PDF del curso
  presentacion.py        Polinomios, procedimiento e informe
  exportacion.py         Gráfica SVG con los resultados calculados
  consola.py             Interacción por consola
  ui/
    app.py               Pantallas y coordinación de acciones
    grafica.py           Dibujo e interacción con Canvas
    tema.py              Colores y estilos
tests/                   Pruebas matemáticas y de interfaz
ejemplos/                Archivos CSV listos para cargar
docs/                    Matemática, diagrama y guía de segunda entrega
tools/                   Generación reproducible de evidencias
```

## Método implementado

Con N puntos se construyen N−1 polinomios. Las incógnitas M son las segundas derivadas del spline en los nodos. Se construye el sistema completo A·M=B, con M inicial = M final = 0, y se resuelve mediante eliminación de Gauss con pivoteo parcial escalado. Finalmente se calculan los coeficientes de cada tramo con las fórmulas del material del curso.

El uso de pivoteo escalado sigue siendo eliminación de Gauss; solo mejora la elección de la fila pivote. La gráfica se obtiene evaluando nuestros polinomios. Canvas dibuja las coordenadas y no calcula el spline.

Se comprueban en cada ejecución interpolación, continuidad de la función y de sus dos primeras derivadas, fronteras naturales y residuo del sistema. Se usa `error <= 1e-8 * escala`, con escala al menos 1. Solo el texto se redondea. Un resultado fuera de tolerancia aparece como **Revisar**, nunca como verificado.

Consulta [el desarrollo matemático](docs/metodo_matematico.md) y [la guía de segunda entrega](docs/segunda_entrega.md).

## Pruebas y evidencias

```console
python -m unittest discover -s tests -v
python tools/generar_evidencias.py
```

La primera orden comprueba resultados conocidos, propiedades, errores de entrada e interacción con los controles de Tkinter. Requiere una sesión gráfica disponible. La segunda genera informes de ejecuciones y figuras reales a partir del modelo matemático. Las capturas de pantalla de la aplicación deben obtenerse de su ejecución real; no se sustituyen por las figuras SVG.

## Alcance y límites

- Se implementa la frontera **natural**. La frontera sujeta no forma parte de esta versión.
- La interfaz limita la entrada a 80 puntos para mantener legible el procedimiento; el núcleo matemático no fija ese límite.
- La eliminación de Gauss usa tiempo O(N³) y memoria O(N²). Se conserva el sistema completo del avance por su relación con Álgebra Lineal. Para conjuntos grandes se podría implementar el algoritmo tridiagonal de Thomas.
- La vista detallada limita el registro a 250 operaciones de resolución y avisa si hay más. El sistema completo y los resultados siguen disponibles.
- Se trabaja con números de punto flotante. Magnitudes extremas o datos mal condicionados pueden ser rechazados o requerir revisar precisión.
- Interpolar no implica suavizar ruido ni conservar monotonía: una curva puede sobrepasar los valores entre nodos.
- El porcentaje y la calificación de la entrega dependen de la revisión del docente. El informe final debe integrar sus observaciones y los objetivos del equipo.
