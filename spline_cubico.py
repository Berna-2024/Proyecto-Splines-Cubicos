import numpy as np


# =====================================================
# INGRESO DE DATOS
# =====================================================

def ingresar_puntos():

    cantidad = int(input("Ingrese cantidad de puntos: "))

    x = []
    y = []

    print("\nIngrese los valores:")

    for i in range(cantidad):
        xi = float(input(f"x{i}: "))
        yi = float(input(f"y{i}: "))

        x.append(xi)
        y.append(yi)

    return np.array(x), np.array(y)



# =====================================================
# CONSTRUCCIÓN DEL SISTEMA MATRICIAL
# SPLINE CÚBICO NATURAL
# =====================================================

def construir_sistema(x, y):

    n = len(x)

    h = np.zeros(n-1)


    # Diferencias entre puntos
    for i in range(n-1):
        h[i] = x[i+1] - x[i]


    # Matriz A y vector B
    A = np.zeros((n, n))
    B = np.zeros(n)


    # Condiciones naturales
    A[0][0] = 1
    A[n-1][n-1] = 1


    # Ecuaciones internas
    for i in range(1, n-1):

        A[i][i-1] = h[i-1]

        A[i][i] = 2*(h[i-1] + h[i])

        A[i][i+1] = h[i]


        B[i] = (
            3*((y[i+1]-y[i])/h[i])
            -
            3*((y[i]-y[i-1])/h[i-1])
        )


    return A, B, h



# =====================================================
# CALCULAR COEFICIENTES DEL SPLINE
# =====================================================

def calcular_coeficientes(x, y):

    A, B, h = construir_sistema(x,y)


    # Resolver sistema matricial:
    # A*C = B

    c = np.linalg.solve(A,B)


    n = len(x)-1

    a = np.zeros(n)
    b = np.zeros(n)
    d = np.zeros(n)


    for i in range(n):

        a[i] = y[i]


        b[i] = (
            (y[i+1]-y[i])/h[i]
            -
            h[i]*(2*c[i]+c[i+1])/3
        )


        d[i] = (
            (c[i+1]-c[i])
            /
            (3*h[i])
        )


    return a,b,c,d,A,B



# =====================================================
# MOSTRAR RESULTADOS
# =====================================================

def mostrar_resultados(x,a,b,c,d,A,B):


    print("\n================================")
    print(" MATRIZ DEL SISTEMA")
    print("================================")

    print(A)


    print("\nVector B:")
    print(B)



    print("\n================================")
    print(" POLINOMIOS SPLINE")
    print("================================")


    for i in range(len(a)):

        print(f"\nIntervalo [{x[i]}, {x[i+1]}]")


        print(
            f"S{i}(x)= "
            f"{a[i]:.4f}"
            f" + {b[i]:.4f}(x-{x[i]})"
            f" + {c[i]:.4f}(x-{x[i]})²"
            f" + {d[i]:.4f}(x-{x[i]})³"
        )



# =====================================================
# PROGRAMA PRINCIPAL
# =====================================================

print("================================")
print("     SPLINE CÚBICO NATURAL")
print("================================")


x,y = ingresar_puntos()


print("\nPuntos ingresados:")

for i in range(len(x)):
    print(f"({x[i]}, {y[i]})")


a,b,c,d,A,B = calcular_coeficientes(x,y)


mostrar_resultados(x,a,b,c,d,A,B)