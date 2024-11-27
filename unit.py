import pygame          #pygame est utilisée pour gérer l'interface graphique
import random          #random pour ajouter de l'alétoire
from competence import Competence 
# Constantes
GRID_SIZE = 8          #Taille de la grille
CELL_SIZE = 60         #T'aille d'une case en pixel
WIDTH = GRID_SIZE * CELL_SIZE       #Width et Height représentent les dimensions de la fenetre du jeu
HEIGHT = GRID_SIZE * CELL_SIZE
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

    def __init__(self, x, y, health, attack_power, team):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
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
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.competences = []  # Liste des compétences de l'unité

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:   #Verfier si la case choisie est toujours dans la grille
            self.x += dx
            self.y += dy

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
    def ajouter_competence(self, competence):
        """Ajoute une compétence à l'unité."""
        self.competences.append(competence)

    def utiliser_competence(self, competence_nom, cible):
        """Utilise une compétence spécifique sur une cible."""
        competence = next((c for c in self.competences if c.nom == competence_nom), None)
        if competence:
            competence.utiliser(self, cible)
        else:
            print(f"{self.nom} ne possède pas la compétence {competence_nom}.")




