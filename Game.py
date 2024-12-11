import pygame
import random
from unit import *
from competence import Competence
from AnimationManager import AnimationManager
from CompetenceManager import CompetenceManager
from MenuManager import MenuManager
from MenuSelection import *

# Constantes
WIDTH, HEIGHT = 1000, 700  # Dimensions de la fenêtre
GRID_SIZE = 8  # Taille de la grille
CELL_SIZE = 60  # Taille d'une cellule
WHITE, BLACK, RED, GREEN, BLUE = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)

pygame.mixer.init()

# Charger un son d'explosion
try:
     explosion_sound = pygame.mixer.Sound("explosion.wav")  
except pygame.error as e:
    print("Erreur lors du chargement du son :", e)
    explosion_sound = None  # Si le son ne peut pas être chargé, on continue sans

class Game:
    """
    Classe pour représenter le jeu.
    """
    def __init__(self, screen,mode):
        """
        Construit le jeu avec la surface de la fenêtre.

        :param screen: Surface Pygame où le jeu est affiché.
        """
        self.screen = screen
        self.mode = mode  # Mode sélectionné transmis
        self.backgrounds = {
            "air": pygame.image.load("air.png"),
            "terre": pygame.image.load("terre.png"),
            "feu": pygame.image.load("feu.png"),
            "electricite": pygame.image.load("electricite.png"),
        }
        self.current_background = self.backgrounds.get(self.mode, None)
        if self.current_background is not None:
            self.current_background = pygame.transform.scale(self.current_background, (WIDTH, HEIGHT))
        else:
            print(f"Erreur : Aucun arrière-plan trouvé pour le mode {self.mode}")

        self.font = pygame.font.Font(None, 36)

        # Initialisation des unités
        self.player_units = [Unit(0, 0, 100, 2, 'player', 'tueur', 4,image_path="tueur.png"),
                             Unit(1, 0, 100, 2, 'player', 'tireur', 2,image_path="tireur.png"),
                             Unit(2, 0, 100, 2, 'player', 'sorcier', 4,image_path="sorcier.png"),
                             Unit(3, 0, 100, 2, 'player', 'tank', 4,image_path="tank.png")]
        self.enemy_units = [Unit(6, 6, 100, 1, 'enemy', 'tueur_enemy', 4,image_path="tueur_enemy.png"),
                            Unit(7, 6, 100, 1, 'enemy', 'tireur_enemy', 4,image_path="tireur_enemy.png"),
                            Unit(8, 6, 100, 1, 'enemy', 'sorcier_enemy', 4,image_path="sorcier_enemy.png"),
                            Unit(7, 7, 100, 1, 'enemy', 'tank_enemy', 4,image_path="tank_enemy.png")]

        # Initialisation des gestionnaires
        colors = {'white': WHITE, 'black': BLACK, 'red': RED, 'green': GREEN, 'blue': BLUE}
        dimensions = {'width': WIDTH, 'height': HEIGHT}

        self.animation_manager = AnimationManager(screen, colors, dimensions, CELL_SIZE)
        self.menu_manager = MenuManager(screen, self.font, colors, dimensions)
        #self.competence_manager = CompetenceManager()

        # Ajout de compétences
        self.ajouter_competences()
         # Initialisation des gestionnaires
        self.competence_manager = CompetenceManager()  # Initialisation de CompetenceManager
        
    def ajouter_competences(self):
        """Ajoute des compétences aux unités."""
        pistolet = Competence("Pistolet", degats=20, portee=5, effet="blessure")
        grenade = Competence("Grenade", degats=50, portee=3, effet="explosion")
        dague = Competence("Dague", degats=30, portee=1, effet="saignement")
        bouclier = Competence("Bouclier", degats=0, portee=1, effet="blocage")
        baton_magique = Competence("Baton magique", degats=40, portee=4, effet="soin")

        self.player_units[0].ajouter_competence(pistolet)  # Unité tueur
        self.player_units[0].ajouter_competence(grenade)  # Unité tueur
        self.player_units[1].ajouter_competence(pistolet)  # Unité tireur
        self.player_units[1].ajouter_competence(dague)  # Unité tireur
        self.player_units[2].ajouter_competence(pistolet)  # Unité sorcier
        self.player_units[2].ajouter_competence(baton_magique)  # Unité sorcier
        self.player_units[3].ajouter_competence(pistolet)  # Unité tank
        self.player_units[3].ajouter_competence(bouclier)  # Unité tank
       
        self.enemy_units[0].ajouter_competence(pistolet)  # Unité tueur
        self.enemy_units[0].ajouter_competence(grenade)  # Unité tueur
        self.enemy_units[1].ajouter_competence(pistolet)  # Unité tireur
        self.enemy_units[1].ajouter_competence(dague)  # Unité tireur
        self.enemy_units[2].ajouter_competence(pistolet)  # Unité sorcier
        self.enemy_units[2].ajouter_competence(baton_magique)  # Unité sorcier
        self.enemy_units[3].ajouter_competence(pistolet)  # Unité tank
        self.enemy_units[3].ajouter_competence(bouclier)  # Unité tank
        
    def activer_bouclier(self, tank):
        """Active automatiquement l'effet Bouclier pour le Tank."""
        if "blocage" not in tank.etats:
            tank.etats.append("blocage")
            print(f"{tank.nom} active Bouclier : réduction automatique des dégâts.")


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

        # Ajouter ici l'appel au son d'explosion si la compétence est "Boule de Feu"
        if competence.nom == "grenade" and explosion_sound:
            explosion_sound.play()  # Joue le son d'explosion

        # Vérifier si la cible est éliminée
        if cible.health <= 0:
            if cible.team == 'enemy':
                self.enemy_units.remove(cible)
            else:
                self.player_units.remove(cible)
        #Verifier si le jeu est terminé
        self.check_end_game()
    def handle_player_turn(self):
        """Tour du joueur."""
        for selected_unit in self.player_units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display(active_unit=selected_unit)  # Mettre en évidence l'unité active

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
                            #Verifier si le jeu est terminé
                            self.check_end_game()
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
                            self.flip_display(active_unit=selected_unit)  # Mettre à jour l'affichage
                            has_acted = True
                            #Verifier si le jeu est terminé
                            self.check_end_game()


    def handle_enemy_turn(self):
        """Tour des ennemis."""
        for enemy in self.enemy_units:
            #Verifier si le jeu est terminé
            self.check_end_game()
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
    def dessiner_grille(self):
        """Dessine une grille sur l'écran."""
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (200, 200, 200), (x, 0), (x, HEIGHT), 1)  # Lignes verticales
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (200, 200, 200), (0, y), (WIDTH, y), 1)  # Lignes horizontales

    def flip_display(self, active_unit=None):
        """Met à jour l'affichage du jeu, en mettant en évidence l'unité active."""
        if self.current_background:
            self.screen.blit(self.current_background, (0, 0))  # Dessiner l'arrière-plan
        else:
            self.screen.fill((0, 0, 0))  # Fond noir si aucun arrière-plan

        self.dessiner_grille()  # Dessiner la grille

        # Afficher toutes les unités
        for unit in self.player_units + self.enemy_units:
            is_active = (unit == active_unit)  # L'unité active est celle en cours de jeu
            unit.draw(self.screen, is_active=is_active)

        pygame.display.flip()




    def check_end_game(self):

        """Vérifie si le jeu est terminé (victoire ou défaite)."""
        if not self.enemy_units:  # Si tous les ennemis sont éliminés
            action = self.afficher_interface_fin("victoire")
            if action == "rejouer":
                self.reinitialiser_jeu()
        elif not self.player_units:  # Si tous les joueurs sont éliminés
            action = self.afficher_interface_fin("echec")
            if action == "rejouer":
                self.reinitialiser_jeu()

    def afficher_message_fin(self, message):
        """Affiche un message de fin du jeu (Victoire ou Défaite)."""
        self.screen.fill((0, 0, 0))  # Fond noir
        font = pygame.font.Font(None, 72)  # Police plus grande pour le message
        texte = font.render(message, True, (255, 255, 255))  # Texte blanc
        texte_rect = texte.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(texte, texte_rect)
        pygame.display.flip()
        pygame.time.wait(3000)  # Attendre 3 secondes avant de fermer

    def afficher_interface_fin(self, resultat):
        """
        Affiche l'interface de fin avec un bouton pour rejouer ou quitter.
        :param resultat: "victoire" ou "echec"
        """
        # Charger l'image correspondante
        image_path = "victoire.png" if resultat == "victoire" else "defaite.png"
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (self.screen.get_width(), self.screen.get_height()))
    
        # Boucle pour l'interface de fin
        while True:
            self.screen.blit(image, (0, 0))

            # Afficher les boutons
            font = pygame.font.Font(None, 50)
            rejouer_texte = font.render("Rejouer", True, (255, 255, 255))
            quitter_texte = font.render("Quitter", True, (255, 255, 255))

            # Dimensions des boutons
            button_width, button_height = 200, 50
            replay_button_rect = pygame.Rect(
                self.screen.get_width() // 2 - button_width // 2,
                self.screen.get_height() // 2,
                button_width,
                button_height
            )
            quit_button_rect = pygame.Rect(
                self.screen.get_width() // 2 - button_width // 2,
                self.screen.get_height() // 2 + 70,
                button_width,
                button_height
            )

            # Dessiner les boutons
            pygame.draw.rect(self.screen, (0, 128, 0), replay_button_rect)
            pygame.draw.rect(self.screen, (128, 0, 0), quit_button_rect)

            self.screen.blit(rejouer_texte, (replay_button_rect.x + 50, replay_button_rect.y + 10))
            self.screen.blit(quitter_texte, (quit_button_rect.x + 50, quit_button_rect.y + 10))

            pygame.display.flip()

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay_button_rect.collidepoint(event.pos):
                        return "rejouer"
                    elif quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        exit()
    def reinitialiser_jeu(self):
        """Réinitialise le jeu en recréant les unités et réinitialisant l'état."""
        self.player_units = [
            Unit(0, 0, 100, 2, 'player', 'tueur', 4, image_path="tueur.png"),
            Unit(1, 0, 100, 2, 'player', 'tireur', 2, image_path="tireur.png"),
            Unit(2, 0, 100, 2, 'player', 'sorcier', 4, image_path="sorcier.png"),
            Unit(3, 0, 100, 2, 'player', 'tank', 4, image_path="tank.png")
            ]
        self.enemy_units = [
            Unit(6, 6, 100, 1, 'enemy', 'tueur_enemy', 4, image_path="tueur_enemy.png"),
            Unit(7, 6, 100, 1, 'enemy', 'tireur_enemy', 4, image_path="tireur_enemy.png"),
            Unit(8, 6, 100, 1, 'enemy', 'sorcier_enemy', 4, image_path="sorcier_enemy.png"),
            Unit(9, 6, 100, 1, 'enemy', 'tank_enemy', 4, image_path="tank_enemy.png")
        ]
         # Ajout des compétences aux unités
        self.ajouter_competences()

        # Démarrer le tour des joueurs
        self.handle_player_turn()



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Appeler le menu de sélection
    personnages, mode = afficher_menu_selection()
    print(f"Mode sélectionné : {mode}")  # Vérifiez le mode sélectionné dans la console

    # Passer les choix au jeu
    game = Game(screen, mode)

    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()
 



if __name__ == "__main__":
    main()

