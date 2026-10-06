import sys
import msvcrt
import os
import time
import random

# ==========================================
# CONFIGURACIÓN
# ==========================================

FILAS = 80
COLUMNAS = 80

SIMBOLO_VIVO = "■"
SIMBOLO_MUERTO = "·"
SIMBOLO_CURSOR = "□"

COLORES_HEX = ["00ff9c", "00d9ff", "ffcc00", "ff5c5c"]

# ==========================================
# FUNCIONES DE CONSOLA (basadas en tu script)
# ==========================================

def cls_imprimir(texto):
    sys.stdout.write(texto)
    sys.stdout.flush()

def cls_mover_cursor(fila, columna):
    cls_imprimir(f"\033[{fila};{columna}H")

def cls_ocultar_cursor():
    cls_imprimir("\033[?25l")

def cls_mostrar_cursor():
    cls_imprimir("\033[?25h")

def cls_limpiar_pantalla():
    cls_imprimir("\033[2J\033[H")

def cls_restaurar_colores():
    cls_imprimir("\033[0m")

def cls_establecer_color_hex(hex_color):
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    cls_imprimir(f"\033[38;2;{r};{g};{b}m")

# ==========================================
# LECTURA DE TECLAS
# ==========================================

def cls_leer_tecla():

    if not msvcrt.kbhit():
        return None

    tecla = msvcrt.getch()

    if tecla == b'\r':
        return "ENTER"

    if tecla in (b'\x00', b'\xe0'):
        flecha = msvcrt.getch()
        if flecha == b'H': return "ARRIBA"
        if flecha == b'P': return "ABAJO"
        if flecha == b'M': return "DERECHA"
        if flecha == b'K': return "IZQUIERDA"

    if tecla.lower() == b's':
        return "START"

    if tecla.lower() == b'q':
        return "SALIR"

    return None

# ==========================================
# DIBUJAR MATRIZ
# ==========================================

def dibujar_matriz(matriz):

    for f in range(FILAS):
        for c in range(COLUMNAS):

            col_visual = (c * 2) + 1
            cls_mover_cursor(f+12, col_visual)

            if matriz[f][c] == 1:
                cls_establecer_color_hex(random.choice(COLORES_HEX))
                cls_imprimir(SIMBOLO_VIVO)
                cls_restaurar_colores()
            else:
                cls_imprimir(SIMBOLO_MUERTO)

# ==========================================
# DIBUJAR CURSOR
# ==========================================

def dibujar_cursor(fila, columna):

    col_visual = (columna * 2) + 1
    cls_mover_cursor(fila+12, col_visual)
    cls_establecer_color_hex("ffffff")
    cls_imprimir(SIMBOLO_CURSOR)
    cls_restaurar_colores()

# ==========================================
# CONTAR VECINOS
# ==========================================

def vecinos(matriz, fila, col):

    total = 0

    for i in [-1,0,1]:
        for j in [-1,0,1]:

            if i == 0 and j == 0:
                continue

            nf = fila + i
            nc = col + j

            if 0 <= nf < FILAS and 0 <= nc < COLUMNAS:
                total += matriz[nf][nc]

    return total

# ==========================================
# GENERAR SIGUIENTE GENERACIÓN
# ==========================================

def siguiente_generacion(matriz):

    nueva = [[0]*COLUMNAS for _ in range(FILAS)]

    for f in range(FILAS):
        for c in range(COLUMNAS):

            v = vecinos(matriz,f,c)

            if matriz[f][c] == 1 and (v == 2 or v == 3):
                nueva[f][c] = 1

            if matriz[f][c] == 0 and v == 3:
                nueva[f][c] = 1

    return nueva

# ==========================================
# PANTALLA DE TÍTULO
# ==========================================

def mostrar_titulo():
    cls_limpiar_pantalla()

    cls_mover_cursor(1,1)
    cls_imprimir("===============================================")

    cls_mover_cursor(2,1)
    cls_imprimir("         JUEGO DE LA VIDA DE CONWAY")

    cls_mover_cursor(3,1)
    cls_imprimir("          Autor: Adalberto Ruiz Chavez")

    cls_mover_cursor(4,1)
    cls_imprimir("===============================================")

    cls_mover_cursor(6,1)
    cls_imprimir("INSTRUCCIONES:")

    cls_mover_cursor(7,1)
    cls_imprimir("Flechas  -> mover cursor")

    cls_mover_cursor(8,1)
    cls_imprimir("ENTER    -> activar/desactivar celula")

    cls_mover_cursor(9,1)
    cls_imprimir("S        -> iniciar simulacion")

    cls_mover_cursor(10,1)
    cls_imprimir("Q        -> salir")

# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def iniciar():

    os.system("")
    cls_ocultar_cursor()

    matriz = [[0]*COLUMNAS for _ in range(FILAS)]

    fila = 0
    col = 0

    mostrar_titulo()
    dibujar_matriz(matriz)
    dibujar_cursor(fila, col)

    try:

        simulando = False

        while True:

            tecla = cls_leer_tecla()

            if tecla == "SALIR":
                break

            if not simulando:

                if tecla == "ARRIBA":
                    fila = max(0, fila-1)

                elif tecla == "ABAJO":
                    fila = min(FILAS-1, fila+1)

                elif tecla == "IZQUIERDA":
                    col = max(0, col-1)

                elif tecla == "DERECHA":
                    col = min(COLUMNAS-1, col+1)

                elif tecla == "ENTER":
                    matriz[fila][col] = 1 - matriz[fila][col]

                elif tecla == "START":
                    simulando = True

                dibujar_matriz(matriz)
                dibujar_cursor(fila,col)

            else:

                matriz = siguiente_generacion(matriz)
                dibujar_matriz(matriz)
                time.sleep(0.1)

    finally:

        cls_restaurar_colores()
        cls_mostrar_cursor()
        cls_mover_cursor(FILAS+10,1)

        print("\nSimulación terminada")

if __name__ == "__main__":
    iniciar()