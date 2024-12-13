class Competence:
    def __init__(self, nom, degats, portee, zone_effet=1, effet=None):
        self.nom = nom
        self.degats = degats
        self.portee = portee
        self.zone_effet = zone_effet
        self.effet = effet

    def est_a_portee(self, lanceur, cible):
        """Vérifie si une cible est dans la portée de la compétence."""
        distance = abs(lanceur.x - cible.x) + abs(lanceur.y - cible.y)
        return distance <= self.portee

    def appliquer_effet(self, cible):
        """Applique l'effet spécial de la compétence à la cible."""
        if self.effet == "soin":
            cible.heal(self.degats)  # Soigne la cible en fonction des dégâts
            #print(f"{cible.nom} a été soigné de {self.degats} PV !")
        elif self.effet == "explosion":
            cible.take_damage(self.degats)  # Inflige des dégâts à la cible
            cible.etats.append("explosé")  # Ajoute l'état "explosé"
        elif self.effet == "blessure":
            cible.take_damage(self.degats)  # Inflige des dégâts de blessure
            cible.etats.append("blessé")
        elif self.effet == "saignement" :
            cible.take_damage(self.degats)
            cible.etats.append("saigne")
        else:
            print(f"Aucun effet spécial pour {self.nom}.")

    def utiliser(self, lanceur, cible):
        """Utilise la compétence sur une cible."""
        if not self.est_a_portee(lanceur, cible):
            print(f"{self.nom} est hors de portée.")
            return False
        # Appliquer les effets si définis
        if self.effet:
            self.appliquer_effet(cible)
        else:  # Infliger les dégâts uniquement si aucun effet de type soin ou passif
            cible.take_damage(self.degats)
            #print(f"{lanceur.nom} utilise {self.nom} sur {cible.nom}, infligeant {self.degats} dégâts !")

        return True
