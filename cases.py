import pygame


class Cell:
    """
    Classe pour représenter une cellule sur la grille.

    Attributs
    ---------
    x : int
        La position x de la cellule sur la grille.
    y : int
        La position y de la cellule sur la grille.
    cell_type : str
        Le type de cellule ('teleport', 'wall', 'trap', ou 'normal').
    linked_cell : Cell
        La cellule liée pour la téléportation (optionnel).
    image : pygame.Surface
        L'image associée à la cellule (optionnel, seulement pour les téléportations).
    """
    def __init__(self, x, y, cell_type='normal', linked_cell=None, image=None):
        self.x = x
        self.y = y
        self.cell_type = cell_type
        self.linked_cell = linked_cell
        self.image = image

    def is_walkable(self):
        """Retourne True si la cellule est accessible."""
        return self.cell_type != 'wall'

    def on_enter(self, unit):
        """
        Applique l'effet initial d'entrée dans une cellule.
        """
        if self.cell_type == 'fire':
            # Exemple : infliger des dégâts
            unit.health -= 2

    def confirm_teleport(self, unit):
        """
        Téléporte l'unité si elle est sur une case de téléportation et confirme l'action.
        """
        if self.cell_type == 'teleport' and self.linked_cell:
            unit.x, unit.y = self.linked_cell.x, self.linked_cell.y
