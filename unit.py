import pygame
import random
from competence import Competence  # Assurez-vous d'importer la classe Competence

# Constantes
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Unit:
    def __init__(self, x, y, health, attack_power, team, nom="Unité", vitesse=3, etats=None):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.nom = nom
        self.vitesse = vitesse
        self.is_selected = False
        self.competences = []  # Liste des compétences de l'unité vide par défaut
        self.etats = etats if etats else []  # Liste des états de l'unité (par exemple, 'empoisonné')

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if abs(dx) + abs(dy) > self.vitesse:
            print(f"{self.nom} ne peut pas se déplacer de plus de {self.vitesse} cases par tour.")
            return
        
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy
            print(f"{self.nom} s'est déplacé vers ({self.x}, {self.y}).")
        else:
            print(f"{self.nom} ne peut pas sortir de la grille.")
            
    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.take_damage(self.attack_power)

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

        # Afficher la barre de santé
        pygame.draw.rect(screen, RED, (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, CELL_SIZE, 5))
        current_health_width = int(CELL_SIZE * self.health / 100)
        pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, current_health_width, 5))

    def take_damage(self, amount):
        """Réduit la santé de l'unité."""
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print(f"{self.nom} est mort.")
        else:
            print(f"{self.nom} subit {amount} dégâts, santé actuelle : {self.health}.")

    def heal(self, amount):
        """Soigne l'unité en ajoutant des points de vie."""
        self.health += amount
        if self.health > 100:
            self.health = 100
        print(f"{self.nom} a été soigné de {amount} PV. Santé actuelle : {self.health} PV.")

    def ajouter_competence(self, competence):
        """Ajoute une compétence à l'unité."""
        self.competences.append(competence)

    def utiliser_competence(self, competence, cible, mode=None):
        """Utilise une compétence sur une cible avec un mode spécifique."""
        if not self.competences:
            print(f"{self.nom} n'a pas de compétences.")
            return

        # Si le mode est appliqué, il affecte l'effet de la compétence
        if mode:
            print(f"Le mode {mode} est appliqué à la compétence {competence.nom}.")

        # Vérifier la portée de la compétence et appliquer les effets supplémentaires du mode
        distance = abs(self.x - cible.x) + abs(self.y - cible.y)
        if distance > competence.portee:
            print(f"{cible.nom} est hors de portée.")
            return

        if mode:
            # Applique des effets spéciaux selon le mode (feu, vent, etc.)
            if mode == "feu":
                competence.effet = "brulure"
                print(f"{self.nom} utilise {competence.nom} avec effet de brûlure!")
            elif mode == "vent":
                competence.effet = "ralentissement"
                print(f"{self.nom} utilise {competence.nom} avec effet de ralentissement!")

        # Utiliser la compétence normalement
        competence.utiliser(self, cible)

    def afficher_menu_competences(self):
        """Affiche les compétences disponibles."""
        # À implémenter selon l'interface graphique
        pass









