import pygame
import random

# Constantes
GRID_SIZE = 12
GRID_SIZEX = 12
GRID_SIZEY = 8
CELL_SIZE = 60
WIDTH = GRID_SIZEX * CELL_SIZE
HEIGHT = GRID_SIZEY * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)


class Unit:
    """Classe pour représenter une unité.
        x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    velocity : int
        La portée de mouvement de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    get_reachable_squares()
        Retourne les cases accessibles basées sur la vitesse.
"""
    def __init__(self, x, y, health, attack_power, velocity, team):
        """Construit une unité avec une position, une santé, une puissance d'attaque, une vitesse et une équipe.
                x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        health : int
            La santé de l'unité.
        attack_power : int
            La puissance d'attaque de l'unité.
        velocity : int
            La portée de mouvement de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.velocity = velocity
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZEX and 0 <= self.y + dy < GRID_SIZEY:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def get_reachable_squares(self):
        """Calcule les cases accessibles en fonction de la vitesse."""
        reachable = [(self.x, self.y)]  # Include the current position
        for dx in range(-self.velocity, self.velocity + 1):
            for dy in range(-self.velocity, self.velocity + 1):
                if abs(dx) + abs(dy) <= self.velocity:  # Restriction à une distance Manhattan
                    nx, ny = self.x + dx, self.y + dy
                    if 0 <= nx < GRID_SIZEX and 0 <= ny < GRID_SIZEY:
                        reachable.append((nx, ny))
        return reachable


    def draw(self, screen):
        """Draw the unit on the screen with a health bar."""
        # Define unit color
        color = (0, 0, 255) if self.team == 'player' else (255, 0, 0)  # Blue for player, Red for enemy

    # Draw selection indicator (if selected)
        if self.is_selected:
            pygame.draw.rect(screen, (0, 255, 0), (self.x * CELL_SIZE,
                                               self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

        # Draw the unit as a circle
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE // 2,
                                       self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

        # Draw health bar background (black bar)
        bar_width = CELL_SIZE - 10  # Adjust bar width relative to cell size
        bar_height = 6  # Height of the health bar
        bar_x = self.x * CELL_SIZE + 5  # Offset X position for the bar
        bar_y = self.y * CELL_SIZE + CELL_SIZE - 10  # Offset Y position for the bar
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height))

    # Draw the current health bar (green proportional to health)
        health_ratio = max(self.health / 10, 0)  # Assuming max health is 10
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))



