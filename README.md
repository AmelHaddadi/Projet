# Jeu de Stratégie Pygame

### Un jeu tactique au tour par tour avec des personnages uniques et des compétences variées.

Bienvenue dans **Jeu de Stratégie Pygame**

## **Fonctionnalités**
- Sélection de personnages et modes de jeu variés.
- Gestion des compétences (soin, dégâts, etc.).
- Historique des actions et animation des compétences.

## **Structure du projet**

Voici les principaux fichiers et leur rôle dans le projet :

- **`Game.py`** : 
  - Fichier principal qui initialise et exécute le jeu.
  - Gère les tours des joueurs et des ennemis, l'interface utilisateur, et les interactions globales entre les entités.

- **`unit.py`** : 
  - Définit la classe `Unit`, qui représente les personnages du jeu (joueurs ou ennemis).
  - Gère les actions comme le déplacement, l'attaque, et la gestion des compétences.

- **`competence.py`** : 
  - Contient la classe `Competence`, qui définit les compétences disponibles.
  - Gère leurs effets et la logique pour les appliquer aux cibles.

- **`CompetenceManager.py`** : 
  - Gère l'utilisation des compétences.
  - Enregistre l'historique des actions effectuées et applique les effets des compétences sur les cibles.

- **`AnimationManager.py`** : 
  - Gère les animations graphiques telles que les attaques, les déplacements, et les effets visuels comme les soins ou les explosions.

- **`MenuManager.py`** : 
  - Gère l'affichage des menus pour sélectionner les compétences ou les cibles pendant la partie.

- **`MenuSelection.py`** : 
  - Implémente le menu de sélection initial où le joueur choisit ses personnages et le mode de jeu.


## **Installation**
1. Clonez le projet :
   ```bash
   git clone https://github.com/AmelHaddadi/Projet-game-POO.git
   cd Projet-game-POO
2. Installez les dépendances : 
    pip install pygame

## **Utilisation**
1. Lancer le jeu :
    python3 Game.py
2. Suivez les instructions à l'écran pour sélectionner :
    Les personnages pour votre équipe.
    Le mode de jeu (air, feu, terre, électricité).
3. Utilisez le clavier pour contrôler les personnages :
    **Flèches directionnelles** : Déplacement.
    **C** : Utiliser une compétence.
    **Q** : Aucun choix effectué et annuler .
4. Terminez le jeu en éliminant tous les ennemis ou en perdant tous vos personnages.

## **Crédits** 
- **Bibliothèque utilisée** : [Pygame](https://www.pygame.org/)

