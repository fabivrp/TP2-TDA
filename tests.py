from colorama import Fore, Style

def extraer_juegos(nombre_archivo):
    juegos = {}

    with open("archivos/" + nombre_archivo, 'r') as archivo:
        contenido = archivo.read().strip().split('\n\n')

    for bloque in contenido:
        lineas = bloque.split('\n')
        nombre_juego = lineas[0].strip()

        movimientos = []
        ganancia_sophia = 0
        ganancia_mateo = 0
        
        for linea in lineas[1:]:
            if "Sophia debe agarrar" in linea or "Mateo agarra" in linea:
                movimientos.extend(linea.strip().split("; "))

            elif "Ganancia Sophia" in linea:
                ganancia_sophia = int(linea.split(":")[1].strip())

            elif "Ganancia Mateo" in linea:
                ganancia_mateo = int(linea.split(":")[1].strip())

        juegos[nombre_juego] = {
            'movimientos': movimientos,
            'ganancia_sophia': ganancia_sophia,
            'ganancia_mateo': ganancia_mateo
        }

    return juegos


def tests(leer_archivo, jugar):
    archivos_disponibles = [5, 10, 20, 25, 50, 100, 1000, 2000, 5000, 10000]

    juegos = extraer_juegos("Resultados Esperados.txt")

    print("Corriendo tests...")

    for archivo in archivos_disponibles:
        print("--------------------------------------------")
        print(f"Corriendo test de {archivo}.txt")

        monedas = leer_archivo(f'archivos/{archivo}.txt')
        elecciones = jugar(monedas)
        paso_test = True

        cant_fallas = 0
        ultima_falla = -1

        for i, movimiento in enumerate(juegos[f'{archivo}.txt']['movimientos']):
            if movimiento != elecciones[i]:
                if ultima_falla != i - 1 or ultima_falla == -1:
                    print(f"({i}) Movimiento incorrecto: {movimiento}. Nuestro algoritmo eligio: {elecciones[i]}.")
                ultima_falla = i
                paso_test = False
                cant_fallas += 1
                
        if paso_test:
            print(Fore.GREEN + f"Paso el test de {archivo}.txt" + Style.RESET_ALL)
        else:
            print(Fore.RED + "No paso el test de", archivo + Style.RESET_ALL)
            print(f"Errores: {cant_fallas}")


def unittest(leer_archivo, jugar, archivo):
    juegos = extraer_juegos("Resultados Esperados.txt")

    monedas = leer_archivo(f'archivos/{archivo}.txt')
    elecciones = jugar(monedas)
    paso_test = True

    cant_fallas = 0

    for i, movimiento in enumerate(juegos[f'{archivo}.txt']['movimientos']):
        if movimiento != elecciones[i]:
            print(f"({i}) Movimiento incorrecto: {movimiento}. Nuestro algoritmo eligio: {elecciones[i]}.")
            paso_test = False
            cant_fallas += 1

    if paso_test:
        print(f"Paso el test de {archivo}.txt")
    else:
        print("No paso el test de", archivo)
        print(f"Errores: {cant_fallas}")
