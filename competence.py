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
            print(f"{cible.nom} a été soigné de {self.degats} PV !")
        elif self.effet == "poison":
            cible.take_damage(self.degats)  # Inflige des dégâts à la cible
            cible.etats.append("empoisonné")  # Ajoute l'état "empoisonné"
            print(f"{cible.nom} a été empoisonné et subit {self.degats} dégâts !")
        elif self.effet == "brulure":
            cible.take_damage(self.degats)  # Inflige des dégâts de brûlure
            cible.etats.append("brûlé")
            print(f"{cible.nom} a été brûlé et subit {self.degats} dégâts !")
        else:
            print(f"Aucun effet spécial pour {self.nom}.")

    def utiliser(self, lanceur, cible):
        """Utilise la compétence sur une cible."""
        if not self.est_a_portee(lanceur, cible):
            print(f"{self.nom} est hors de portée.")
            return False

        # Appliquer les effets de la compétence
        if self.effet:
            self.appliquer_effet(cible)

        # Infliger les dégâts
        cible.take_damage(self.degats)
        print(f"{lanceur.nom} utilise {self.nom} sur {cible.nom}, infligeant {self.degats} dégâts !")
        return True


# Définition des compétences des personnages et modes
competences_personnages = {
    "tireur": {
        "commune": Competence("Pistolet", degats=20, portee=5),
        "specific": Competence("Grenade", degats=50, portee=3, effet="ralentissement")
    },
    "tueur": {
        "commune": Competence("Pistolet", degats=20, portee=5),
        "specific": Competence("Dague", degats=30, portee=1, effet="poison")
    },
    "tank": {
        "commune": Competence("Pistolet", degats=20, portee=5),
        "specific": Competence("Bouclier", degats=0, portee=0, effet="soin")
    },
    "sorcier": {
        "commune": Competence("Pistolet", degats=20, portee=5),
        "specific": Competence("Bâton magique", degats=40, portee=4, effet="poison")
    },
}

competences_modes = {
    "air": Competence("Vent", degats=10, portee=6, effet="ralentissement"),
    "terre": Competence("Roche", degats=40, portee=3),
    "feu": Competence("Boule de feu", degats=60, portee=5, effet="poison"),
    "electricite": Competence("Éclair", degats=50, portee=5, effet="ralentissement"),
}


# Fonction pour obtenir les compétences d'un personnage et d'un mode
def obtenir_competences(personnages, mode):
    competences = {
        "commune": [],
        "specific": [],
        "mode": []
    }

    # Ajouter les compétences communes et spécifiques des personnages
    for personnage in personnages:
        competences["commune"].append(competences_personnages[personnage]["commune"])
        competences["specific"].append(competences_personnages[personnage]["specific"])

    # Ajouter la compétence spécifique du mode
    competences["mode"].append(competences_modes[mode])

    return competences