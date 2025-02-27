import sys
import pygame
import numpy as np

pygame.init()

# Colores
BLANCO = (255, 255, 255)
GRIS = (128, 128, 128)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)

# Proporciones y tamaños
ANCHO = 300
LARGO = 300
GROSOR_LINEA = 5
COLS = 3
FILS = 3
TAM_CUADRICULA = ANCHO // COLS
RADIO_CIRCULO = TAM_CUADRICULA // 3
ANCHO_CIRCULO = 15
ANCHO_X = 25

screen = pygame.display.set_mode((ANCHO, LARGO))
pygame.display.set_caption('Triqui')
screen.fill(NEGRO)

board = np.zeros((FILS, COLS))


def dibujar_lineas(color=BLANCO):
    for i in range(1, FILS):
        pygame.draw.line(screen, color, (0, TAM_CUADRICULA * i), (ANCHO, TAM_CUADRICULA * i), GROSOR_LINEA)
        pygame.draw.line(screen, color, (TAM_CUADRICULA * i, 0), (TAM_CUADRICULA * i, LARGO), GROSOR_LINEA)


def dibujar_figuras(color=BLANCO):
    for fil in range(FILS):
        for col in range(COLS):
            if board[fil][col] == 1:
                pygame.draw.circle(screen, color, (
                int(col * TAM_CUADRICULA + TAM_CUADRICULA // 2), int(fil * TAM_CUADRICULA + TAM_CUADRICULA // 2)),
                                   RADIO_CIRCULO, ANCHO_CIRCULO)
            elif board[fil][col] == 2:
                pygame.draw.line(screen, color, (
                col * TAM_CUADRICULA + TAM_CUADRICULA // 4, fil * TAM_CUADRICULA + TAM_CUADRICULA // 4), (
                                 col * TAM_CUADRICULA + 3 * TAM_CUADRICULA // 4,
                                 fil * TAM_CUADRICULA + 3 * TAM_CUADRICULA // 4), ANCHO_X)
                pygame.draw.line(screen, color, (
                col * TAM_CUADRICULA + TAM_CUADRICULA // 4, fil * TAM_CUADRICULA + 3 * TAM_CUADRICULA // 4), (
                                 col * TAM_CUADRICULA + 3 * TAM_CUADRICULA // 4,
                                 fil * TAM_CUADRICULA + TAM_CUADRICULA // 4), ANCHO_X)


def marcar_cuadrado(fila, columna, jugador):
    board[fila][columna] = jugador


def pos_libre(fila, columna):
    return board[fila][columna] == 0


def tablero_full():
    return not np.any(board == 0)


def verificar_ganada(jugador):
    for col in range(COLS):
        if np.all(board[:, col] == jugador):
            return True

    for fil in range(FILS):
        if np.all(board[fil, :] == jugador):
            return True

    if np.all(np.diag(board) == jugador) or np.all(np.diag(np.fliplr(board)) == jugador):
        return True

    return False


def minimax(tablero, profundidad, maximiza):
    if verificar_ganada(2):  # Es muy bueno para la IA
        return float('inf')
    elif verificar_ganada(1):  # extremadamnete malo para la IA
        return float('-inf')
    elif tablero_full():
        return 0

    if maximiza:
        mejor_puntaje = -float('inf')
        for fil in range(FILS):
            for col in range(COLS):
                if tablero[fil][col] == 0:
                    tablero[fil][col] = 2
                    puntaje = minimax(tablero, profundidad + 1, False)
                    tablero[fil][col] = 0
                    mejor_puntaje = max(puntaje, mejor_puntaje)
        return mejor_puntaje

    else:
        mejor_puntaje = float('inf')
        for fil in range(FILS):
            for col in range(COLS):
                if tablero[fil][col] == 0:
                    tablero[fil][col] = 1
                    puntaje = minimax(tablero, profundidad + 1, True)
                    tablero[fil][col] = 0
                    mejor_puntaje = min(puntaje, mejor_puntaje)
        return mejor_puntaje

"""
MAX_DEPTH = 2
def minimax(tablero, profundidad, alpha, beta, maximiza):
    # Condiciones terminales: si hay un ganador o el tablero está lleno
    if verificar_ganada(2):  # Gana la IA (jugador 2)
        return float('inf')
    elif verificar_ganada(1):  # Gana el humano (jugador 1)
        return float('-inf')
    elif tablero_full():
        return 0  # Empate

    if maximiza:  # Turno de la IA (maximiza su puntaje)
        mejor_puntaje = -float('inf')
        for fil in range(FILS):
            for col in range(COLS):
                if tablero[fil][col] == 0:  # Si la casilla está libre
                    tablero[fil][col] = 2  # Simula la jugada de la IA
                    puntaje = minimax(tablero, profundidad + 1, alpha, beta, False)
                    tablero[fil][col] = 0  # Deshace el movimiento

                    mejor_puntaje = max(mejor_puntaje, puntaje)
                    alpha = max(alpha, puntaje)  # Actualiza alpha (mejor valor del maximizador)

                    # Poda alfa-beta: Si beta <= alpha, se corta la búsqueda en esta rama
                    if beta <= alpha:
                        break  
        return mejor_puntaje

    else:  # Turno del jugador humano (minimiza el puntaje de la IA)
        mejor_puntaje = float('inf')
        for fil in range(FILS):
            for col in range(COLS):
                if tablero[fil][col] == 0:  # Si la casilla está libre
                    tablero[fil][col] = 1  # Simula la jugada del humano
                    puntaje = minimax(tablero, profundidad + 1, alpha, beta, True)
                    tablero[fil][col] = 0  # Deshace el movimiento

                    mejor_puntaje = min(mejor_puntaje, puntaje)
                    beta = min(beta, puntaje)  # Actualiza beta (mejor valor del minimizador)

                    # Poda alfa-beta: Si beta <= alpha, se corta la búsqueda en esta rama
                    if beta <= alpha:
                        break  
        return mejor_puntaje




"""




def mejor_mov():
    mejor_puntaje = -float('inf')
    mov = (-1, -1)
    for fil in range(FILS):
        for col in range(COLS):
            if board[fil][col] == 0:
                board[fil][col] = 2
                puntaje = minimax(board, 0, False)
                board[fil][col] = 0
                if puntaje > mejor_puntaje:
                    mejor_puntaje = puntaje
                    mov = (fil, col)

    if mov != (-1, -1):
        marcar_cuadrado(mov[0], mov[1], 2)
        return True
    return False


def reiniciar_juego():
    screen.fill(NEGRO)
    dibujar_lineas()
    board.fill(0)


dibujar_lineas()
jugador = 1
juego_terminado = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not juego_terminado:
            mouse_x, mouse_y = event.pos

            fila = mouse_y // TAM_CUADRICULA
            columna = mouse_x // TAM_CUADRICULA

            if 0 <= fila < FILS and 0 <= columna < COLS and pos_libre(fila, columna):
                marcar_cuadrado(fila, columna, jugador)

                if verificar_ganada(jugador):
                    juego_terminado = True

                jugador = jugador % 2 + 1

                if not juego_terminado and mejor_mov():
                    if verificar_ganada(2):
                        juego_terminado = True
                    jugador = jugador % 2 + 1

                if not juego_terminado and tablero_full():
                    juego_terminado = True

            dibujar_figuras()
            if juego_terminado:
                if verificar_ganada(2):
                    dibujar_figuras(ROJO)
                    dibujar_lineas(ROJO)
                elif verificar_ganada(1):
                    dibujar_figuras(VERDE)
                    dibujar_lineas(VERDE)
                else:
                    dibujar_figuras(GRIS)
                    dibujar_lineas(GRIS)

    pygame.display.update()
