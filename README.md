# WOF
World Of Feur -- Powered by FeurEngine

## Introduction
Ce projet a pour but de faire tourner un jeux vidéo avec des technologies décrites [ici](#analyse-et-conception) aux critères définis ci-après. 
Le jeu en question est au tour par tour, le but est de détruire le coffre adverse en utilisant ses pions et ces pièces. Chaque pièce à des propriétés intrasecs à toutes (i.e. les points de vies, les dégats données par coups, la portée de l'attaque, les déplacements). Peut également s'y ajouter des attributs spécifiques (ex: le fou soigne ses alliés à la place d'attaquer). Les cases ont elles aussi, de la meme manière des attributs communs (peut-on passer au travers de la case, peut-on y aller plus rapidement, ...) et spécifique (on peut se cacher de la vision adverse dans des bushs). 

## Description du projet

### Exigence fonctionnelles

### Exigence non fonctionnelles

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
    
    [comment] # (__MAP.md__, fichier de documentation des fichiers d'extension .map)

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

## Organisation et bilan du projet

### Organisation du groupe : méthode de travail

### Résultat

### Améliorations envisagées

## Conclusion

