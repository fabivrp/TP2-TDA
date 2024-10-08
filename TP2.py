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

    turno_sophia = True

    elecciones = []

    while i <= j:
        if turno_sophia:
            
            if monedas[i] + (optimo[i + 2][j] if i + 2 <= j else 0) > monedas[j] + (optimo[i + 1][j - 1] if i + 1 <= j - 1 else 0):
                elecciones.append(f"Sophia debe agarrar la primera ({monedas[i]})")
                i += 1
            else:
                elecciones.append(f"Sophia debe agarrar la ultima ({monedas[j]})")
                j -= 1
        else: 
            if monedas[i] > monedas[j]:
                elecciones.append(f"Mateo agarra la primera ({monedas[i]})")
                i += 1
            else:
                elecciones.append(f"Mateo agarra la ultima ({monedas[j]})")
                j -= 1

        turno_sophia = not turno_sophia

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
   
