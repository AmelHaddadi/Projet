import pygame
import random

from unitbiz import *
from cases import Cell

# Define new dimensions for the grid
GRID_WIDTH = 12
GRID_HEIGHT = 8
CELL_SIZE = 60  # Adjust if needed
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)

# Load teleport image
TELEPORT_IMAGE = pygame.image.load("teleport.jpeg")  # Replace with the correct path
TELEPORT_IMAGE = pygame.transform.scale(TELEPORT_IMAGE, (CELL_SIZE, CELL_SIZE))  # Resize to match grid

# Load fire image
FIRE_IMAGE = pygame.image.load("fire.jpeg")  # Replace with the correct path
FIRE_IMAGE = pygame.transform.scale(FIRE_IMAGE, (CELL_SIZE, CELL_SIZE))  # Resize to match grid


class Game:
    """
    Classe pour représenter le jeu.
    """

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.player_units = [Unit(0, 0, 10, 2, 3, 'player'),
                             Unit(1, 0, 10, 2, 3, 'player')]

        self.enemy_units = [Unit(6, 6, 8, 1, 2, 'enemy'),
                            Unit(7, 6, 8, 1, 2, 'enemy')]

        self.grid = self.create_grid()

    def create_grid(self):
        """Crée une grille avec différents types de cellules."""
        grid = []
        occupied_positions = set()

        # Generate random teleport pairs
        num_teleports = 3  # Adjust the number of teleport pairs as needed
        teleport_pairs = []
        for _ in range(num_teleports):
            while True:
                x1 = random.randint(0, GRID_WIDTH - 1)
                y1 = random.randint(0, GRID_HEIGHT - 1)
                x2 = random.randint(0, GRID_WIDTH - 1)
                y2 = random.randint(0, GRID_HEIGHT - 1)
                if (x1, y1) not in occupied_positions and (x2, y2) not in occupied_positions and (x1, y1) != (x2, y2):
                    teleport_pairs.append(((x1, y1), (x2, y2)))
                    occupied_positions.add((x1, y1))
                    occupied_positions.add((x2, y2))
                    break

        # Generate walls in groups of 3
        num_wall_groups = 7  # Adjust number of wall groups as needed
        for _ in range(num_wall_groups):
            while True:
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                direction = random.choice(['horizontal', 'vertical'])

                # Define wall positions
                if direction == 'horizontal':
                    wall_positions = [(x, y), (x + 1, y), (x + 2, y)]
                else:  # vertical
                    wall_positions = [(x, y), (x, y + 1), (x, y + 2)]

                # Validate wall positions
                if all(
                    0 <= wx < GRID_WIDTH and 0 <= wy < GRID_HEIGHT and (wx, wy) not in occupied_positions
                    for wx, wy in wall_positions
                ):
                    # Ensure walls don't block teleports or units
                    if not any((wx, wy) in [pair[0] for pair in teleport_pairs] + [pair[1] for pair in teleport_pairs]
                               for wx, wy in wall_positions):
                        occupied_positions.update(wall_positions)
                        break

        # Generate fire cells
        num_fire_cells = 5  # Adjust number of fire cells
        fire_cells = []
        for _ in range(num_fire_cells):
            while True:
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                if (x, y) not in occupied_positions:
                    fire_cells.append((x, y))
                    occupied_positions.add((x, y))
                    break

        # Fill the grid
        teleport_cells = {}
        for x in range(GRID_WIDTH):
            row = []
            for y in range(GRID_HEIGHT):
                if (x, y) in occupied_positions:
                    if any((x, y) == pair[0] or (x, y) == pair[1] for pair in teleport_pairs):
                        # Create a teleport cell with an image
                        cell = Cell(x, y, 'teleport', image=TELEPORT_IMAGE)
                        teleport_cells[(x, y)] = cell
                        row.append(cell)
                    elif (x, y) in fire_cells:
                        # Create a fire cell with an image
                        cell = Cell(x, y, 'fire', image=FIRE_IMAGE)
                        row.append(cell)
                    else:
                        # Create a wall
                        row.append(Cell(x, y, 'wall'))
                else:
                    # Create a normal cell
                    row.append(Cell(x, y))
            grid.append(row)

        # Link teleport pairs
        for pair in teleport_pairs:
            cell1 = teleport_cells[pair[0]]
            cell2 = teleport_cells[pair[1]]
            cell1.linked_cell = cell2
            cell2.linked_cell = cell1

        return grid
    
    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:

            # Tant que l'unité n'a pas terminé son tour
            has_acted = False

            # Calcule les cases accessibles une fois au début du tour
            reachable_squares = selected_unit.get_reachable_squares()

            # Ajouter la position actuelle de l'unité comme accessible
            reachable_squares.append((selected_unit.x, selected_unit.y))

            # Empêcher de se déplacer sur d'autres unités, sauf soi-même
            occupied_positions = [
                (u.x, u.y) for u in self.player_units + self.enemy_units if u != selected_unit
            ]
            reachable_squares = [
                (x, y) for x, y in reachable_squares
                if self.grid[x][y].is_walkable() and (x, y) not in occupied_positions
            ]

            while not has_acted:
                # Affiche les cases accessibles au début du tour
                selected_unit.is_selected = True
                self.flip_display(reachable_squares)

                # Gestion des événements Pygame
                for event in pygame.event.get():

                    # Gestion de la fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Gestion des touches du clavier
                    if event.type == pygame.KEYDOWN:

                        # Déplacement (touches fléchées)
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        new_x = selected_unit.x + dx
                        new_y = selected_unit.y + dy

                        # Restreindre le mouvement aux cases accessibles
                        if (new_x, new_y) in reachable_squares:
                            selected_unit.move(dx, dy)

                            # Appliquer les effets de la cellule sur laquelle on entre
                            self.grid[new_x][new_y].on_enter(selected_unit)

                        # Si la touche Espace est pressée, confirmer la téléportation
                        if event.key == pygame.K_SPACE:
                            current_cell = self.grid[selected_unit.x][selected_unit.y]
                            if current_cell.cell_type == 'teleport':
                                current_cell.confirm_teleport(selected_unit)

                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            new_x = enemy.x + dx
            new_y = enemy.y + dy

            occupied_positions = [(u.x, u.y) for u in self.player_units + self.enemy_units]

            if (
                0 <= new_x < GRID_WIDTH
                and 0 <= new_y < GRID_HEIGHT
                and self.grid[new_x][new_y].is_walkable()
                and (new_x, new_y) not in occupied_positions
            ):
                enemy.move(dx, dy)
                self.grid[new_x][new_y].on_enter(enemy)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

    def flip_display(self, reachable_squares=None):
        """Affiche le jeu."""

        # Affiche la grille
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                cell = self.grid[x // CELL_SIZE][y // CELL_SIZE]
                if cell.cell_type == 'wall':
                    pygame.draw.rect(self.screen, (128, 128, 128), rect)
                elif cell.cell_type == 'teleport' and cell.image:
                    self.screen.blit(cell.image, (x, y))
                elif cell.cell_type == 'fire' and cell.image:
                    self.screen.blit(cell.image, (x, y))
                else:
                    pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Affiche les cases accessibles
        if reachable_squares:
            for nx, ny in reachable_squares:
                center_x = nx * CELL_SIZE + CELL_SIZE // 2
                center_y = ny * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(self.screen, LIGHT_BLUE, (center_x, center_y), CELL_SIZE // 4)

        # Affiche les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Rafraîchit l'écran
        pygame.display.flip()


def main():
    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()


if __name__ == "__main__":
    main()
