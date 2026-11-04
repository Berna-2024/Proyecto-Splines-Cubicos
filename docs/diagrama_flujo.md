# Diagrama del programa · Tercera entrega (semana 11)

La versión vectorial está en [diagrama_flujo.svg](diagrama_flujo.svg). Este código Mermaid permite mantener el diagrama editable.

```mermaid
flowchart TD
    inicio([Inicio]) --> interfaz[Mostrar interfaz y ejemplo inicial]
    interfaz --> datos[Ingresar puntos, cargar ejemplo o importar CSV]
    datos --> validar{¿Dos a ochenta puntos finitos y x creciente?}
    validar -- No --> error[Invalidar ambos resultados, mostrar mensaje y corregir datos]
    error --> datos
    distancias -. Error numérico .-> error
    coeficientes -. Error numérico .-> error
    validar -- Sí --> distancias[Calcular h y pendientes entre nodos]
    distancias --> sistema[Construir A y B con frontera natural]
    sistema --> gauss[Gauss con pivoteo parcial escalado]
    gauss --> resoluble{¿Sistema resoluble?}
    resoluble -- No --> error
    resoluble -- Sí --> sustitucion[Sustitución regresiva: obtener M]
    sustitucion --> coeficientes[Calcular a, b, c y d de cada tramo]
    coeficientes --> comprobaciones[Comprobar interpolación, continuidad, fronteras y residuo]
    comprobaciones --> muestras[Preparar muestras del spline]
    muestras -. Error numérico .-> error
    muestras --> precision{¿Cumple la tolerancia?}
    precision -- Sí --> verificado[Mostrar estado Verificado]
    precision -- No --> revisar[Mostrar estado Revisar]
    verificado --> lagrange[Construir Lagrange baricéntrico con los mismos nodos]
    revisar --> lagrange
    lagrange --> validarl[Comprobar nodos y muestrear: finitud, cancelación y magnitudes]
    lagrange -. Error numérico .-> desactivar[Advertir y desactivar solo Lagrange; conservar spline]
    validarl --> fiable{¿Comprobaciones y muestreo aceptables?}
    fiable -- No --> desactivar
    fiable -- Sí --> disponible[Lagrange disponible; advertir con más de 20 nodos]
    disponible --> resultados[Mostrar curvas y nodos en mismos ejes y dominio; polinomios, procedimiento y validación del spline]
    desactivar --> resultados
    resultados --> accion{¿Qué desea hacer?}
    accion -- Mostrar u ocultar --> alternar[Redibujar según casilla si Lagrange disponible; spline visible]
    alternar --> accion
    accion -- Evaluar o clic --> dominio{¿x finito dentro del dominio?}
    dominio -- Sí --> evaluar[Evaluar S y mostrar tramo y derivadas]
    dominio -- No --> avisar[Indicar el dominio permitido]
    evaluar --> tienel{¿Lagrange disponible?}
    tienel -- No --> accion
    tienel -- Sí --> evaluarpl[Evaluar P y diferencia absoluta entre S y P]
    evaluarpl --> seguro{¿Evaluación numéricamente aceptable?}
    seguro -- Sí --> comparar[Mostrar S, P y diferencia absoluta]
    comparar --> accion
    seguro -- No --> fallopl[Advertir, retirar Lagrange y desactivar comparación; conservar S]
    fallopl --> accion
    avisar --> accion
    accion -- Exportar --> formato{Formato solicitado}
    formato -- TXT --> txt[Guardar informe del spline]
    formato -- SVG --> svg[Preparar nodos, spline y leyenda; Lagrange si disponible y visible]
    svg --> exportable{¿Muestreo aceptable o Lagrange no solicitado?}
    exportable -- Sí --> guardar[Guardar SVG]
    exportable -- No --> omitir[Guardar SVG del spline con aviso: Lagrange omitido]
    txt --> accion
    guardar --> accion
    omitir --> accion
    accion -- Editar, limpiar, ejemplo o CSV --> invalidar[Invalidar resultados de ambos métodos al cambiar datos]
    invalidar --> datos
    accion -- Cerrar --> fin([Fin])
```

En el SVG, los círculos con la misma letra indican continuidad entre bloques:
**A** continúa con Lagrange; **R** vuelve a las acciones; **E** evalúa;
**X** exporta; **D** cambia datos; **I** vuelve a la entrada.

Los errores de entrada, resolución o magnitudes del spline invalidan los
resultados. Un estado **Revisar precisión** no impide intentar Lagrange.
Su comprobación en nodos y el muestreo no garantizan precisión uniforme.
Ocultar Lagrange no impide evaluarlo. La diferencia entre interpolaciones
no es un error respecto de una función original desconocida.

Los ejemplos y una importación válida recalculan automáticamente. Editar o
limpiar invalida resultados hasta recalcular. Una importación fallida conserva
el texto anterior e invalida los resultados. Cancelar un diálogo conserva el
estado; un error de archivo muestra un mensaje. El cierre está disponible
en cualquier momento.

Para regenerar solo el SVG desde la raíz, sin actualizar otras evidencias:

```console
python -c "from pathlib import Path; from tools.generar_evidencias import diagrama_svg; Path('docs/diagrama_flujo.svg').write_text(diagrama_svg(), encoding='utf-8')"
```
