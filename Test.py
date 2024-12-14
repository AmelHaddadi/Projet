import pygame
from MenuSelection import afficher_menu_selection

def main():
    # Initialisation de Pygame
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))  # Remplacez par WIDTH et HEIGHT si constants définis
    pygame.display.set_caption("Test Menu de Sélection")

    # Appel de la fonction de menu
    personnages, mode = afficher_menu_selection()

    # Affichage des résultats sélectionnés
    print("Personnages sélectionnés :", personnages)
    print("Mode sélectionné :", mode)

    # Quitter proprement
    pygame.quit()

if __name__ == "__main__":
    main()
