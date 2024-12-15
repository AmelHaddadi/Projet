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
    def __init__(self, screen,mode,selected_characters):
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
         # Initialisation des unités pour le joueur
        CHARACTER_SPEEDS = {
        "tireur": 1,
        "tueur": 2,
        "tank": 2,
        "sorcier": 1,
        }

        # Création des unités du joueur en utilisant PlayerUnit
        self.player_units = [
            PlayerUnit(0, i, 100, 2, char_name, vitesse=CHARACTER_SPEEDS[char_name], image_path=f"{char_name}.png")
            for i, char_name in enumerate(selected_characters)
        ]

        # Création des unités ennemies en utilisant EnemyUnit
        all_characters = ["tireur", "tueur", "tank", "sorcier"]
        enemy_characters = random.sample(all_characters, 3)
        self.enemy_units = [
            EnemyUnit(7, i, 100, 1, char_name, vitesse=CHARACTER_SPEEDS[char_name], image_path=f"{char_name}_enemy.png")
            for i, char_name in enumerate(enemy_characters)
        ]


        # Initialisation des gestionnaires
        colors = {'white': WHITE, 'black': BLACK, 'red': RED, 'green': GREEN, 'blue': BLUE}
        dimensions = {'width': WIDTH, 'height': HEIGHT}
        self.animation_manager = AnimationManager(screen, colors, dimensions, CELL_SIZE)
        self.menu_manager = MenuManager(screen, self.font, colors, dimensions)

        # Ajouter les compétences
        self.ajouter_competences()
         # Initialisation des gestionnaires
        self.competence_manager = CompetenceManager()  # Initialisation de CompetenceManager


        # Ajout des obstacles
        self.obstacles = [(3,3),(5,5),(2,6),(1,5),(2,4),(4,5),(9,2),(12,5),(12,4),(8,2),(10,10),(11,11),(1,6),(2,6),(1,7),(2,7),(0,3),(5,1)]  # Exemple d'obstacles à des coordonnées spécifiques

    def is_occupied(self, units, x, y):
        """Vérifie si une case est occupée par une unité ou un obstacle."""
        # Vérifier si la case est un obstacle
        if (x, y) in self.obstacles:
            return True

        # Vérifier si la case est occupée par une autre unité
        for unit in units:
            if unit.x == x and unit.y == y:
                return True
        return False

        
    def ajouter_competences(self):
        """Ajoute des compétences aux unités sélectionnées et aux ennemis."""
        # Définir des compétences communes
        pistolet = Competence("Pistolet", degats=20, portee=5, effet="blessure")
        grenade = Competence("Grenade", degats=50, portee=3, effet="explosion")
        dague = Competence("Dague", degats=30, portee=1, effet="saignement")
        baton_magique = Competence("Baton magique", degats=40, portee=4, effet="soin")

        # Ajout de compétences aux unités du joueur
        for unit in self.player_units:
            if unit.nom == "tueur":
                unit.ajouter_competence(pistolet)
                unit.ajouter_competence(grenade)
            elif unit.nom == "tireur":
                unit.ajouter_competence(pistolet)
                unit.ajouter_competence(dague)
            elif unit.nom == "sorcier":
                unit.ajouter_competence(pistolet)
                unit.ajouter_competence(baton_magique)
            elif unit.nom == "tank":
                unit.ajouter_competence(pistolet)
                
        # Ajout de compétences aux ennemis
        for unit in self.enemy_units:
            if unit.nom == "tueur":
                unit.ajouter_competence(pistolet)
                unit.ajouter_competence(grenade)
            elif unit.nom == "tireur":
                unit.ajouter_competence(pistolet)
                unit.ajouter_competence(dague)
            elif unit.nom == "sorcier":
                unit.ajouter_competence(pistolet)
                unit.ajouter_competence(baton_magique)
            elif unit.nom == "tank":
                unit.ajouter_competence(pistolet)

    def utiliser_competence(self, selected_unit):
        """Permet au joueur d'utiliser une compétence."""
        # Vérifier si l'unité a des compétences
        if not selected_unit.competences:
            print(f"{selected_unit.nom} n'a pas de compétences.")
            return False

        # Afficher le menu des compétences
        competence = self.menu_manager.selectionner_competence(selected_unit.competences)
        if not competence:  # Si le joueur annule
            print("Action annulée.")
            self.flip_display(active_unit=selected_unit)  # Réinitialiser l'affichage
            return False

        print(f"Compétence sélectionnée : {competence.nom}")  # Debug

        # Déterminer les cibles valides
        if competence.effet == "soin":      #Cette compétence ne peut etre appliquée que sur les coéquipiers : baton magique
            cibles = [unit for unit in self.player_units if unit != selected_unit]
        else:
            cibles = self.enemy_units

        # Afficher le menu des cibles
        cible = self.menu_manager.afficher_menu_cibles(cibles)
        if not cible:
            print("Action annulée.")
            return False

        # Jouer l'animation et appliquer la compétence
        if competence.effet == "soin":
            self.animation_manager.animer_soin(cible.x, cible.y)
        else:
            self.animation_manager.animer_attaque(cible.x, cible.y)

        self.competence_manager.utiliser_competence(competence, selected_unit, cible)

        # Ajout du son de l'explosion lorsqu'il s'agit de l'utilisation de grenade
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
        return True
    def handle_player_turn(self):
        """Tour du joueur."""
        print("Tour des joueurs")  # Debug
        for selected_unit in self.player_units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display(active_unit=selected_unit)

            move_attempted = False  # Flag pour vérifier si un déplacement a eu lieu
            ability_used = False  # Flag pour vérifier si une compétence a été utilisée

            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            # Vérifier si l'ennemi est dans le champ de vision
                            if selected_unit.est_dans_vision(self.enemy_units[0]):  # Assumer que l'ennemi est sélectionné
                                action_result = self.utiliser_competence(selected_unit)
                                if action_result:
                                    ability_used = True  # Indique qu'une compétence a été utilisée
                                    has_acted = True
                                    selected_unit.is_selected = False
                            else:
                                print(f"{selected_unit.nom} ne peut pas utiliser une compétence car l'ennemi n'est pas dans le champ de vision.")
                                # Le joueur peut se déplacer encore une fois avant que le tour passe
                                if not move_attempted:
                                    print(f"{selected_unit.nom} peut se déplacer une fois.")
                                    move_attempted = True  # Première tentative de déplacement
                                else:
                                    print(f"{selected_unit.nom} ne peut plus agir, le tour passe.")
                                    has_acted = True  # Le tour passe après le déplacement
                        elif event.key == pygame.K_s:  #  utiliser une capacité spéciale 
                            selected_unit.special_ability()
                        elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                            dx, dy = 0, 0
                            if event.key == pygame.K_LEFT:
                                dx = -selected_unit.vitesse
                            elif event.key == pygame.K_RIGHT:
                                dx = selected_unit.vitesse
                            elif event.key == pygame.K_UP:
                                dy = -selected_unit.vitesse
                            elif event.key == pygame.K_DOWN:
                                dy = selected_unit.vitesse

                            # Vérification du déplacement
                            if abs(dx) > selected_unit.vitesse or abs(dy) > selected_unit.vitesse:
                                print(f"{selected_unit.nom} ne peut pas se déplacer de plus de {selected_unit.vitesse} cases par tour.")
                            else:
                                # Vérifier que la case cible n'est pas occupée par un obstacle ou une autre unité
                                selected_unit.move(dx, dy, self.player_units + self.enemy_units)  # Vérifier l'occupation avec toutes les unités
                                self.flip_display(active_unit=selected_unit)
                                move_attempted = True  # Le joueur a effectué un déplacement
                                has_acted = True  # Le tour passe après le déplacement

            # Marquez la fin de l'action de cette unité
            selected_unit.is_selected = False
    def handle_enemy_turn(self):
        """Tour des ennemis."""
        print("Début du tour des ennemis")

        for enemy in self.enemy_units:
            # Vérifier si le jeu est terminé
            self.check_end_game()

            # Choisir une cible parmi les joueurs
            target = random.choice(self.player_units)  # Choisir une cible aléatoire parmi les unités des joueurs

            # Vérifier si la cible est à portée d'attaque directe
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                # Attaquer directement si la cible est à portée
                print(f"{enemy.nom} attaque directement {target.nom}")
                enemy.attack(target)

                # Vérifier si la cible a été éliminée
                if target.health <= 0:
                    print(f"{target.nom} a été éliminé par {enemy.nom}.")
                    self.player_units.remove(target)
                continue  # Passer au prochain ennemi

            # Calculer le déplacement si l'attaque directe n'est pas possible
            dx = (1 if enemy.x < target.x else -1 if enemy.x > target.x else 0)
            dy = (1 if enemy.y < target.y else -1 if enemy.y > target.y else 0)

            # Limiter le déplacement par la vitesse de l'ennemi
            dx = max(-enemy.vitesse, min(dx, enemy.vitesse))
            dy = max(-enemy.vitesse, min(dy, enemy.vitesse))

            # Vérifier si la case cible est occupée ou un obstacle
            new_x, new_y = enemy.x + dx, enemy.y + dy
            if self.is_occupied(self.player_units + self.enemy_units, new_x, new_y):
                print(f"Case ({new_x}, {new_y}) est occupée ou un obstacle. {enemy.nom} ne peut pas se déplacer.")
                continue  # Passer au prochain ennemi

            # Déplacer l'ennemi
            enemy.move(dx, dy, self.player_units + self.enemy_units)
            self.flip_display()  # Mettre à jour l'affichage après déplacement

            # Vérifier si une attaque ou une compétence peut être utilisée après le déplacement
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                competence = random.choice(enemy.competences) if enemy.competences else None
                if competence:
                    print(f"{enemy.nom} utilise {competence.nom} sur {target.nom}")
                    self.animation_manager.animer_attaque(target.x, target.y)
                    self.competence_manager.utiliser_competence(competence, enemy, target)
                else:
                    enemy.attack(target)

                # Vérifier si la cible a été éliminée
                if target.health <= 0:
                    print(f"{target.nom} a été éliminé par {enemy.nom}.")
                    self.player_units.remove(target)

        # Mettre à jour l'affichage après le tour des ennemis
        self.flip_display()

    def dessiner_grille(self):
    #"""Dessine une grille sur l'écran, avec des obstacles en gris."""
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                # Vérifier si la case contient un obstacle
                if (x // CELL_SIZE, y // CELL_SIZE) in obstacles:
                    pygame.draw.rect(self.screen, (169, 169, 169), pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))  # Gris pour les obstacles
                else:
                    pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), 1)  # Grille normale

    def flip_display(self, active_unit=None):
        """Met à jour l'affichage du jeu, en mettant en évidence l'unité active."""
        if self.current_background:
            self.screen.blit(self.current_background, (0, 0))  # Dessiner l'arrière-plan
        else:
            self.screen.fill((0, 0, 0))  # Fond noir si aucun arrière-plan

        self.dessiner_grille()  # Dessiner la grille


        

        # Dessiner les unités et leur champ de vision uniquement pour l'unité active
        for unit in self.player_units + self.enemy_units:
            # Afficher le champ de vision uniquement pour l'unité active
            if unit == active_unit:
                unit.draw_vision(self.screen)  # Dessiner le champ de vision de l'unité active
            is_active = (unit == active_unit)  # Marquer l'unité active
            unit.draw(self.screen, is_active=is_active)  # Dessiner l'unité


             # Si l'unité est un joueur, afficher le nombre d'utilisations restantes
            if isinstance(unit, PlayerUnit):  # Vérifie si l'unité est une unité de type PlayerUnit
                unit.draw_special_uses(self.screen)  # Affiche les utilisations restantes des capacités spéciales

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
        """Réinitialise complètement le jeu en retournant au menu de sélection."""
        # Appeler le menu de sélection pour recommencer
        selected_characters, mode = afficher_menu_selection()
    
        # Mettre à jour les unités du joueur et le mode
        self.mode = mode
        self.current_background = self.backgrounds.get(self.mode, None)
        if self.current_background:
            self.current_background = pygame.transform.scale(self.current_background, (WIDTH, HEIGHT))
    
        # Réinitialiser les unités sélectionnées
        CHARACTER_SPEEDS = {
        "tireur": 1,
        "tueur": 2,
        "tank": 2,
        "sorcier": 1,
        }
                # Création des unités du joueur en utilisant PlayerUnit
        self.player_units = [
            PlayerUnit(0, i, 100, 2, char_name, vitesse=CHARACTER_SPEEDS[char_name], image_path=f"{char_name}.png")
            for i, char_name in enumerate(selected_characters)
        ]

        # Création des unités ennemies en utilisant EnemyUnit
        all_characters = ["tireur", "tueur", "tank", "sorcier"]
        enemy_characters = random.sample(all_characters, 3)
        self.enemy_units = [
            EnemyUnit(7, i, 100, 1, char_name, vitesse=CHARACTER_SPEEDS[char_name], image_path=f"{char_name}_enemy.png")
            for i, char_name in enumerate(enemy_characters)
        ]

        # Réinitialiser les compétences
        self.ajouter_competences()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    personnages, mode = afficher_menu_selection()
    game = Game(screen, mode, personnages)

    player_turn = True  # Alternance entre joueurs et ennemis

    while True:
        if player_turn:
            game.handle_player_turn()
        else:
            game.handle_enemy_turn()

        player_turn = not player_turn  # Alterner les tours
if __name__ == "__main__":
    main()
