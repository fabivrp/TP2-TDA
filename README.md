# TP2

**Importante**: No tocar la estructura del directorio.

## Cómo usar los archivos

Primero hay que instalar unos paquetes en un entorno.

```
pip install -r requirements.txt
```

### Usar un archivo en particular

Para ejecutar un archivo en particular, ejecutar el comando (ponemos el ejemplo de 25.txt)

``` 
python TP2.py archivos/25.txt
```

### Generar un caso

Para generar un caso y ejecutar el algoritmo, ejecutar el comando:

``` 
python TP2.py --gen [numero_entero_de_monedas_totales]
```

### Ejecutar una prueba en un archivo en particular
```
python TP2.py --test [numero_archivo]
```

ó
```
python TP2.py -t [numero_archivo]
```

### Ejecutar pruebas en todos los archivos
```
python TP2.py --test
```

ó
```
python TP2.py -t
```
