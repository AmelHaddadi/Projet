from competence import Competence

class CompetenceManager:
    def __init__(self):
        self.log = []  # Historique des compétences utilisées

    def utiliser_competence(self, competence, utilisateur, cible):
        """Utilise une compétence spécifique sur une cible."""
        # Appeler la méthode 'utiliser' de la compétence
        if competence.utiliser(utilisateur, cible):
            self.log.append((utilisateur.nom, competence.nom, cible.nom, "Succès"))
            if cible.health <= 0:
                print(f"{cible.nom} a été vaincu !")
        else:
            self.log.append((utilisateur.nom, competence.nom, cible.nom, "Échec"))

    def afficher_log(self):
        """Affiche l'historique des compétences utilisées."""
        for action in self.log:
            print(f"{action[0]} a utilisé {action[1]} sur {action[2]} : {action[3]}")
