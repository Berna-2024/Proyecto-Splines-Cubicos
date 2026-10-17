# Evidencias reproducibles

Los archivos TXT son salidas reales del cálculo y contienen las verificaciones. Los SVG son gráficas de los polinomios obtenidos, no capturas de pantalla. `resumen.json` reúne nodos, tramos, cantidad de comprobaciones y errores de los cuatro ejemplos. `pruebas.txt` conserva la salida real de la batería de pruebas.

Regenerar desde la raíz del proyecto:

```console
python tools/generar_evidencias.py
python tools/verificar_entrega.py
```

Para los pantallazos que exige la rúbrica, seguir el guion de `../segunda_entrega.md`. Deben capturarse durante una ejecución auténtica y acompañarse de una explicación. La captura automática de la ventana no estuvo disponible durante esta sesión; no se atribuyen a estas figuras características de pantallazos que no tienen.
