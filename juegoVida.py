import time
import os
import sys
from colorama import init
from colorama.ansi import clear_screen



def limpiar_pantalla():
    """
    Limpia la pantalla usando secuencias ANSI y lleva el cursor
    a la esquina superior izquierda.
    Con colorama debería funcionar bien en Windows.
    """
    # \033[2J -> limpia toda la pantalla
    # \033[H  -> mueve el cursor a la posición (fila 1, columna 1)
    sys.stdout.write(clear_screen())
    sys.stdout.flush()
    
def limpiar_pantalla_ansi():
    """
    Limpia la pantalla usando secuencias ANSI y lleva el cursor
    a la esquina superior izquierda. Suele ser más fluido que os.system('clear').
    """
    # \033[2J -> limpia toda la pantalla
    # \033[H  -> mueve el cursor a la posición (fila 1, columna 1)
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def crear_tablero_vacio(filas, columnas):
    #voy a crear las celulas muertas en el tablero
    
    return [[0 for _ in range(columnas)] for _ in range(filas)]


def introducir_celulas_vivas(tablero):
    #voy a crear las celulas vivas en el tablero

    filas = len(tablero)
    columnas = len(tablero[0])

    print("\nIntroduce las posiciones de las células vivas.")
    print("Formato: fila columna  (empezando desde 0)")
    print("Escribe 'fin' para terminar.\n")

    while True:
        entrada = input("introduzca la fila y columna donde quiera que las celulas vivas se posicionen: ").strip()
        if entrada.lower() == "fin":
            break
        
        try:
            f, c = map(int, entrada.split())
        except ValueError:
            print("Entrada no válida, introduzca dos valores validos")
            continue

        if not (0 <= f < filas and 0 <= c < columnas):
            print("Coordenadas fuera del tablero.")
            continue

        tablero[f][c] = 1
        print(f"Celda viva añadida en ({f}, {c})")

    return tablero

def mostrar_tablero(tablero, generacion):
    """
    Muestra el tablero por consola sobrescribiendo el contenido anterior.
    """
    limpiar_pantalla_ansi()

    print(f"Juego de la Vida de Conway - Generación {generacion}")
    # Línea separadora del ancho del tablero
    print("-" * len(tablero[0]))

    for fila in tablero:
        linea = ""
        for celda in fila:
            linea += "■" if celda == 1 else " "
        print(linea)

    print("-" * len(tablero[0]))
    print("Ctrl + C para salir")

def contar_vecinos_vivos(tablero, fila, col):
    """
    Cuenta los vecinos vivos de la celda (fila, col).
    Los bordes consideran celdas fuera como muertas.
    """
    filas = len(tablero)
    columnas = len(tablero[0])
    vecinos_vivos = 0

    for df in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if df == 0 and dc == 0:
                continue

            nf = fila + df
            nc = col + dc

            if 0 <= nf < filas and 0 <= nc < columnas:
                vecinos_vivos += tablero[nf][nc]

    return vecinos_vivos

def siguiente_generacion(tablero):
    """
    Aplica las reglas del Juego de la Vida y genera
    el siguiente estado del tablero.
    """
    filas = len(tablero)
    columnas = len(tablero[0])

    nuevo_tablero = [[0 for _ in range(columnas)] for _ in range(filas)]

    for f in range(filas):
        for c in range(columnas):
            vecinos = contar_vecinos_vivos(tablero, f, c)

            if tablero[f][c] == 1:
                if vecinos == 2 or vecinos == 3:
                    nuevo_tablero[f][c] = 1
            else:
                if vecinos == 3:
                    nuevo_tablero[f][c] = 1

    return nuevo_tablero 

def main():
    print("=== Juego de la Vida de Conway ===")

    try:
        filas = int(input("Número de filas: "))
        columnas = int(input("Número de columnas: "))
    except ValueError:
        print("Entrada no válida.")
        return

    if filas <= 0 or columnas <= 0:
        print("Las dimensiones deben ser mayores que 0.")
        return

    tablero = crear_tablero_vacio(filas, columnas)
    tablero = introducir_celulas_vivas(tablero)

    try:
        generaciones = int(input("Número de generaciones (0 = infinito): "))
    except ValueError:
        print("Entrada no válida.")
        return

    try:
        pausa = float(input("Pausa entre generaciones en segundos (ej. 0.3): "))
    except ValueError:
        pausa = 0.3

    generacion = 0

    try:
        if generaciones == 0:
            while True:
                mostrar_tablero(tablero, generacion)
                tablero = siguiente_generacion(tablero)
                generacion = generacion + 1
                time.sleep(pausa)
        else:
            for _ in range(generaciones):
                mostrar_tablero(tablero, generacion)
                tablero = siguiente_generacion(tablero)
                generacion = generacion + 1
                time.sleep(pausa)
    except KeyboardInterrupt:
        print("\nSimulación detenida por el usuario.")
            
    

if __name__ == "__main__":
    main()




        

        
        
        

    

    
