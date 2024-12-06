import pygame

class MenuManager:
    def __init__(self, screen, font, colors, dimensions):
        """
        Initialise le gestionnaire de menu.
        
        :param screen: Surface Pygame où afficher le menu.
        :param font: Police utilisée pour le texte.
        :param colors: Dictionnaire des couleurs (ex: {'white': (255, 255, 255), ...}).
        :param dimensions: Dictionnaire des dimensions (ex: {'width': 800, 'height': 600}).
        """
        self.screen = screen
        self.font = font
        self.colors = colors
        self.dimensions = dimensions

    def afficher_menu_competences(self, competences):
        """Affiche un menu pour sélectionner une compétence avec pagination."""
        items_per_page = 5  # Nombre maximum d'éléments par page
        page = 0  # Page courante

        while True:
            start_index = page * items_per_page
            end_index = min(start_index + items_per_page, len(competences))

            menu_height = items_per_page * 30 + 30
            menu_surface = pygame.Surface((self.dimensions['width'], menu_height))
            menu_surface.fill(self.colors['white'])

            for i, competence in enumerate(competences[start_index:end_index], start=1):
                texte = f"{i}. {competence.nom} (Portée: {competence.portee}, Dégâts: {competence.degats})"
                texte_surface = self.font.render(texte, True, self.colors['black'])
                menu_surface.blit(texte_surface, (10, (i - 1) * 30))

            # Ajouter une option pour "Annuler"
            annuler_texte = self.font.render("Q. Annuler", True, self.colors['black'])
            menu_surface.blit(annuler_texte, (10, items_per_page * 30))

            # Ajouter des indicateurs pour pagination
            if page > 0:
                prev_text = self.font.render("<- Précédent", True, self.colors['black'])
                menu_surface.blit(prev_text, (10, items_per_page * 30 + 30))
            if end_index < len(competences):
                next_text = self.font.render("Suivant ->", True, self.colors['black'])
                menu_surface.blit(next_text, (self.dimensions['width'] - 100, items_per_page * 30 + 30))

            self.screen.blit(menu_surface, (0, self.dimensions['height'] - menu_height))
            pygame.display.flip()

            # Gérer les entrées utilisateur
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return None
                    elif event.key == pygame.K_LEFT and page > 0:
                        page -= 1
                    elif event.key == pygame.K_RIGHT and end_index < len(competences):
                        page += 1
                    else:
                        index = event.key - pygame.K_1
                        if 0 <= index < items_per_page:
                            return competences[start_index + index]

            """Affiche un menu pour sélectionner une compétence."""
            menu_height = len(competences) * 30 + 30
            menu_surface = pygame.Surface((self.dimensions['width'], menu_height))
            menu_surface.fill(self.colors['white'])

            for i, competence in enumerate(competences):
                texte = f"{i + 1}. {competence.nom} (Portée: {competence.portee}, Dégâts: {competence.degats})"
                texte_surface = self.font.render(texte, True, self.colors['black'])
                menu_surface.blit(texte_surface, (10, i * 30))

            annuler_texte = self.font.render("Q. Annuler", True, self.colors['black'])
            menu_surface.blit(annuler_texte, (10, len(competences) * 30))

            self.screen.blit(menu_surface, (0, self.dimensions['height'] - menu_height))
            pygame.display.flip()

    def selectionner_competence(self, competences):
        """Affiche un menu pour sélectionner une compétence et retourne la compétence choisie."""
        menu_height = len(competences) * 30 + 30
        menu_surface = pygame.Surface((self.dimensions['width'], menu_height))
        menu_surface.fill(self.colors['white'])

        # Afficher les compétences
        for i, competence in enumerate(competences):
            texte = f"{i + 1}. {competence.nom} (Portée: {competence.portee}, Dégâts: {competence.degats})"
            texte_surface = self.font.render(texte, True, self.colors['black'])
            menu_surface.blit(texte_surface, (10, i * 30))

        # Ajouter une option pour annuler
        annuler_texte = self.font.render("Q. Annuler", True, self.colors['black'])
        menu_surface.blit(annuler_texte, (10, len(competences) * 30))

        self.screen.blit(menu_surface, (0, self.dimensions['height'] - menu_height))
        pygame.display.flip()

        # Attendre une sélection
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Annuler
                        return None

                    # Vérification du décalage de touche
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        index = event.key - pygame.K_1  # Convertir la touche numérique en index
                        print(f"Touche appuyée : {event.key}, index calculé : {index}")  # Debug
                        if 0 <= index < len(competences):
                            return competences[index]
    def afficher_menu_cibles(self, cibles):
        """
        Affiche un menu graphique pour choisir une cible parmi les unités disponibles.

        Paramètres:
        ----------
        cibles : list[Unit]
            Liste des unités pouvant être ciblées.

        Retourne:
        --------
        Unit : La cible choisie par le joueur.
        """
        menu_height = len(cibles) * 30 + 30  # Hauteur du menu (30 px par ligne + 30 px pour l'option annuler)
        menu_surface = pygame.Surface((self.dimensions['width'], menu_height))
        menu_surface.fill(self.colors['white'])

        # Afficher chaque cible
        for i, cible in enumerate(cibles):
            texte = f"{i + 1}. {cible.nom} (PV: {cible.health})"
            texte_surface = self.font.render(texte, True, self.colors['black'])
            menu_surface.blit(texte_surface, (10, i * 30))

        # Ajouter une option pour annuler
        annuler_texte = self.font.render("Q. Annuler", True, self.colors['black'])
        menu_surface.blit(annuler_texte, (10, len(cibles) * 30))

        self.screen.blit(menu_surface, (0, self.dimensions['height'] - menu_height))
        pygame.display.flip()

        # Attendre l'entrée de l'utilisateur pour choisir une cible
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Annuler l'action
                        return None

                    # Vérifier si l'utilisateur appuie sur une touche de 1 à 9 pour sélectionner une cible
                    index = event.key - pygame.K_1
                    if 0 <= index < len(cibles):
                        return cibles[index]  # Retourne la cible choisie
