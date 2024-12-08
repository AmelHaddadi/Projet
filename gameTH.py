import pygame
import random
from unitTH import Soldier, Archer, Tank  # Importer les nouvelles classes d'unités

# Constantes
WIDTH = 480  # Largeur de l'écran
HEIGHT = 480  # Hauteur de l'écran
CELL_SIZE = 60  # Taille des cellules de la grille
FPS = 30  # Fréquence de rafraîchissement de l'écran
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)  # Couleur du texte
FONT_SIZE = 20  # Taille de la police

class Game:
    """
    Classe pour représenter le jeu.

    Attributs :
    -----------
    screen : pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
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
        self.font = pygame.font.SysFont("Arial", FONT_SIZE)  # Police pour afficher les caractéristiques
        # Création des unités avec différents types
        self.player_units = [Soldier(0, 0, 'player'), Archer(1, 0, 'player'), Tank(2, 0, 'player')]
        self.enemy_units = [Soldier(6, 6, 'enemy'), Archer(7, 6, 'enemy'), Tank(8, 6, 'enemy')]

    def handle_player_turn(self):
        """Tour du joueur."""
        for selected_unit in self.player_units:

            has_acted = False
            selected_unit.is_selected = True
            self.flip_display(selected_unit)

            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        selected_unit.move(dx, dy)
                        self.flip_display(selected_unit)

                        if event.key == pygame.K_SPACE:
                            # Attaque de l'unité
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)

                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:
            target = random.choice(self.player_units)  # L'ennemi choisit une unité aléatoire du joueur

            # Déplacement vers l'unité cible
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

    def flip_display(self, selected_unit):
        """Affiche le jeu et les caractéristiques de l'unité sélectionnée."""
        self.screen.fill(BLACK)

        # Afficher la grille
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Afficher les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Afficher les caractéristiques de l'unité sélectionnée
        if selected_unit:
            self.display_unit_info(selected_unit)

        # Rafraîchir l'écran
        pygame.display.flip()

    def display_unit_info(self, unit):
        """Affiche les caractéristiques de l'unité sélectionnée."""
        info_text = f"Unité: {unit.name} | PV: {unit.health}/{unit.max_health} | " \
                    f"Attaque: {unit.attack_power} | Défense: {unit.defense} | Vitesse: {unit.speed}"
        text_surface = self.font.render(info_text, True, TEXT_COLOR)
        self.screen.blit(text_surface, (10, HEIGHT - 30))  # Positionner le texte en bas de l'écran

    def check_game_over(self):
        """Vérifie si le jeu est terminé"""
        if len(self.player_units) == 0:
            print("Le joueur a perdu !")
            return True
        if len(self.enemy_units) == 0:
            print("L'ennemi a perdu !")
            return True
        return False

def main():
    """Fonction principale du jeu."""

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
        if game.check_game_over():
            break  # Fin de la boucle si la partie est terminée
        game.handle_enemy_turn()
        if game.check_game_over():
            break  # Fin de la boucle si la partie est terminée

if __name__ == "__main__":
    main()
