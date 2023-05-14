# WOF
World Of Feur -- Powered by FeurEngine

## Introduction
Ce projet a pour but de faire tourner un jeux vidéo avec des technologies décrites [ici](#analyse-et-conception) aux critères définis ci-après. 
Le jeu en question est au tour par tour, le but est de détruire le coffre adverse en utilisant ses pions et ces pièces. Chaque pièce à des propriétés intrasecs à toutes (i.e. les points de vies, les dégats données par coups, la portée de l'attaque, les déplacements). Peut également s'y ajouter des attributs spécifiques (ex: le fou soigne ses alliés à la place d'attaquer). Les cases ont elles aussi, de la meme manière des attributs communs (peut-on passer au travers de la case, peut-on y aller plus rapidement, ...) et spécifique (on peut se cacher de la vision adverse dans des bushs). 

## Description du projet

### Exigence fonctionnelles

* Pouvoir déplacer une de ses pieces
* Attaquer/Tuer les pieces adverses
* Attaquer/Tuer les coffres adverses
* Visualiser les possibilités d'attaques et de déplacements distinctements
* Pouvoir la piece que l'on veut jouer
* Pouvoir jouer $n \in \mathbb{N} ^*$ mouvements **ou** attaques
* Ne pas pouvoir franchir des cases solides
* Pouvoir se cacher dans des buissons
* Pouvoir attaquer à la fois à distance et au cac
* Avoir des bonus en fonction de la case où l'on est

### Exigence non fonctionnelles

* Fiabilité et facile à modifier
* KISS (Keep It Simple Stupid)
* DRY (Don't Repeat Yourself)
* Ouvert à la modification dans un but de faciliter la personalisation du jeu par le joueur
  * Des fichiers de configurations
  * Des modules pythons
* Performances suffisantes pour tourner sur un ordinateur (unix/windows) moderne.

## Analyse et conception

### Spécification des exigences : les cas d'utilisations

### Analyse du domaine : le diagramme de classe

* Ce référer aux docstring au sein du code pour l'utilisation exacte des constantes/variables/méthodes/classes
* Ce référer à [APIDOC](/APIDOC/) pour les informations globales et le diagramme de classe (publique seulement)
* Les méthodes privées relèvent du fonctionnement interne des classes et ne sont pas mentionnée dans l'interface API publique.
  * [gamengine.py](/gamengine.py) : MaitreDuJeu.__adjacent, MaitreDuJeu.__adjacent_one
  * [map.py](/map.py) : MapObject.__trace_zone, MapObject.__str_to_tuple, MapObject.__adjacent
  * Pour ces méthodes se référer aux docstrings et les prototypages sur les fonctions elle-mêmes

### La conception fonctionnelle

Fragmentation du code autourde plusieur classes (OOP), 
```python
### entities.py ###

class HPBar(pygame.sprite.Sprite):
    """
    Objet destiné à afficher la barre de vie des Pieces/Batiment en vie
    /!\ Ne peut s'afficher de lui-même
    """

class Entity(pygame.sprite.Sprite):
    """
    Objet destinée à représenter tout objet vivant (i.e. les Pieces et les Batiments)
    Possède les attributs intrasecs à tous les entités (tel que la position, les propriétés, la texture (déjà chargé))
    Possède une fonction d'affichage propre (à utiliser de préférence à la place de blit: 'Entity.blit')
    """

class Piece(Entity):
    """Une piece d'échec associé à joueur"""

class Chest(Entity):
    """Représente un coffre (pas necessairement affilié à un jour)"""

class Filtre(pygame.sprite.Sprite):
    """Filtre coloré permettant de surligner des cases, possède également sa propre méthode d'affichage"""


### gamengine.py ###

class FeurEngine:
    """Class qui sert d'interface intermédiaire pour la communication avec pygame
    aucune autre class ne doit intéragir avec pygame (les fonctions utilisant
    l'API de pygame sont autorisé Ssi c'est FeurEngine qui les appels.)"""

class MaitreDuJeu:
    """Class de coordination du jeu et des l'ordre de toute choses, elle possède les moyens"""

### main.py ###

"""Module de lancement du jeu : crée une instance de MaitreDuJeu et execute sa fonction d'entrée MaitreDuJeu.mainloop"""

### map.py ###

class MapObject:
    """Stocke la map comme un objet manipulable (ainsi que ses attributs)"""

### player.py ###
class Player:
    """Classe stockant les propriétés d'un joueur"""

```
### La conception technique

* Fichier de configuration :
    * __[config-good.json](/config-good.json)__, pour la configurations des pieces (points de vies, dégats par coups, caractéristiques, ...)
    * __[map.json](/map.json)__, pour la configuration de la map (nom des cases, numéro d'attribution, caractéritiques, avantages, ...)
    * __[RESSOURCES.py](/RESSOURCE.py)__, constances liés aux différentes configurations diverses
    * __[.gitignore](/.gitignore)__, fichier de configuration du repo git
* Ressources :
    * __[/tiles/](/tiles/)__, pour les images des tuiles *- (45x45px)*
    * __[/pieces/](/pieces/)__, textures des pieces, format : *campPIECE.png - (45x45px)*
    * __[/maps/](/maps/)__, dossier de stockages des maps
    * __[/APIDOC/](/APIDOC/)__, dossier de documentation de l'API du jeu
    * __[README.md](/README.md)__, fichier de documentation général :)

Description fichier par fichier:
* __[player.py](/player.py)__
* __[entities.py](/entities.py)__
* __[gamengine.py](/gamengine.py)__
* __[main.py](/main.py)__ *(executable, entrypoint)*
* __[map.py](/map.py)__

### La conception graphique 

Interface divisée en cases, certaines cases contiennent des variations aléatoires.
Les cases sont disignés en interne, les pieces d'échec et le plateau de jeux proviennent de [chess.com](https://www.chess.com).
Les filtres de couleurs sont juste des pygame.Surface colorés avec un canal alpha à 125.

## Réalisation technique

### Les languages utilisés

Technologies utilisés:
* Version python : >= 3.10
* Module graphique : pygame
* Autres modules : json, random

### Les tests

En vue de la complexité du projet, les tests unitaire sont éviter, des tests en jeu ont été menés :
* Déplacement des pieces
* Attaque de pieces
* Tests sur les propriétés des cases
* Tests limite $\big ( \lim\limits_{m \rightarrow hp^-} hp-m$ et $\lim\limits_{m \rightarrow 0^+} hp-m \big )$ sur la barre de vie.
* Après execution du coffre, test que le jeu se termine bien
* Test de la modularité du code (adaptation à de nouvelles map, à des modifications de stats de pieces, etc ...)

## Organisation et bilan du projet

### Organisation du groupe : méthode de travail

Après une reflexion commune sur les directions que prendrait le jeu tant artistiquement, que fonctionnellement, que dans l'implémentation. nous nous sommes répartis la charge de travail.

### Résultat

Résultats pluôt satisfesant et en cohérence avec le travail fourni. Certaines fonctionnalités n'ont cependant pas été implémentés. D'autres ont été abandonées d'un point de vue de la cohérence du jeu. Par ailleurs quelques changements en cours de route nous ont forcé à réimplémenter certaines fonctionnalités déjà existante, laissant donc un peu l'optimisation de côté bien qu'elle reste correcte pour le cahier des charges que nous nous étuions imposé.

### Améliorations envisagées

* Harmonisation du code
* Finir l'implémentation de l'interface
* Ajouter la fin par manque de temps
* Implémenter la régénaration de pieces sur le terrains
* Ajouts de nouveaux builds.

## Conclusion

Pour la modification et la redistribution veillez suivre les spécification fourni [LICENSE](/LICENSE) (GNU General Public Licence)