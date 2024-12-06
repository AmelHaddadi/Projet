class CompetenceManager:
    def __init__(self):
        self.log = []  # Historique des compétences utilisées

    def utiliser_competence(self, competence, utilisateur, cible):
        """Utilise une compétence spécifique sur une cible."""
        distance = abs(utilisateur.x - cible.x) + abs(utilisateur.y - cible.y)
        if distance > competence.portee:
            print(f"{cible.nom} est hors de portée pour {competence.nom}.")
            self.log.append((utilisateur.nom, competence.nom, cible.nom, "Echec"))
            return False

        # Appliquer la compétence
        competence.utiliser(utilisateur, cible)
        self.log.append((utilisateur.nom, competence.nom, cible.nom, "Succès"))

        # Gérer des effets persistants (exemple : poison)
        if competence.effet == "poison":
            cible.etats.append("empoisonné")
            print(f"{cible.nom} est maintenant empoisonné.")

        if cible.health <= 0:
            print(f"{cible.nom} a été vaincu !")
            return True
        return False

    def afficher_log(self):
        """Affiche l'historique des compétences utilisées."""
        for action in self.log:
            print(f"{action[0]} a utilisé {action[1]} sur {action[2]} : {action[3]}")
