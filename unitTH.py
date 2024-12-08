import pygame

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
HEALTH_BAR_HEIGHT = 6  # Hauteur de la barre de vie
HEALTH_BAR_COLOR = (0, 255, 0)  # Couleur de la barre de vie (verte)
HEALTH_BAR_BACKGROUND_COLOR = (255, 0, 0)  # Fond de la barre de vie (rouge)


class Unit:
    """
    Classe de base pour représenter une unité.

    Attributs de base :
    ------------------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé actuelle de l'unité.
    max_health : int
        La santé maximale de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    defense : int
        La défense de l'unité.
    speed : int
        La vitesse de l'unité (nombre de cases qu'elle peut se déplacer par tour).
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.
    """

    def __init__(self, x, y, health, attack_power, defense, speed, team):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health  # Ajout d'un attribut pour les points de vie maximum
        self.attack_power = attack_power
        self.defense = defense
        self.speed = speed
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            # Calcul des dégâts en fonction de la défense
            damage = max(self.attack_power - target.defense, 0)
            target.health -= damage
            print(f"{self.team} attaque {target.team} pour {damage} points de dégât.")
            # Vérifie si l'unité a perdu tous ses points de vie
            if target.health <= 0:
                print(f"{target.team} perd une unité!")

    def draw(self, screen):
        """Affiche l'unité sur l'écran avec une barre de vie."""
        # Déterminer la couleur en fonction de l'équipe
        color = BLUE if self.team == 'player' else RED

        # Dessiner le carré de sélection (si l'unité est sélectionnée)
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Dessiner l'unité sous forme de cercle
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE // 2,
                                           self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

        # Dessiner la barre de vie
        health_bar_width = CELL_SIZE  # Largeur de la barre de vie (égale à la largeur de la cellule)
        health_bar_length = (self.health / self.max_health) * health_bar_width  # Longueur de la barre de vie
        pygame.draw.rect(screen, HEALTH_BAR_BACKGROUND_COLOR,
                         (self.x * CELL_SIZE, self.y * CELL_SIZE - HEALTH_BAR_HEIGHT, health_bar_width, HEALTH_BAR_HEIGHT))
        pygame.draw.rect(screen, HEALTH_BAR_COLOR,
                         (self.x * CELL_SIZE, self.y * CELL_SIZE - HEALTH_BAR_HEIGHT,
                          health_bar_length, HEALTH_BAR_HEIGHT))


# Création des sous-classes spécifiques pour chaque type d'unité

class Soldier(Unit):
    #Soldier : Une unité de base avec des statistiques équilibrées.
    def __init__(self, x, y, team):
        super().__init__(x, y, 10, 5, 2, 1, team)  # 10 points de vie, 5 d'attaque, 2 de défense, 1 de vitesse
        self.name = "Soldier"

class Archer(Unit):
    #Archer : Une unité plus rapide et plus forte en attaque, mais plus faible en points de vie.
    def __init__(self, x, y, team):
        super().__init__(x, y, 8, 6, 1, 2, team)  # 8 points de vie, 6 d'attaque, 1 de défense, 2 de vitesse
        self.name = "Archer"

class Tank(Unit):
    #Tank : Une unité très résistante avec une défense et des points de vie élevés, mais lente.
    def __init__(self, x, y, team):
        super().__init__(x, y, 15, 3, 5, 1, team)  # 15 points de vie, 3 d'attaque, 5 de défense, 1 de vitesse
        self.name = "Tank"

# Exemple d'usage dans un jeu
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")
    
    # Création des unités
    player_units = [Soldier(0, 0, 'player'), Archer(1, 0, 'player'), Tank(2, 0, 'player')]
    enemy_units = [Soldier(6, 6, 'enemy'), Archer(7, 6, 'enemy'), Tank(8, 6, 'enemy')]
    
    # Boucle de jeu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Remplir l'écran en noir
        screen.fill(BLACK)

        # Dessiner les unités
        for unit in player_units + enemy_units:
            unit.draw(screen)

        # Rafraîchir l'écran
        pygame.display.flip()

    pygame.quit()
