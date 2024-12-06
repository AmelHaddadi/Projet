import pygame
import random
from unit import *
from competence import Competence
from AnimationManager import AnimationManager
from CompetenceManager import CompetenceManager
from MenuManager import MenuManager

# Constantes
WIDTH, HEIGHT = 800, 600  # Dimensions de la fenêtre
GRID_SIZE = 8  # Taille de la grille
CELL_SIZE = 40  # Taille d'une cellule
WHITE, BLACK, RED, GREEN, BLUE = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)

class Game:
    """
    Classe pour représenter le jeu.
    """
    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        :param screen: Surface Pygame où le jeu est affiché.
        """
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

        # Initialisation des unités
        self.player_units = [Unit(0, 0, 100, 2, 'player', 'guerrier', vitesse=4),
                             Unit(1, 0, 100, 2, 'player', 'arche', vitesse=4)]
        self.enemy_units = [Unit(6, 6, 100, 1, 'enemy', 'guerrier_ennemie', vitesse=4),
                            Unit(7, 6, 100, 1, 'enemy', 'arche_ennemie', vitesse=4)]

        # Initialisation des gestionnaires
        colors = {'white': WHITE, 'black': BLACK, 'red': RED, 'green': GREEN, 'blue': BLUE}
        dimensions = {'width': WIDTH, 'height': HEIGHT}

        self.animation_manager = AnimationManager(screen, colors, dimensions, CELL_SIZE)
        self.menu_manager = MenuManager(screen, self.font, colors, dimensions)
        self.competence_manager = CompetenceManager()

        # Ajout de compétences
        self.ajouter_competences()

    def ajouter_competences(self):
        """Ajoute des compétences aux unités."""
        boule_de_feu = Competence("Boule de Feu", degats=25, portee=3, effet=None)
        soin = Competence("Soin", degats=20, portee=2, effet="soin")
        poison = Competence("Poison", degats=10, portee=2, effet="poison")

        self.player_units[0].ajouter_competence(boule_de_feu)  # Unité guerrier
        self.player_units[1].ajouter_competence(soin)  # Unité arche
        self.enemy_units[0].ajouter_competence(poison)  # Ennemi guerrier
    def utiliser_competence(self, selected_unit):
        """Permet au joueur d'utiliser une compétence."""
        # Vérifier si l'unité a des compétences
        if not selected_unit.competences:
            print(f"{selected_unit.nom} n'a pas de compétences.")
            return

        # Afficher le menu des compétences
        competence = self.menu_manager.selectionner_competence(selected_unit.competences)
        if not competence:  # Si le joueur annule
            print("Action annulée.")
            return

        print(f"Compétence sélectionnée : {competence.nom}")  # Debug

        # Déterminer les cibles valides
        if competence.effet == "soin":
            cibles = [unit for unit in self.player_units if unit != selected_unit]
        else:
            cibles = self.enemy_units

        # Afficher le menu des cibles
        cible = self.menu_manager.afficher_menu_cibles(cibles)
        if not cible:
            print("Action annulée.")
            return

        # Jouer l'animation et appliquer la compétence
        if competence.effet == "soin":
            self.animation_manager.animer_soin(cible.x, cible.y)
        else:
            self.animation_manager.animer_attaque(cible.x, cible.y)

        self.competence_manager.utiliser_competence(competence, selected_unit, cible)

        # Vérifier si la cible est éliminée
        if cible.health <= 0:
            if cible.team == 'enemy':
                self.enemy_units.remove(cible)
            else:
                self.player_units.remove(cible)

    def handle_player_turn(self):
        """Tour du joueur."""
        for selected_unit in self.player_units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()

            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            self.utiliser_competence(selected_unit)
                            has_acted = True
                            selected_unit.is_selected = False
                        elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
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
                            self.flip_display()
                            has_acted = True

    def handle_enemy_turn(self):
        """Tour des ennemis."""
        for enemy in self.enemy_units:
            target = random.choice(self.player_units)
            dx, dy = (1 if enemy.x < target.x else -1 if enemy.x > target.x else 0,
                      1 if enemy.y < target.y else -1 if enemy.y > target.y else 0)
            enemy.move(dx, dy)

            # Utiliser une compétence ou attaquer
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                competence = random.choice(enemy.competences) if enemy.competences else None
                if competence:
                    self.animation_manager.animer_attaque(target.x, target.y)
                    self.competence_manager.utiliser_competence(competence, enemy, target)
                else:
                    enemy.attack(target)

                # Supprimer l'unité si elle est vaincue
                if target.health <= 0:
                    self.player_units.remove(target)
            self.flip_display()

    def flip_display(self):
        """Affiche l'état du jeu."""
        self.screen.fill(WHITE)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.rect(self.screen, BLACK, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), 1)
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)
        pygame.display.flip()

    def check_end_game(self):
        """Vérifie si une équipe a gagné ou perdu."""
        if not self.enemy_units:
            print("Victoire !")
            pygame.quit()
            exit()
        elif not self.player_units:
            print("Défaite !")
            pygame.quit()
            exit()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")
    game = Game(screen)

    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()

if __name__ == "__main__":
    main()
