# Desarrollo matemático y relación con el código

## 1. Datos y notación

Sean N puntos (xᵢ,yᵢ), i=0,...,N−1, con x₀<x₁<...<xₙ₋₁. Hay N−1 intervalos. El código utiliza N para la cantidad de puntos; los PDF también utilizan n+1 puntos, por lo que su n equivale a N−1.

Cada tramo tiene la forma

$$S_i(x)=a_i(x-x_i)^3+b_i(x-x_i)^2+c_i(x-x_i)+d_i.$$

Los coeficientes mantienen el orden del curso: **a cúbico, b cuadrático, c lineal y d independiente**. No se deben intercambiar con convenciones de otras fuentes.

## 2. Incógnitas y condiciones

Definimos

$$h_i=x_{i+1}-x_i,\qquad m_i=\frac{y_{i+1}-y_i}{h_i},\qquad M_i=S''(x_i).$$

Mᵢ corresponde a la segunda derivada del spline, no necesariamente a la segunda derivada de una función original. Solo se necesitan los puntos.

Existen 4(N−1) coeficientes. Las condiciones son 2(N−1) de interpolación en ambos extremos, N−2 de continuidad de la primera derivada, N−2 de continuidad de la segunda derivada y dos condiciones de frontera. En total: 4(N−1). La continuidad de S ya está asegurada por interpolar ambos extremos de cada tramo; no se cuenta otra vez como condición independiente.

La frontera natural es

$$M_0=M_{N-1}=0.$$

Esto no exige que las pendientes de los extremos sean cero.

## 3. Sistema de ecuaciones

En los nodos interiores, i=1,...,N−2:

$$h_{i-1}M_{i-1}+2(h_{i-1}+h_i)M_i+h_iM_{i+1}=6(m_i-m_{i-1}).$$

El programa conserva las N incógnitas. La primera fila del sistema expresa M₀=0 y la última Mₙ₋₁=0. Las restantes filas contienen las ecuaciones anteriores. `construir_sistema` en `splines/matematica.py` arma estas filas utilizando listas.

Para los nodos (0,0), (1,1), (2,16), (3,81):

$$
\begin{bmatrix}
1&0&0&0\\
1&4&1&0\\
0&1&4&1\\
0&0&0&1
\end{bmatrix}
\begin{bmatrix}M_0\\M_1\\M_2\\M_3\end{bmatrix}
=\begin{bmatrix}0\\84\\300\\0\end{bmatrix}.
$$

## 4. Gauss escrito en Python

`resolver_gauss` en `splines/algebra.py` copia A y B para preservar los originales. En cada columna:

1. Calcula la escala de cada fila como el mayor valor absoluto de sus coeficientes.
2. Selecciona la fila con mayor cociente |pivote|/escala entre las filas pendientes.
3. Intercambia filas si hace falta.
4. Calcula el multiplicador Aᵢₖ/Aₖₖ.
5. Aplica Fᵢ ← Fᵢ − multiplicador·Fₖ a la matriz y al vector.
6. Con el sistema triangular, aplica sustitución regresiva.

No se calcula una matriz inversa. No se utiliza ningún solucionador externo. Los sistemas singulares o con pivotes demasiado pequeños producen un error explicativo.

Para el ejemplo, M=(0;2,4;74,4;0).

## 5. Coeficientes

$$a_i=\frac{M_{i+1}-M_i}{6h_i},\qquad b_i=\frac{M_i}{2},$$

$$c_i=m_i-\frac{h_i(2M_i+M_{i+1})}{6},\qquad d_i=y_i.$$

Las reglas del ejemplo son:

$$S_0(x)=0,4x^3+0,6x,\qquad 0\leq x\leq1,$$

$$S_1(x)=12(x-1)^3+1,2(x-1)^2+1,8(x-1)+1,\qquad1\leq x\leq2,$$

$$S_2(x)=-12,4(x-2)^3+37,2(x-2)^2+40,2(x-2)+16,\qquad2\leq x\leq3.$$

Por ejemplo, S(1,5)=3,7. El spline interpola x⁴ en los nodos, pero no tiene por qué coincidir con x⁴ entre ellos.

## 6. Evaluación y gráfica

Se elige el intervalo que contiene x y se evalúa el polinomio mediante la forma de Horner. En un nodo compartido se elige el tramo derecho, excepto en el último extremo; las verificaciones comprueban que ambos coincidan.

La gráfica evalúa 50 muestras por tramo. No utiliza un interpolador de una biblioteca. Tkinter Canvas transforma las coordenadas matemáticas en posiciones de pantalla y las dibuja. La figura SVG utiliza 60 muestras por tramo.

## 7. Validación

Se comprueba:

- Sᵢ(xᵢ)=yᵢ y Sᵢ(xᵢ₊₁)=yᵢ₊₁ para cada tramo.
- Coincidencia de S, S' y S'' de tramos adyacentes en cada nodo interior.
- Segunda derivada nula en ambos extremos.
- Residuo A·M−B en cada fila del sistema original.

El criterio es error≤10⁻⁸·escala. Para las comparaciones de valores, escala=max(1, |obtenido|, |esperado|). En el residuo del sistema, escala=max(1, suma de los valores absolutos de los productos de la fila, |Bᵢ|). El redondeo de pantalla no participa en estas comprobaciones.

## Referencias del curso y erratas revisadas

- Presentación: *MA331 - S03.1 - Splines cúbicos VF*, diapositivas 11–18.
- Libro: *Libro de splin de grado k*, páginas 8–11.
- La página 8 del libro repite el mismo índice a ambos lados de las igualdades de continuidad: deben compararse tramos adyacentes.
- En la tabla de la página 11, a₀ del ejemplo x⁴ debe ser 0,4. La expresión final de esa página sí utiliza ese valor.
- La respuesta de la página 13 para 1/(1+x²) no interpola los puntos solicitados. El programa calcula su propio resultado y lo valida.
