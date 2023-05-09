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

### La conception fonctionnelle

### La conception technique

### La conception graphique 

## Réalisation technique

### Les languages utilisés

### Les tests

## Organisation et bilan du projet

### Organisation du groupe : méthode de travail

### Résultat

### Améliorations envisagées

## Conclusion


Technologies utilisés:
* Version python : >= 3.10
* Module graphique : pygame
* Fichier de configuration :
    * __config-good.json__, pour la configurations des pieces (points de vies, dégats par coups, caractéristiques, ...)
    * __map.json__, pour la configuration de la map (nom des cases, numéro d'attribution, caractéritiques, avantages, ...)
    * __RESSOURCES.py__, constances liés aux différentes configurations diverses
* Ressources :
    * __/tiles__, pour les images des tuiles *(45x45px)*
    * __/pieces__, textures des pieces, format : *campPIECE.png  (45x45px)*
    * __/maps__, fichier de stockages des maps
    * __README.md__, fichier de documentation général :)
    * __MAP.md__, fichier de documentation des fichiers d'extension .map 

Description fichier par fichier:
* __entities.py__
* __gamengine.py__
* __main.py__ (executable)
* __/maps/map_toolbox.py__
* __map.py__

