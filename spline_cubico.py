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

    # h_i = x_(i+1)-x_i
    h = np.zeros(n-1)

    for i in range(n-1):

        h[i] = x[i+1]-x[i]


    # Sistema AM = B

    A = np.zeros((n,n))
    B = np.zeros(n)


    # Condiciones naturales:
    # M0 = 0
    # Mn = 0

    A[0][0] = 1
    A[n-1][n-1] = 1


    # Ecuaciones internas

    for i in range(1,n-1):

        A[i][i-1] = h[i-1]

        A[i][i] = 2*(h[i-1]+h[i])

        A[i][i+1] = h[i]


        B[i] = 6 * (
            ((y[i+1]-y[i])/h[i])
            -
            ((y[i]-y[i-1])/h[i-1])
        )


    return A,B,h

# =====================================================
# CALCULAR COEFICIENTES DEL SPLINE
# =====================================================

def calcular_coeficientes(x,y):


    A,B,h = construir_sistema(x,y)

    # A M = B
    # M son las segundas derivadas

    M = np.linalg.solve(A,B)


    n = len(x)-1

    # Coeficientes:

    a = np.zeros(n)

    b = np.zeros(n)

    c = np.zeros(n)

    d = np.zeros(n)



    for i in range(n):
        # Coeficiente cúbico

        a[i] = (
            (M[i+1]-M[i])
            /
            (6*h[i])
        )

        # Coeficiente cuadrático

        b[i] = M[i]/2

        # Coeficiente lineal

        c[i] = (
            (y[i+1]-y[i])/h[i]
            -
            h[i]*(2*M[i]+M[i+1])/6
        )

        # Término independiente

        d[i] = y[i]

    return a,b,c,d,M,A,B


# =====================================================
# MOSTRAR RESULTADOS
# =====================================================

def mostrar_resultados(x,a,b,c,d,M,A,B):


    print("\n================================")
    print(" MATRIZ DEL SISTEMA")
    print("================================")

    print(A)


    print("\nVector B:")

    print(B)

    print("\n================================")
    print(" SEGUNDAS DERIVADAS M")
    print("================================")

    print(M)

    print("\n================================")
    print(" POLINOMIOS SPLINE")
    print("================================")

    for i in range(len(a)):


        print(f"\nIntervalo [{x[i]}, {x[i+1]}]")


        print(
            f"S{i}(x)= "
            f"{a[i]:.4f}(x-{x[i]})³ "
            f"+ {b[i]:.4f}(x-{x[i]})² "
            f"+ {c[i]:.4f}(x-{x[i]}) "
            f"+ {d[i]:.4f}"
        )

# =====================================================
# PROGRAMA PRINCIPAL
# =====================================================


print("================================")
print(" SPLINE CÚBICO NATURAL")
print("================================")


x,y = ingresar_puntos()


print("\nPuntos ingresados:")

for i in range(len(x)):

    print(f"({x[i]}, {y[i]})")

a,b,c,d,M,A,B = calcular_coeficientes(x,y)

mostrar_resultados(
    x,
    a,
    b,
    c,
    d,
    M,
    A,
    B
)