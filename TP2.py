import csv
import math

def leer_archivo(archivo):
    with open(archivo, newline='') as csvfile:
        data = list(csv.reader(csvfile, delimiter=';'))
        return [int(moneda) for moneda in data[1:][0]]
    
def ecuacion_recurrencia(memoria, turno, primer_moneda, ultima_moneda):
    if turno == 0:
        return max(0 + primer_moneda, 0 + ultima_moneda)
    return max(memoria[turno - 1] + primer_moneda, memoria[turno - 1] + ultima_moneda)

def greedy(turno, primer_moneda, ultima_moneda):
    if turno == 1:
        return max(0 + primer_moneda, 0 + ultima_moneda)
    return max(primer_moneda, ultima_moneda)

def quitar_moneda_pd(izq, der, monedas, memoria_sophie, turno):
    if memoria_sophie[turno - 1] + monedas[izq] == memoria_sophie[turno]:
        return izq + 1, der
    else:
        return izq, der - 1

def quitar_moneda(izq, der, primer_moneda, ultima_moneda):
    if primer_moneda > ultima_moneda:
        return izq + 1, der
    else:
        return izq, der - 1

    
def jugar(monedas: list, memoria_sophie: list, memoria_mateo: list):

    izq = 0
    der = len(monedas) - 1

    for turno in range(len(monedas)):

        # Turno de Sophia
        if turno % 2 == 0:

            n = turno // 2
            memoria_sophie[n] = ecuacion_recurrencia(memoria_sophie, n, monedas[izq], monedas[der])

            # Saco la moneda elegida
            izq, der = quitar_moneda_pd(izq, der, monedas, memoria_sophie, n)

        else:
            n = math.floor(turno / 2)
            memoria_mateo[n] = memoria_mateo[n - 1] + greedy(n, monedas[izq], monedas[der])

            # Saco la moneda elegida
            izq, der = quitar_moneda(izq, der, monedas[izq], monedas[der])

    return reconstruir(monedas, memoria_sophie, memoria_mateo)

def reconstruir(monedas, memoria_sophie, memoria_mateo):
    monedas_elegidas = []
    

    izq = 0
    der = len(monedas) - 1

    for turno in range(len(monedas)):
        if turno % 2 == 0:
            if memoria_sophie[turno // 2 - 1] + monedas[izq] == memoria_sophie[turno // 2]:
                monedas_elegidas.append("Sophie elige " + str(monedas[izq]))
                izq += 1
            else:
                monedas_elegidas.append("Sophie elige " + str(monedas[der]))
                der -= 1
        else:
            if memoria_mateo[math.floor(turno // 2) - 1] + monedas[izq] == memoria_mateo[math.floor(turno // 2)]:
                monedas_elegidas.append("Mateo elige " + str(monedas[izq]))
                izq += 1
            else:
                monedas_elegidas.append("Mateo elige " + str(monedas[der]))
                der -= 1

    return monedas_elegidas


if __name__ == "__main__":
    monedas = leer_archivo('archivos/10.txt')

    # Inicializo la memoria con 0s. Si monedas es par, la memoria es la mitad de monedas. 
    # Si monedas es impar, la memoria es la mitad de monedas + 1.
    memoria_sophie = [0] * (math.ceil(len(monedas) / 2)) 
    memoria_mateo = [0] * (len(monedas) // 2)  


    print(jugar(monedas, memoria_sophie, memoria_mateo))

    print(memoria_sophie)
    print(memoria_mateo)