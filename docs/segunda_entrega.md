# Segunda entrega · Guía de demostración e informe

Este documento relaciona el avance con la rúbrica proporcionada. Los porcentajes no se estiman contando líneas de código: la demostración debe evidenciar las funciones y explicar los resultados.

## Correspondencia con la rúbrica

| Criterio | Material disponible | Acción para la entrega del equipo |
|---|---|---|
| Levantar observaciones de la primera revisión | Correcciones técnicas documentadas en README y método | Incorporar las observaciones reales del docente y describir cómo se atendió cada una. Aún no fueron proporcionadas. |
| Informe ordenado y buena redacción | Guía, fundamento matemático y resultados exportables | Integrar portada, autores, objetivos originales y el formato solicitado por el docente. |
| Figuras y ecuaciones claras | Diagrama SVG y figuras de ejecuciones; fórmulas escritas en LaTeX | Insertar las ecuaciones como ecuaciones editables, no como capturas. Numerar las figuras. |
| Diagrama detallado | `diagrama_flujo.svg` y versión Mermaid en `diagrama_flujo.md` | Explicar las decisiones de validación y el ciclo de exploración. |
| Aplicación conectada con el tema | Ejemplo de contorno superior del pato, 21 nodos | Desarrollar la aplicación propuesta abajo y sus límites. |
| Evidencias de ejecución y descripción | Informes TXT, figuras SVG y pruebas; guion de capturas abajo | Añadir capturas auténticas de las pantallas y sus descripciones al informe. |
| Conclusiones y recomendaciones | Propuesta de redacción abajo | Ajustar a los objetivos originales del equipo. |
| Interfaz explicada y ejecución del avance | Interfaz completa y modo consola; iniciadores `.cmd` y `.pyw` | Ejecutar en el equipo de exposición. Requiere Python con Tcl/Tk; no incluye un `.exe` autónomo. |
| Validación en cada ejecución | Pestaña Validación e informe de comprobaciones | Mostrar al menos una ejecución correcta y un error de entrada controlado. |

## Funciones implementadas para demostrar

Ingreso manual e importación CSV; validación de datos; sistema natural; Gauss manual; coeficientes por intervalo; gráfica; consulta dentro del dominio; cuatro ejemplos; desarrollo matemático visible; validación automática; informe TXT y gráfica SVG.

La interfaz utiliza fondo claro, violeta para la curva y acciones principales, verde azulado para los nodos, verde para comprobaciones satisfactorias y rojo para errores. Los estados también se describen con texto para que el significado no dependa solo del color. La entrada y los resultados están separados y la navegación permite revisar cada etapa.

## Aplicación: reconstrucción del contorno superior de un pato

**Problema:** representar de forma suave un contorno del que solo conocemos coordenadas discretas.

**Datos:** 21 puntos del material del curso; se encuentran en `ejemplos/contorno_pato.csv` y en el selector de ejemplos. Las abscisas recorren de 0,9 a 13,3.

**Conexión con Álgebra Lineal:** se construye un sistema de 21 ecuaciones para las segundas derivadas nodales y se resuelve con operaciones elementales de Gauss. A partir de su solución se construyen 20 polinomios de grado como máximo tres. Las condiciones de continuidad unen los intervalos sin saltos en valor, pendiente ni segunda derivada.

**Resultado que se debe mostrar:** la gráfica pasa por los nodos y permite consultar alturas intermedias. La pestaña Validación comprueba las condiciones en esa misma ejecución.

**Límite de la aplicación:** estos datos describen el contorno superior, no toda la silueta cerrada ni el ala. Una silueta con varias alturas para la misma abscisa requiere varios contornos o una representación paramétrica. El ejemplo no permite inferir áreas o dimensiones físicas sin definir previamente las unidades y el resto de la geometría.

## Guion de exposición y capturas auténticas

Crear una carpeta de imágenes y guardar capturas de la aplicación en ejecución. Las figuras SVG generadas son gráficas matemáticas; no son pantallazos de la interfaz.

| Figura sugerida | Acción | Descripción para acompañarla |
|---|---|---|
| 1. Interfaz y curva | Abrir el ejemplo x⁴ en Gráfica | Se ingresan cuatro nodos y se construyen tres tramos con frontera natural. La curva pasa por los puntos dados. |
| 2. Polinomios | Abrir Polinomios y seleccionar S1 | La tabla presenta los coeficientes a, b, c y d; el panel inferior muestra la expresión en la base desplazada del curso. |
| 3. Sistema matricial | Abrir Procedimiento y desplazar a la sección 02 | Se observan A, B y la relación Mᵢ=S''(xᵢ). Las filas extremas imponen la frontera natural. |
| 4. Resolución | Mostrar la sección 03 de Procedimiento | El registro explica intercambios y operaciones de eliminación, seguido por el sistema triangular y la sustitución regresiva. |
| 5. Validación | Abrir Validación | Para el ejemplo x⁴ se comprueban 18 condiciones con tolerancias explícitas. El estado se obtiene de los coeficientes sin redondear. |
| 6. Valor intermedio | En Gráfica, evaluar x=1,5 | Se obtiene S(1,5)=3,7 y se indican el tramo y sus derivadas. Es una interpolación de los nodos, no una reproducción exacta de x⁴ en todo el intervalo. |
| 7. Aplicación | Seleccionar Contorno del pato | Se construyen 20 tramos sobre los 21 puntos del contorno superior. Mostrar también su validación. |
| 8. Entrada incorrecta | Repetir una abscisa y calcular | Se informa el error y no se presenta un nuevo resultado como válido. Corregir y recalcular para mostrar la recuperación. |

La herramienta de captura automática no consiguió capturar la ventana durante esta sesión (`window capture timed out`). No se incluyen capturas ficticias. Las pruebas de integración verifican controles y navegación, pero no sustituyen la inspección visual del equipo ni los pantallazos del informe.

## Conclusiones propuestas

1. La interpolación cúbica natural permite construir una función por tramos que interpola los nodos y mantiene continuidad en la función y sus dos primeras derivadas. El programa comprueba esas condiciones en cada ejecución.
2. El problema de interpolación se convierte en un sistema lineal para las segundas derivadas nodales. La implementación de Gauss permite relacionar la solución computacional con las operaciones elementales estudiadas en Álgebra Lineal.
3. La aplicación al contorno superior del pato muestra cómo un conjunto de coordenadas puede transformarse en una curva suave y evaluable en puntos intermedios. Su utilidad está limitada por la calidad de los datos y por la representación elegida.

Estas conclusiones describen funciones comprobables del avance. El equipo debe relacionarlas con sus objetivos reales antes de entregarlas.

## Recomendaciones propuestas

- Validar abscisas crecientes y datos finitos antes de construir el sistema.
- Conservar la precisión completa en los cálculos y redondear únicamente la presentación.
- Elegir las condiciones de frontera de acuerdo con el problema; la frontera natural no es obligatoriamente la mejor para toda aplicación.
- Para conjuntos mucho mayores, implementar un solucionador tridiagonal y comparar su complejidad con Gauss.
- Probar el inicio y la legibilidad de la interfaz en el equipo de exposición y adjuntar capturas reales con sus explicaciones.

## Pendientes externos al código

1. Observaciones exactas del docente en la primera revisión.
2. Objetivos y recomendaciones del informe anterior del equipo.
3. Capturas auténticas de las pantallas en el equipo de exposición y revisión visual final.
4. Confirmar si el docente exige específicamente un binario `.exe` o admite ejecutar el proyecto con Python.

No se afirma una nota ni un porcentaje de aprobación: corresponde al docente evaluar la demostración y el informe final.
