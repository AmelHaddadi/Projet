import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu de Sélection")

# Couleurs
WHITE = (255, 255, 255)
HIGHLIGHT = (200, 200, 0)

# Charger les images
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

welcome_image = pygame.image.load("Bienvenue.png")
welcome_image = pygame.transform.scale(welcome_image, (WIDTH, HEIGHT))

# Charger la musique immersive
pygame.mixer.music.load("immersive_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Boucle infinie

# Charger un effet sonore
click_sound = pygame.mixer.Sound("click.wav")

# Police
font = pygame.font.Font(None, 50)

# Classe pour les entités (personnages ou modes)
class Entite:
    def __init__(self, nom, image, position):
        self.nom = nom
        self.image = pygame.transform.scale(image, (150, 150))
        self.position = position

    def dessiner(self, screen, selectionne=False):
        x, y = self.position
        screen.blit(self.image, (x, y))
        if selectionne:
            pygame.draw.rect(screen, HIGHLIGHT, (x, y, 150, 150), 5)
        afficher_texte(self.nom.capitalize(), x + 20, y + 160)

# Charger les personnages
personnages = [
    Entite("tireur", pygame.image.load("tireur.png"), (100, 200)),
    Entite("tueur", pygame.image.load("tueur.png"), (300, 200)),
    Entite("tank", pygame.image.load("tank.png"), (500, 200)),
    Entite("sorcier", pygame.image.load("sorcier.png"), (700, 200)),
]

# Charger les modes
modes = [
    Entite("air", pygame.image.load("air.png"), (150, 450)),
    Entite("terre", pygame.image.load("terre.png"), (350, 450)),
    Entite("feu", pygame.image.load("feu.png"), (550, 450)),
    Entite("electricite", pygame.image.load("electricite.png"), (750, 450)),
]

# Afficher du texte
def afficher_texte(text, x, y, color=WHITE):
    texte = font.render(text, True, color)
    screen.blit(texte, (x, y))

# Variables pour gérer l'état
selected_personnages = []
selected_mode = None
step = "welcome"  # Étape initiale : "welcome" -> "personnages" -> "modes"
clignotement = True  # Pour le texte clignotant

# Timer pour le clignotement du texte
clignote_event = pygame.USEREVENT + 1
pygame.time.set_timer(clignote_event, 500)

# Boucle principale
running = True
while running:
    screen.fill(WHITE)

    if step == "welcome":
        # Afficher l'écran de bienvenue
        screen.blit(welcome_image, (0, 0))
        if clignotement:
            afficher_texte("Appuyez sur Entrée pour continuer", 250, 600)

    elif step == "personnages":
        # Afficher l'écran de sélection des personnages
        screen.blit(background_image, (0, 0))
        afficher_texte("Choisissez 2 personnages", 300, 50)

        for personnage in personnages:
            personnage.dessiner(screen, personnage.nom in selected_personnages)

    elif step == "modes":
        # Afficher l'écran de sélection des modes
        screen.blit(background_image, (0, 0))
        afficher_texte("Choisissez 1 mode de jeu", 350, 50)

        for mode in modes:
            mode.dessiner(screen, mode.nom == selected_mode)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == clignote_event and step == "welcome":
            clignotement = not clignotement

        if event.type == pygame.KEYDOWN:
            if step == "welcome" and event.key == pygame.K_RETURN:
                step = "personnages"
            elif event.key == pygame.K_ESCAPE and step != "welcome":
                step = "welcome"

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if step == "personnages":
                for personnage in personnages:
                    px, py = personnage.position
                    if px < x < px + 150 and py < y < py + 150:
                        click_sound.play()
                        if personnage.nom in selected_personnages:
                            selected_personnages.remove(personnage.nom)
                        elif len(selected_personnages) < 2:
                            selected_personnages.append(personnage.nom)

                if len(selected_personnages) == 2:
                    step = "modes"

            elif step == "modes":
                for mode in modes:
                    px, py = mode.position
                    if px < x < px + 150 and py < y < py + 150:
                        click_sound.play()
                        selected_mode = mode.nom

                if selected_mode:
                    print(f"Personnages sélectionnés : {selected_personnages}")
                    print(f"Mode sélectionné : {selected_mode}")
                    afficher_texte("Merci d'avoir joué !", 300, 300)
                    pygame.time.delay(3000)
                    running = False

    pygame.display.flip()

pygame.quit()
