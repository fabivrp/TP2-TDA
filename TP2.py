import csv
import math
# from tabulate import tabulate

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

    elecciones_sophia = []
    elecciones_mateo = []

    # print(tabulate(optimo, tablefmt="fancy_grid"))

    # Falta reconstruir la solución acá

    return elecciones_sophia, elecciones_mateo


if __name__ == "__main__":
    monedas = leer_archivo('archivos/10.txt')

    elecciones_sophia, elecciones_mateo = jugar(monedas)

    print("Elecciones Sophia:", elecciones_sophia)
    print("Elecciones Mateo:", elecciones_mateo)

