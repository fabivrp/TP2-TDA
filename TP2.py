import csv
# from tabulate import tabulate
import sys
from tests import tests, unittest
from generador import generardor


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
    izq = 0
    der = len(monedas) - 1
    elecciones = []
    turno_sophia = True
    
    ganancia_sophia = 0
    ganancia_mateo = 0

    while izq <= der:
        if turno_sophia:

            if monedas[izq + 1] > monedas[der]:
                eleccion_izq = optimo[izq + 2][der] if izq + 2 <= der else 0
            else:
                eleccion_izq = optimo[izq + 1][der - 1] if izq + 1 <= der - 1 else 0
            if monedas[izq] > monedas[der - 1]:
                eleccion_der = optimo[izq + 1][der - 1] if izq + 1 <= der - 1 else 0
            else:
                eleccion_der = optimo[izq][der - 2] if izq <= der - 2 else 0
                
            if monedas[izq] + eleccion_izq == optimo[izq][der]:
                elecciones.append(f"Sophia debe agarrar la primera ({monedas[izq]})")
                ganancia_sophia += monedas[izq]
                izq += 1
            elif monedas[izq] + eleccion_der == optimo[izq][der]:
                elecciones.append(f"Sophia debe agarrar la ultima ({monedas[der]})")
                ganancia_sophia += monedas[der]
                der -= 1
            elif monedas[der] + eleccion_der == optimo[izq][der]:
                elecciones.append(f"Sophia debe agarrar la ultima ({monedas[der]})")
                ganancia_sophia += monedas[der]
                der -= 1
            elif monedas[der] + eleccion_izq == optimo[izq][der]:
                elecciones.append(f"Sophia debe agarrar la primera ({monedas[izq]})")
                ganancia_sophia += monedas[izq]
                izq += 1
            
        else:
            if monedas[izq] > monedas[der]:
                elecciones.append(f"Mateo agarra la primera ({monedas[izq]})")  
                ganancia_mateo += monedas[izq]
                izq += 1
            else:
                elecciones.append(f"Mateo agarra la ultima ({monedas[der]})")  
                ganancia_mateo += monedas[der]
                der -= 1

        turno_sophia = not turno_sophia 

    return elecciones, optimo, ganancia_sophia, ganancia_mateo


if __name__ == "__main__":

    if sys.argv[1] == "-h":
        print("Uso: python3 TP2.py [numero_archivo]")
        sys.exit()

    if sys.argv[1] == "-g" or sys.argv[1] == "--gen":
        if len(sys.argv) > 2 and sys.argv[2].isnumeric():
            print("Creando archivo...")
            generardor(int(sys.argv[2]))
            print("Archivo creado con exito!")

            monedas = leer_archivo("archivos/" + sys.argv[2] + ".txt")
    
            elecciones, optimo, ganancia_sophia, ganancia_mateo = jugar(monedas)

            print("Ganancia Sophia:", ganancia_sophia)
            print("Ganancia Mateo:", ganancia_mateo)

        sys.exit()

    if sys.argv[1] == "-t" or sys.argv[1] == "--test":
        if len(sys.argv) > 2 and sys.argv[2].isnumeric():
            unittest(leer_archivo, jugar, sys.argv[2])
            sys.exit()
        tests(leer_archivo, jugar)
        sys.exit()
   
    monedas = leer_archivo(sys.argv[1])
    
    elecciones, optimo, ganancia_sophia, ganancia_mateo = jugar(monedas)
    # print("Las elecciones que deben hacer Sophia y Mateo junto a sus puntajes finales esperados se han guardado en el archivo 'resultado_elecciones.txt'")

    print("Ganancia Sophia:", ganancia_sophia)
    print("Ganancia Mateo:", ganancia_mateo)

    
    # with open("resultado_elecciones.txt", "w") as archivo_resultado:
    #     archivo_resultado.write(tabulate(dict(Persona=["Sophia", "Mateo"], Ganancia=[ganancia_sophia, ganancia_mateo]), headers="keys"))
    #     archivo_resultado.write("\n\n")
    #     archivo_resultado.write(tabulate([[i + 1, eleccion] for i, eleccion in enumerate(elecciones)], headers=["Movimiento", "Eleccion"]))

