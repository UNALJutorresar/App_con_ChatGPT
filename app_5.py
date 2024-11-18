# -*- coding: utf-8 -*-
"""apps.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14uS8HhY1nJykgarqC4gDQ9hIQpbGqoIT
"""

import pygame
import streamlit as st
import numpy as np
import io
from PIL import Image

# Inicialización de Pygame
pygame.init()

# Definir parámetros del pozo de pelotas
WIDTH, HEIGHT = 600, 400
FPS = 60

# Propiedades de la pelota
RADIUS = 20
GRAVITY = 0.5
FRICTION = 0.99

# Definir la pantalla de Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pozo de Pelotas")

# Clase para la pelota
class Ball:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = RADIUS
        self.color = color
        self.x_vel = 0
        self.y_vel = 0

    def move(self):
        """Actualizar la posición de la pelota considerando la gravedad y la fricción."""
        self.y_vel += GRAVITY  # Aplicar gravedad
        self.x += self.x_vel
        self.y += self.y_vel
        self.x_vel *= FRICTION  # Aplicar fricción
        self.y_vel *= FRICTION  # Aplicar fricción

        # Colisiones con los bordes (pantalla)
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.x_vel = -self.x_vel  # Rebotar en el eje X
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.y_vel = -self.y_vel  # Rebotar en el eje Y

    def draw(self, screen):
        """Dibujar la pelota en la pantalla."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Crear varias pelotas
balls = [
    Ball(np.random.randint(50, WIDTH-50), np.random.randint(50, HEIGHT-50), (np.random.randint(255), np.random.randint(255), np.random.randint(255)))
    for _ in range(5)
]

def game_loop():
    """Lógica principal del juego que maneja las pelotas y su interacción."""
    screen.fill((255, 255, 255))  # Fondo blanco

    # Mover y dibujar las pelotas
    for ball in balls:
        ball.move()
        ball.draw(screen)

    pygame.display.flip()

def capture_screen():
    """Capturar la pantalla de Pygame como una imagen y convertirla en un formato adecuado para Streamlit."""
    # Capturar la pantalla de Pygame
    pygame.image.save(screen, "pozo_pelotas.png")

    # Abrir la imagen capturada con PIL y convertirla a un formato compatible con Streamlit
    img = Image.open("pozo_pelotas.png")
    return img

# Interfaz de Streamlit
def main():
    st.title("Pozo de Pelotas con Física de Colisión y Gravedad")
    st.write("Arrastra las pelotas con el cursor y observa cómo interactúan entre ellas y con las paredes.")

    # Mostrar instrucciones
    st.markdown("""
    **Instrucciones:**
    - Las pelotas caen debido a la gravedad.
    - Las pelotas rebotan entre sí y contra las paredes.
    - Arrastra las pelotas con el mouse para moverlas.
    """)

    # Crear el control para iniciar/pausar la animación
    if 'is_running' not in st.session_state:
        st.session_state.is_running = False

    start_button = st.button('Iniciar/Pausar animación')

    if start_button:
        st.session_state.is_running = not st.session_state.is_running

    # Si la animación está en ejecución, continuar generando fotogramas
    if st.session_state.is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                st.stop()

        # Lógica del juego
        game_loop()

        # Capturar la pantalla y mostrarla en Streamlit
        img = capture_screen()
        st.image(img, caption="Pozo de Pelotas", use_column_width=True)

        # Control de FPS
        pygame.time.Clock().tick(FPS)
    else:
        st.write("La animación está pausada. Haz clic en 'Iniciar' para continuar.")

if __name__ == "__main__":
    main()