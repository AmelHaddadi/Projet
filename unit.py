import pygame          #pygame est utilisée pour gérer l'interface graphique
import random          #random pour ajouter de l'alétoire
from competence import Competence   #Gérer les compétences de chaque unité
# Constantes
GRID_SIZE = 8          #Taille de la grille
CELL_SIZE = 60         #Taille d'une case en pixel
WIDTH = GRID_SIZE * CELL_SIZE       #Largeur totale de la fenetre en pixcel
HEIGHT = GRID_SIZE * CELL_SIZE      #Hauteur totale de la fenetre en pixcel
FPS = 30                 #Nombre d'images par seconde
#Couleurs :    # 0 aucune intensité et 255 pour pleine intensité modèle (R,G,B), qui combinent trois couleurs 
WHITE = (255, 255, 255)    #Rouge, Vert, et Bleu sont à 255, donc toutes les couleurs sont maximales, ce qui donne blanc.   
BLACK = (0, 0, 0)     #Rouge, Vert, et Bleu sont à 0, donc aucune lumière, ce qui donne noir.
RED = (255, 0, 0)   #Seul le rouge est à pleine intensité, le vert et le bleu sont à zéro. La couleur est donc rouge pur.
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Unit:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
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
    """

    def __init__(self, x, y, health, attack_power, team, nom="Unité",vitesse=3,etats=None):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.nom= nom
        self.vitesse= vitesse
        self.is_selected = False
        self.competences = []  # Liste des compétences de l'unité vide par défaut
        self.etats = []  # Liste des états de l'unité (par exemple, 'empoisonné')


    def move(self, dx, dy):
        """
        Déplace l'unité de dx, dy, en respectant sa vitesse.

        Paramètres:
        ----------
        dx : int
            Déplacement horizontal.
        dy : int
            Déplacement vertical.
        """
        if abs(dx) + abs(dy) > self.vitesse:
            print(f"{self.nom} ne peut pas se déplacer de plus de {self.vitesse} cases par tour.")
            return
        
        # Vérifie que le déplacement reste dans la grille
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy
            print(f"{self.nom} s'est déplacé vers ({self.x}, {self.y}).")
        else:
            print(f"{self.nom} ne peut pas sortir de la grille.")
        

            
    def attack(self, target):
        """Attaque une unité cible."""    #cible adjacente au plus 1 case
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:  #Cette condition vérifie si une unité (l'attaquant) est suffisamment proche d'une autre unité (la cible) pour l'attaquer.
            target.health -= self.attack_power    #target représente l'ennemi , la santé (health) de la cible est réduite en fonction de la puissance d'attaque (attack_power) de l'attaquant.

    def draw(self, screen):      #Cette méthode utilise les fonctionnalités de pygame afin de dessiner une unité sur la grille
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED   #unité bleu pour le joueur et rouge pour l'ennemi
        if self.is_selected:     #unité sélectionnée
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,           #CELL_SIZE : taille du rectangle en pixels (largeur et hauteur)
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))    #rectangle vert est dessiné autour de la case où se trouve l'unité
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //  #l'unité est représenté par un cercle au centre de la case
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)  #CELL_SIZE/3 reprèsente le rayon du cercle
        #Amelioration :
        """ Ajouter une barre de santé au-dessus de l'unité"""
        # Position et taille de la barre rouge (fond de la barre)
        pygame.draw.rect(screen, RED, 
                        (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, CELL_SIZE, 5)) #self.x * CELL_SIZE : La barre commence horizontalement au début de la case.
        #self.y * CELL_SIZE - 10 : La barre est placée au-dessus de l'unité (10 pixels au-dessus du bord supérieur de la case).
    
        # Position et taille de la barre verte (santé restante)
        current_health_width = int(CELL_SIZE * self.health / 100)  # Ajuster la largeur en fonction des PV
        pygame.draw.rect(screen, GREEN, 
                        (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, current_health_width, 5))
      #Competences des unités

    def take_damage(self, amount):
        """
        Réduit la santé de l'unité en fonction des dégâts reçus.

        Paramètres:
        ----------
        amount : int
            Les dégâts infligés à l'unité.
        """
        self.health -= amount  # Réduit les points de vie
        if self.health <= 0:
            self.health = 0
            print(f"{self.nom} est mort et sera retiré du jeu.")
            self.is_active = False
        else:
            print(f"{self.nom} subit {amount} dégâts, santé actuelle : {self.health}.")

    def heal(self, amount):
        """
        Soigne l'unité en ajoutant des points de vie.

        :param amount: Montant des points de vie à ajouter.
        """
        self.health += amount
        # Empêcher la santé de dépasser un maximum, si nécessaire (par exemple, 100 PV max)
        if self.health > 100:
            self.health = 100
        print(f"{self.nom} a été soigné de {amount} PV. Santé actuelle : {self.health} PV.")

    def ajouter_competence(self, competence):
        """Ajoute une compétence à l'unité."""
        self.competences.append(competence)

    def utiliser_competence(self, selected_unit):
        """
        Permet au joueur d'utiliser une compétence via une interface graphique avec animation.
        """
        if not selected_unit.competences:
            print(f"{selected_unit.nom} n'a pas de compétences.")
            return

        # Affiche le menu des compétences et récupère la compétence choisie
        competence = self.afficher_menu_competences(selected_unit)
        if not competence:
            print("Action annulée.")
            return

        # Filtrer les cibles disponibles selon le type de compétence
        if competence.effet == "soin":
            # Afficher uniquement les coéquipiers (alliés), sauf l'unité sélectionnée
            cibles = [unit for unit in self.player_units if unit != selected_unit]
        else:
            # Afficher uniquement les ennemis
            cibles = self.enemy_units

        # Vérifier s'il existe des cibles valides
        print(f"Cibles disponibles pour {competence.nom} : {[c.nom for c in cibles]}")
        if not cibles:
            print(f"Aucune cible valide pour la compétence {competence.nom}.")
            return

        # Afficher le menu de sélection des cibles
        print("Affichage du menu de cibles...")
        cible = self.afficher_menu_cibles(cibles)
        if not cible:
            print("Action annulée.")
            return

        # Utiliser la compétence
        print(f"{selected_unit.nom} utilise {competence.nom} sur {cible.nom}.")
        competence.utiliser(selected_unit, cible)










