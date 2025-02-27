import sys
import pygame
import numpy as np
import math

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
                pygame.draw.circle(screen, color, (int(col * TAM_CUADRICULA + TAM_CUADRICULA // 2), 
                                                     int(fil * TAM_CUADRICULA + TAM_CUADRICULA // 2)), 
                                                     RADIO_CIRCULO, ANCHO_CIRCULO)
            elif board[fil][col] == 2:
                pygame.draw.line(screen, color, 
                                 (col * TAM_CUADRICULA + TAM_CUADRICULA // 4, fil * TAM_CUADRICULA + TAM_CUADRICULA // 4), 
                                 (col * TAM_CUADRICULA + 3 * TAM_CUADRICULA // 4, fil * TAM_CUADRICULA + 3 * TAM_CUADRICULA // 4), 
                                 ANCHO_X)
                pygame.draw.line(screen, color, 
                                 (col * TAM_CUADRICULA + TAM_CUADRICULA // 4, fil * TAM_CUADRICULA + 3 * TAM_CUADRICULA // 4), 
                                 (col * TAM_CUADRICULA + 3 * TAM_CUADRICULA // 4, fil * TAM_CUADRICULA + TAM_CUADRICULA // 4), 
                                 ANCHO_X)

def marcar_cuadrado(fila, columna, jugador):
    board[fila][columna] = jugador

def pos_libre(fila, columna):
    return board[fila][columna] == 0

def tablero_full():
    return not np.any(board == 0)

def verificar_ganada(jugador):
    # Verifica columnas
    for col in range(COLS):
        if np.all(board[:, col] == jugador):
            return True
    # Verifica filas
    for fil in range(FILS):
        if np.all(board[fil, :] == jugador):
            return True
    # Verifica diagonales
    if np.all(np.diag(board) == jugador) or np.all(np.diag(np.fliplr(board)) == jugador):
        return True
    return False

# Límite de profundidad para la búsqueda (2 niveles para análisis)
MAX_DEPTH = 2

def minimax(tablero, profundidad, alpha, beta, maximiza):
    # Condiciones terminales: si hay un ganador, si el tablero está lleno o se alcanzó el límite de profundidad
    if verificar_ganada(2):  # Gana la IA (jugador 2)
        return float('inf')
    elif verificar_ganada(1):  # Gana el humano (jugador 1)
        return float('-inf')
    elif tablero_full() or profundidad >= MAX_DEPTH:
        return 0  # Empate o límite alcanzado: se retorna 0
    
    if maximiza:
        mejor_puntaje = -float('inf')
        for fil in range(FILS):
            for col in range(COLS):
                if tablero[fil][col] == 0:
                    tablero[fil][col] = 2  # Simula el movimiento de la IA (jugador 2)
                    puntaje = minimax(tablero, profundidad + 1, alpha, beta, False)
                    tablero[fil][col] = 0  # Deshace el movimiento\n                    mejor_puntaje = max(mejor_puntaje, puntaje)\n                    alpha = max(alpha, puntaje)  # Actualiza alpha para MAX\n                    if beta <= alpha:  # Poda alfa-beta: detiene la exploración de la rama\n                        break\n        return mejor_puntaje\n    else:\n        mejor_puntaje = float('inf')\n        for fil in range(FILS):\n            for col in range(COLS):\n                if tablero[fil][col] == 0:\n                    tablero[fil][col] = 1  # Simula el movimiento del humano (jugador 1)\n                    puntaje = minimax(tablero, profundidad + 1, alpha, beta, True)\n                    tablero[fil][col] = 0  # Deshace el movimiento\n                    mejor_puntaje = min(mejor_puntaje, puntaje)\n                    beta = min(beta, puntaje)  # Actualiza beta para MIN\n                    if beta <= alpha:  # Poda alfa-beta: detiene la exploración de la rama\n                        break\n        return mejor_puntaje

def mejor_mov():
    mejor_puntaje = -float('inf')
    mov = (-1, -1)
    for fil in range(FILS):
        for col in range(COLS):
            if board[fil][col] == 0:
                board[fil][col] = 2  # Simula el movimiento de la IA\n                puntaje = minimax(board, 0, -float('inf'), float('inf'), False)\n                board[fil][col] = 0  # Deshace el movimiento\n                if puntaje > mejor_puntaje:\n                    mejor_puntaje = puntaje\n                    mov = (fil, col)\n    if mov != (-1, -1):\n        marcar_cuadrado(mov[0], mov[1], 2)\n        return True\n    return False

def reiniciar_juego():
    screen.fill(NEGRO)
    dibujar_lineas()
    board.fill(0)

# Dibuja la cuadrícula inicial
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
