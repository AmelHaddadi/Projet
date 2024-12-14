import pygame

class AnimationManager:
    def __init__(self, screen, colors, dimensions, cell_size=40):
        """
        Initialise le gestionnaire d'animations.

        :param screen: Surface Pygame où afficher les animations.
        :param colors: Dictionnaire des couleurs (ex: {'white': (255, 255, 255), ...}).
        :param dimensions: Dictionnaire des dimensions (ex: {'width': 800, 'height': 600}).
        :param cell_size: Taille de chaque cellule de la grille (par défaut 40).
        """
        self.screen = screen
        self.colors = colors
        self.dimensions = dimensions
        self.cell_size = cell_size

    def animer_attaque(self, x, y, sound_effect=None):
        """
        Anime une attaque sur une case spécifique avec effet sonore optionnel.

        :param x: Coordonnée x de la cible sur la grille.
        :param y: Coordonnée y de la cible sur la grille.
        :param sound_effect: Son à jouer pendant l'animation (optionnel).
        """
        if sound_effect:
            sound_effect.play()  # Joue le son si fourni
        
        explosion_radius = 30
        for i in range(explosion_radius):
            pygame.draw.circle(self.screen, self.colors['red'], 
                               (x * self.cell_size + self.cell_size // 2, 
                                y * self.cell_size + self.cell_size // 2), 
                               i)
            pygame.display.flip()
            pygame.time.delay(10)
        
        # Effacer la zone après l'animation
        rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, self.colors['white'], rect)
        pygame.display.flip()

    def animer_deplacement(self, start_x, start_y, end_x, end_y, redraw_callback):
        """
        Anime un déplacement d'une unité sur la grille en redessinant la grille.

        :param start_x: Position x de départ.
        :param start_y: Position y de départ.
        :param end_x: Position x d'arrivée.
        :param end_y: Position y d'arrivée.
        :param redraw_callback: Fonction pour redessiner l'état actuel du jeu.
        """
        x, y = start_x, start_y
        delta_x = (end_x - start_x) * 0.1
        delta_y = (end_y - start_y) * 0.1

        while abs(x - end_x) > 0.1 or abs(y - end_y) > 0.1:
            x += delta_x
            y += delta_y

            # Redessiner la grille et les unités existantes
            redraw_callback()

            # Dessiner le rectangle de déplacement
            pygame.draw.rect(self.screen, self.colors['green'], 
                             pygame.Rect(int(x * self.cell_size), int(y * self.cell_size), 
                                         self.cell_size, self.cell_size))
            pygame.display.flip()
            pygame.time.delay(20)

    def animer_soin(self, x, y):
        """
        Anime un effet de soin sur une unité.

        :param x: Coordonnée x de la cible sur la grille.
        :param y: Coordonnée y de la cible sur la grille.
        """
        for i in range(10):
            pygame.draw.circle(self.screen, self.colors['green'], 
                               (x * self.cell_size + self.cell_size // 2, 
                                y * self.cell_size + self.cell_size // 2), 
                               self.cell_size // 3 + i, 2)
            pygame.display.flip()
            pygame.time.delay(50)

        # Effacer la zone après l'animation
        rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, self.colors['white'], rect)
        pygame.display.flip()

