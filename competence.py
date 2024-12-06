class Competence:
    def __init__(self, nom, degats, portee, zone_effet=1, effet=None):
        self.nom = nom
        self.degats = degats
        self.portee = portee
        self.zone_effet = zone_effet
        self.effet = effet

    def est_a_portee(self, lanceur, cible):
        """
        Vérifie si une cible est dans la portée de la compétence.
        """
        distance = abs(lanceur.x - cible.x) + abs(lanceur.y - cible.y)
        return distance <= self.portee

    def appliquer_effet(self, cible):
        """
        Applique l'effet spécial de la compétence à la cible.
        """
        if self.effet == "soin":
            cible.heal(self.degats)  # Soigne la cible en fonction des dégâts (transformés en points de soin)
            print(f"{cible.nom} a été soigné de {self.degats} PV !")
        elif self.effet == "poison":
            cible.take_damage(self.degats)  # Inflige des dégâts à la cible
            cible.etats.append("empoisonné")  # Ajoute l'état "empoisonné" à l'unité cible
            print(f"{cible.nom} a été empoisonné et subit {self.degats} dégâts !")
        elif self.effet == "ralentissement":
            cible.vitesse = max(cible.vitesse - 2, 0)  # Ralentit la cible (réduit la vitesse)
            print(f"{cible.nom} a été ralenti ! Vitesse réduite à {cible.vitesse}.")
        else:
            print(f"Aucun effet spécial à appliquer pour {self.nom}.")

    def utiliser(self, lanceur, cible):
        """
        Utilise la compétence sur une cible.

        :param lanceur: L'unité qui utilise la compétence.
        :param cible: L'unité ciblée par la compétence.
        """
        # Vérifier si la cible est un allié ou un ennemi en fonction de l'effet
        if self.effet == "soin" and lanceur.team != cible.team:
            print(f"Erreur : {self.nom} (soin) ne peut être utilisée que sur un coéquipier.")
            return
        elif self.effet != "soin" and lanceur.team == cible.team:
            print(f"Erreur : {self.nom} ne peut pas être utilisée sur un coéquipier.")
            return

        # Vérifier si la cible est à portée
        if not self.est_a_portee(lanceur, cible):
            print(f"{self.nom} est hors de portée (distance maximale : {self.portee}).")
            return

        # Appliquer l'effet de la compétence
        if self.zone_effet == 1:  # Compétence à cible unique
            if self.effet == "soin":
                cible.heal(self.degats)  # Soigne la cible
                print(f"{lanceur.nom} soigne {cible.nom} de {self.degats} PV !")
            else:
                cible.take_damage(self.degats)  # Inflige des dégâts
                print(f"{lanceur.nom} utilise {self.nom} sur {cible.nom}, infligeant {self.degats} dégâts !")
        else:
            print(f"{self.nom} a une zone d'effet, mais cela n'est pas encore implémenté.")

        # Appliquer l'effet secondaire si présent
        if self.effet and self.effet != "soin":
            self.appliquer_effet(cible)  # Applique l'effet (poison, ralentissement, etc.)
