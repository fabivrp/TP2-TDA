import csv
from tabulate import tabulate
import sys
from tests import tests

def leer_archivo(archivo):
    with open(archivo, newline='') as csvfile:
        data = list(csv.reader(csvfile, delimiter=';'))
        return [int(moneda) for moneda in data[1:][0]]
    

def ecuacion_recurrencia(optimo, monedas, izq, der):

    if monedas[izq + 1] > monedas[der]:
        eleccion_izq = optimo[izq + 2][der] if izq + 2 <= der else 0
    else:
        eleccion_izq = optimo[izq + 1][der - 1] if izq + 1 <= der - 1 else 0

    if monedas[izq] > monedas[der - 1]:
        eleccion_der = optimo[izq + 1][der - 1] if izq + 1 <= der - 1 else 0
    else:
        eleccion_der = optimo[izq][der - 2] if izq <= der - 2 else 0

    return max(monedas[izq] + eleccion_izq, monedas[der] + eleccion_der)


def jugar(monedas: list):

    optimo = [[0 for _ in range(len(monedas))] for _ in range(len(monedas))]

    for i in range(len(monedas)):
        optimo[i][i] = monedas[i]

    for cantidad in range(2, len(monedas) + 1):
        for i in range(len(monedas) - cantidad + 1):
            j = i + cantidad - 1
            optimo[i][j] = ecuacion_recurrencia(optimo, monedas, i, j)

    return reconstruir_solucion(optimo, monedas)


def reconstruir_solucion(optimo, monedas):
    i = 0
    j = len(monedas) - 1

    print(tabulate(optimo, headers=[i for i in range(1, len(monedas) + 1)], showindex=[i for i in range(1, len(monedas) + 1)]))

    turno_sophia = True

    ganancia_sophia = 0
    ganancia_mateo = 0

    elecciones = []

    while i <= j:
        if turno_sophia:
            if monedas[i] + optimo[i + 2][j] == optimo[i][j]:
                elecciones.append(f"Sophia debe agarrar la primera ({monedas[i]})")
                ganancia_sophia += monedas[i]
                i += 1
            elif monedas[i] + optimo[i + 1][j - 1] == optimo[i][j]:
                elecciones.append(f"Sophia debe agarrar la primera ({monedas[i]})")
                ganancia_sophia += monedas[i]
                i += 1
            elif monedas[j] + optimo[i + 1][j - 1] == optimo[i][j]:
                elecciones.append(f"Sophia debe agarrar la ultima ({monedas[j]})")
                ganancia_sophia += monedas[j]
                j -= 1
            elif monedas[j] + optimo[i][j - 2] == optimo[i][j]:
                elecciones.append(f"Sophia debe agarrar la ultima ({monedas[j]})")
                ganancia_sophia += monedas[j]
                j -= 1

            # Está faltando un caso acá. Cuando haces la vuelta en la matriz, 
            # a veces tenés dos soluciones posibles que pueden ir. 
            # En ese caso tendría que usar la moneda más grande, 
            # pero a veces usa la chica por como están los ifs.

            # Ejemplo: 

            #      1    2    3     4     5
            # --  ---  ---  ---  ----  ----
            # 1   96  594  (533) 1268  (1483)
            # 2    0  594   594  1111   1544
            # 3    0    0   437  674   (1387)
            # 4    0    0    0   674    950
            # 5    0    0    0     0    950

            # La primera moneda que tendría que agarrar Sophia es la de 950, entonces
            # optimo[0][4-2] + 950 (ultima moneda) = 533 + 950 = 1483
            # 
            # Pero también, es válido el caso de:
            # optimo[0+2][4] + 96 (primera moneda) = 1387 + 96 = 1483
            # 
            # En este caso, debería elegir la moneda más grande, pero el algoritmo
            # elige la moneda que primero encuentra.

        else:
            if monedas[i] > monedas[j]:
                elecciones.append(f"Mateo agarra la primera ({monedas[i]})")
                ganancia_mateo += monedas[i]
                i += 1
            else:
                elecciones.append(f"Mateo agarra la ultima ({monedas[j]})")
                ganancia_mateo += monedas[j]
                j -= 1

        turno_sophia = not turno_sophia

    print(f"Ganancia Sophia: {ganancia_sophia}")
    print(f"Ganancia Mateo: {ganancia_mateo}")

    return elecciones



if __name__ == "__main__":

    if sys.argv[1] == "-h":
        print("Uso: python3 TP2.py [numero_archivo]")
        sys.exit()

    if len(sys.argv) != 2:
        print("Error: cantidad de argumentos invalida")
        sys.exit()

    if sys.argv[1] == "-t" or sys.argv[1] == "--test":
        tests(leer_archivo, jugar)
        sys.exit()

    monedas = leer_archivo(f'archivos/{str(sys.argv[1])}.txt')
    elecciones = jugar(monedas)

    print(tabulate([[i + 1, eleccion] for i, eleccion in enumerate(elecciones)], headers=["Movimiento", "Eleccion"]))
   
