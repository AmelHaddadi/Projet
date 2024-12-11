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
    def __init__(self, x, y, health, attack_power, team, nom="Unité", vitesse=7, etats=None, image_path=None):
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
        
        # Charger l'image si un chemin est fourni
        self.image = pygame.image.load(image_path) if image_path else None


    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if abs(dx) + abs(dy) > self.vitesse:
            print(f"{self.nom} ne peut pas se déplacer de plus de {self.vitesse} cases par tour.")
            return

        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            self.x = new_x
            self.y = new_y
            print(f"{self.nom} s'est déplacé vers ({self.x}, {self.y}).")
        else:
            print(f"{self.nom} ne peut pas sortir de la grille (position : {self.x}, {self.y}).")

            
    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.take_damage(self.attack_power)

    def draw(self, screen, is_active=False):
        """Affiche l'unité avec son image sur l'écran, et ajoute un contour si l'unité est active."""
        # Dessiner un contour si l'unité est active
        if is_active:
            pygame.draw.rect(
                screen,
                (255, 255, 0),  # Couleur jaune pour l'unité active
                (self.x * CELL_SIZE - 2, self.y * CELL_SIZE - 2, CELL_SIZE + 4, CELL_SIZE + 4),  # Contour autour de l'image
                  #4 Épaisseur du contour
        )

        # Afficher l'image de l'unité
        if self.image:
            image_resized = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
            screen.blit(image_resized, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        else:
            color = (0, 0, 255) if self.team == 'player' else (255, 0, 0)
            pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

        # Afficher la barre de santé
        pygame.draw.rect(screen, (255, 0, 0), (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, CELL_SIZE, 5))
        current_health_width = int(CELL_SIZE * self.health / 100)
        pygame.draw.rect(screen, (0, 255, 0), (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, current_health_width, 5))

    def take_damage(self, amount):
        """Réduit les dégâts reçus en fonction des états actifs."""
        if "blocage" in self.etats:
            amount //= 2  # Réduction de moitié
            print(f"{self.nom} utilise Bouclier, dégâts réduits à {amount}.")

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

    def utiliser_competence(self, competence, utilisateur, cible):
        """Utilise une compétence spécifique sur une cible."""
        # Vérifier si la compétence est passive
        if competence.effet == "blocage":
            print(f"{competence.nom} est une compétence passive et ne peut pas être utilisée manuellement.")
            return

        # Appliquer la compétence normalement
        if competence.utiliser(utilisateur, cible):
            self.log.append((utilisateur.nom, competence.nom, cible.nom, "Succès"))
            if cible.health <= 0:
                print(f"{cible.nom} a été vaincu !")
        else:
            self.log.append((utilisateur.nom, competence.nom, cible.nom, "Échec"))


    def afficher_menu_competences(self):
        """Affiche les compétences disponibles."""
        # À implémenter selon l'interface graphique
        pass








