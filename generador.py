from random import randint

def generardor(n, escala = 1):
    with open(f'archivos/{n}.txt', 'w') as archivo:
        archivo.write('# Los valores de las monedas de la fila se muestran tal cual su orden correspondiente, separados por ; \n')
        
        for i in range(n):
            archivo.write(f'{randint(1, 100 * escala)}')
            if i < n - 1:
                archivo.write(';')

        archivo.write('\n')
            