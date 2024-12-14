from competence import Competence

class CompetenceManager:
    def __init__(self):
        self.log = []  # Historique des compétences utilisées

<<<<<<< HEAD
    def utiliser_competence(self, competence, utilisateur, cible, mode=None):
        """Utilise une compétence spécifique sur une cible en tenant compte du mode."""
        distance = abs(utilisateur.x - cible.x) + abs(utilisateur.y - cible.y)
        if distance > competence.portee:
            print(f"{cible.nom} est hors de portée pour {competence.nom}.")
            self.log.append((utilisateur.nom, competence.nom, cible.nom, "Echec"))
            return False

        # Appliquer les effets du mode si applicable
        if mode:
            if mode == "feu":
                if competence.effet != "brulure":
                    # Si la compétence n'a pas déjà un effet brulure, on lui applique
                    competence.effet = "brulure"
                    print(f"Le mode {mode} applique un effet de brûlure sur {cible.nom}.")
            elif mode == "vent":
                if competence.effet != "ralentissement":
                    # Si la compétence n'a pas déjà un effet ralentissement, on lui applique
                    competence.effet = "ralentissement"
                    print(f"Le mode {mode} applique un effet de ralentissement sur {cible.nom}.")
            elif mode == "électricité":
                if competence.effet != "paralysie":
                    # Le mode électricité applique un effet de paralysie
                    competence.effet = "paralysie"
                    print(f"Le mode {mode} applique un effet de paralysie sur {cible.nom}.")
        # Appliquer la compétence avec ses effets
        competence.utiliser(utilisateur, cible)

        # Log l'action réalisée
        self.log.append((utilisateur.nom, competence.nom, cible.nom, "Succès"))

        # Si la cible est morte
        if cible.vie <= 0:
            print(f"{cible.nom} a été vaincu !")
            return True
        return False
=======
    def utiliser_competence(self, competence, utilisateur, cible):
        """Utilise une compétence spécifique sur une cible."""
        # Appeler la méthode 'utiliser' de la compétence
        if competence.utiliser(utilisateur, cible):
            self.log.append((utilisateur.nom, competence.nom, cible.nom, "Succès"))
            if cible.health <= 0:
                print(f"{cible.nom} a été vaincu !")
        else:
            self.log.append((utilisateur.nom, competence.nom, cible.nom, "Échec"))
>>>>>>> dbbbd56bb20d67d6265dcc0117d7eef442485579

    def afficher_log(self):
        """Affiche l'historique des compétences utilisées."""
        for action in self.log:
            print(f"{action[0]} a utilisé {action[1]} sur {action[2]} : {action[3]}")
<<<<<<< HEAD

=======
>>>>>>> dbbbd56bb20d67d6265dcc0117d7eef442485579
