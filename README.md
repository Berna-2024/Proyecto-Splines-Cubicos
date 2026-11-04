# SplineLab · Splines cúbicos naturales y comparación con Lagrange

Proyecto de Álgebra Lineal correspondiente a la tercera y última entrega (semana 11). Implementa splines cúbicos naturales mediante métodos matriciales y permite compararlos gráficamente con el polinomio interpolador de Lagrange construido con los mismos nodos. Muestra el procedimiento del spline y permite evaluar ambas interpolaciones. El cálculo utiliza exclusivamente listas, ciclos y aritmética de Python. No necesita NumPy, SciPy, SymPy, Matplotlib ni paquetes instalados con pip.

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
3. Pulsa **Calcular spline** o **Ctrl + Enter**. Lagrange se construye automáticamente con los mismos datos cuando las condiciones numéricas lo permiten.
4. En **Gráfica**, observa el spline con línea continua, Lagrange con línea naranja discontinua y los nodos originales sobre los mismos ejes y escala. La casilla **Lagrange** permite mostrar u ocultar su curva; el spline permanece visible. Ambas curvas se dibujan dentro del dominio de los nodos.
5. Escribe una abscisa dentro del dominio y pulsa **Evaluar**. También puedes hacer clic en la gráfica. Se muestran S(x), el tramo y las derivadas del spline; cuando Lagrange está disponible, también P(x) y la diferencia absoluta |S(x) − P(x)|. Esta diferencia compara dos interpolaciones y no representa un error respecto de una función original desconocida. Ocultar la curva de Lagrange no desactiva su evaluación.
6. Revisa **Polinomios**, **Procedimiento** y **Validación** para consultar los tramos, el desarrollo matricial y las comprobaciones del spline. La pestaña **Gráfica** también indica la verificación de Lagrange en los nodos cuando está disponible.
7. Usa **Exportar informe** para guardar datos, sistema, operaciones de Gauss, coeficientes y comprobaciones del spline en texto. **Guardar gráfica** crea un SVG con nodos, leyenda y la comparación si Lagrange está disponible y su casilla está activada. Si el muestreo de exportación detecta un problema numérico, el SVG conserva el spline e indica que Lagrange fue omitido. El SVG se puede insertar en el informe sin perder nitidez.

Se admiten punto o coma decimal. Los puntos también pueden separarse en dos columnas con espacios o tabuladores. Los archivos CSV deben usar punto y coma como separador, con cabecera opcional `x;y` y codificación UTF-8. Hay ejemplos en `ejemplos/`.

```text
x;y
0;0
1;1
2;16
3;81
```

Modificar los datos o limpiar el formulario invalida los resultados anteriores de ambos métodos y desactiva la exportación hasta recalcular. Una importación válida recalcula con los nuevos puntos. El programa rechaza valores no finitos, abscisas repetidas o desordenadas y consultas fuera del dominio. Una importación incorrecta conserva el texto de entrada anterior, pero invalida los resultados calculados.

## Estructura

```text
spline_cubico.py          Entrada principal: interfaz o consola
iniciar.pyw              Inicio gráfico sin consola
iniciar.cmd              Inicio con doble clic en Windows
splines/
  algebra.py             Gauss y sustitución regresiva
  matematica.py          Tramos, sistema natural, evaluación y comprobaciones
  lagrange.py            Interpolador baricéntrico, evaluación y control numérico
  entrada.py             Lectura de datos y mensajes de validación
  ejemplos.py            Datos de los PDF del curso
  presentacion.py        Polinomios, procedimiento e informe
  exportacion.py         Gráfica SVG con los resultados calculados
  consola.py             Interacción por consola
  ui/
    app.py               Pantallas y coordinación de acciones
    grafica.py           Dibujo e interacción con Canvas
    tema.py              Colores y estilos
tests/
  test_matematica.py     Pruebas de Gauss, spline, entrada y consola
  test_lagrange.py       Lagrange, comparación, SVG y controlador sin ventana
  test_interfaz.py       Controles Tkinter, visibilidad, errores y exportación
ejemplos/                Archivos CSV listos para cargar
docs/                    Desarrollo matemático, diagrama y documentación histórica
tools/                   Generación reproducible de evidencias
```

## Método implementado

Con N puntos se construyen N−1 polinomios. Las incógnitas M son las segundas derivadas del spline en los nodos. Se construye el sistema completo A·M=B, con M inicial = M final = 0, y se resuelve mediante eliminación de Gauss con pivoteo parcial escalado. Finalmente se calculan los coeficientes de cada tramo con las fórmulas del material del curso.

El uso de pivoteo escalado sigue siendo eliminación de Gauss; solo mejora la elección de la fila pivote. La gráfica se obtiene evaluando nuestros polinomios. Canvas dibuja las coordenadas y no calcula el spline.

Se comprueban en cada ejecución interpolación, continuidad de la función y de sus dos primeras derivadas, fronteras naturales y residuo del sistema. Se usa `error <= 1e-8 * escala`, con escala al menos 1. Solo el texto se redondea. Un resultado fuera de tolerancia aparece como **Revisar**, nunca como verificado.

### Comparación con Lagrange (entrega final)

El interpolador global utiliza exactamente los mismos nodos que el spline y reutiliza su validación de puntos. Se basa en P(x) = Σᵢ yᵢLᵢ(x), donde Lᵢ(x) = ∏ⱼ≠ᵢ (x − xⱼ)/(xᵢ − xⱼ). Se evalúa mediante la forma baricéntrica equivalente, con pesos normalizados mediante logaritmos, sin expandir el polinomio ni redondear los cálculos. Las coincidencias exactas con nodos devuelven sus ordenadas y se comprueba P(xᵢ) ≈ yᵢ con tolerancia `1e-8 * max(1, abs(y_i))`.

Canvas representa las muestras de ambos modelos sobre los mismos ejes; no realiza la interpolación. La incorporación de Lagrange conserva el sistema matricial, la eliminación de Gauss y las condiciones naturales del spline.

Consulta [el desarrollo matemático del spline](docs/metodo_matematico.md). La [guía de segunda entrega](docs/segunda_entrega.md) y las [evidencias conservadas](docs/evidencias/README.md) corresponden a una etapa anterior; se mantienen como antecedentes y no constituyen la documentación final de la semana 11. Este README describe el alcance de la tercera entrega.

## Pruebas y evidencias

```console
python -m unittest discover -v
```

Este comando ejecuta la suite completa, incluidas las pruebas de interfaz, que requieren Tcl/Tk funcional y una sesión gráfica disponible. Si el entorno no puede abrir ventanas, ejecuta las pruebas matemáticas, de SVG y del controlador con controles simulados:

```console
python -m unittest tests.test_matematica tests.test_lagrange -v
```

Las pruebas incluyen los cuatro nodos (0, 0), (1, 1), (2, 0), (3, 1), datos lineales, nodos de x⁴, valores intermedios, entradas inválidas y protección ante inestabilidad de Lagrange. Las pruebas con controles simulados no sustituyen la comprobación visual de Tkinter. Un error de inicio relacionado con `init.tcl` indica que debe revisarse la instalación o configuración de Tcl/Tk.

Se conservan las herramientas de evidencias:

```console
python tools/verificar_entrega.py
python tools/generar_evidencias.py
```

La primera ejecuta la suite completa y guarda su salida en `docs/evidencias/pruebas.txt`; también requiere el entorno gráfico para las pruebas de interfaz. La segunda genera informes y figuras del spline a partir del modelo matemático, sin incorporar automáticamente Lagrange. Estas herramientas actualizan archivos de evidencias; los archivos históricos no acreditan por sí solos la validación de la entrega final. Las capturas de pantalla deben obtenerse de la ejecución real de la aplicación y no se sustituyen por figuras SVG.

## Alcance y límites

- Se implementa la frontera **natural**. La frontera sujeta no forma parte de esta versión.
- La interfaz limita la entrada a 80 puntos para mantener legible el procedimiento; el núcleo matemático no fija ese límite.
- La eliminación de Gauss usa tiempo O(N³) y memoria O(N²). Se conserva el sistema completo del avance por su relación con Álgebra Lineal. Para conjuntos grandes se podría implementar el algoritmo tridiagonal de Thomas.
- La vista detallada limita el registro a 250 operaciones de resolución y avisa si hay más. El sistema completo y los resultados siguen disponibles.
- Se trabaja con números de punto flotante. Magnitudes extremas o datos mal condicionados pueden ser rechazados o requerir revisar precisión.
- Interpolar no implica suavizar ruido ni conservar monotonía: una curva puede sobrepasar los valores entre nodos.
- Lagrange global puede oscilar y perder precisión con muchos nodos o distribuciones desfavorables. La interfaz advierte cuando hay más de 20 nodos y desactiva únicamente la comparación si detecta cancelación excesiva, valores no finitos o magnitudes que no permiten una representación segura. El spline sigue disponible con su límite de 80 puntos.
- La comprobación de nodos y el muestreo de Lagrange no garantizan precisión uniforme entre muestras. La normalización baricéntrica mejora la evaluación, pero no elimina el mal condicionamiento del problema.
- El porcentaje y la calificación de la entrega dependen de la revisión del docente. El informe final debe integrar sus observaciones y los objetivos del equipo.
