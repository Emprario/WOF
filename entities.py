import pygame
import json
from RESSOURCE import REEL_SIZE
from player import Color


class HPBar(pygame.sprite.Sprite):
    """
    Objet destiné à afficher la barre de vie des Pieces/Batiment en vie
    /!\ Ne peut s'afficher de lui-même
    """

    def __init__(self, MAXHP: int) -> None:
        super().__init__()
        self.MAXHP = MAXHP
        self.hp = MAXHP
        self.size = REEL_SIZE
        self.surface = pygame.Surface((self.size, REEL_SIZE/10))
        self.surface.fill((200, 0, 0))

    def update_prop(self) -> None:
        """Update la taille de la bar à afficher"""
        self.size = self.hp * REEL_SIZE / self.MAXHP
        self.surface = pygame.Surface((self.size, REEL_SIZE/10))
        self.surface.fill((200, 0, 0))


class Entity(pygame.sprite.Sprite):
    """
    Objet destinée à représenter tout objet vivant (i.e. les Pieces et les Batiments)
    Possède les attributs intrasecs à tous les entités (tel que la position, les propriétés, la texture (déjà chargé))
    Possède une fonction d'affichage propre (à utiliser de préférence à la place de blit: 'Entity.blit')
    """

    def __init__(self, texture: pygame.Surface, pos: tuple[int, int], type: str, subtype: str):
        super().__init__()
        if texture != None:
            self.img = texture
        else:
            self.img = pygame.image.load("tiles/no-texture.png")
        self.surface = pygame.Surface((REEL_SIZE, REEL_SIZE))
        self.pos = pos  # By case

        # Def properties
        # Load the properties from config.json
        with open("config-good.json", "r", encoding="utf-8") as config:
            data = json.load(config)

        self.properties = data[type][subtype]

        # Prepare HPBAR
        self.hpbar = HPBar(self.properties["HP"])

    def update_pv(self) -> None:
        """Update de l'objet associé HPBar"""
        self.hpbar.hp = self.properties["HP"]
        self.hpbar.update_prop()

    def goto(self, x: int = None, y: int = None) -> None:
        """Modifie la position (future:support de chemin de déplacement)"""
        if (x, y) == (None, None):
            raise Exception(
                "Aucune coordonée fournit, alors que changement demandé")
        else:
            if x == None:
                x = self.pos[0]
            if y == None:
                y = self.pos[1]
            self.pos = x, y

    def get_rect(self) -> tuple[float, float]:
        return self.surface.get_rect()

    def get_pos(self) -> tuple[int, int]:
        return self.pos

    def blit(self, display: pygame.Surface) -> None:
        """Fonction d'affichage propre à l'objet à utiliser à la place de pygame.blit calcule aussi à partir des coordonées et de la taille réel de la carte ansi que les objets associés"""
        display.blit(self.img, [pos * REEL_SIZE for pos in self.pos])
        if self.hpbar.hp < self.hpbar.MAXHP:
            display.blit(self.hpbar.surface, [
                         pos * REEL_SIZE for pos in self.pos])


class Piece(Entity):
    """Une piece d'échec associé à joueur"""

    def __init__(self, color: Color, role: str, pos: tuple[int, int]) -> None:
        self.roles = ('B', 'K', 'N', 'P', 'Q', 'R')
        self.colors = ('w', 'b')
        self.camp = None
        self.oppocamp = None
        if color not in self.colors or role not in self.roles:
            raise TypeError
        self.role, self.color = role, color

        # pyame stuff
        self.img = pygame.image.load(
            "pieces/" + self.color + self.role + ".png")
        super().__init__(self.img, pos, "Pieces", self.role)

    def load_camps(self, camp: object, oppocamp: object):
        """
        Charge les camps indiqués au sein de l'objet afin de facilités les manipulations
        /!\ L'objet demandé est un objet Player du module player.py
        """
        self.camp = camp
        self.oppocamp = oppocamp


class Chest(Entity):
    """Représente un coffre (pas necessairement affilié à un jour)"""

    def __init__(self, appartenance: str, pos: tuple[int, int]) -> None:
        # appartenance =  'O','b','w'
        self.appartenance = appartenance

        # pygame stuff
        self.img = pygame.image.load("pieces/chest.png")
        super().__init__(self.img, pos, "Batiment", "Chest")


# class Turret(Entity):

#     def __init__(self, appartenance: str, pos: tuple[int, int]):
#         # appartenance =  'O','b','w'
#         self.appartenance = appartenance

#         super().__init__("", pos, "Batiment", "Turret")
#         self.UID = "Turret"


class Filtre(pygame.sprite.Sprite):
    """Filtre coloré permettant de surligner des cases, possède également sa propre méthode d'affichage"""

    def __init__(self, pos: tuple[int, int], color_asrgb: tuple[int, int, int] = (255, 0, 0)) -> None:
        super().__init__()
        self.pos = pos
        self.rect = pygame.Rect(0, 0, REEL_SIZE, REEL_SIZE)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(color_asrgb)
        self.image.set_alpha(125)

    def blit(self, DISPLAY_SURF):
        """A préférer à la place de pygame.blit (cf Entity.blit)"""
        DISPLAY_SURF.blit(self.image, [pos * REEL_SIZE for pos in self.pos])


if __name__ == "__main__":
    print("Please don't run this file ! \n"
          "Run this instead : \n "
          "* (windows) `py main.py` \n "
          "* (linux) `chmod +x main.py` then `./main.py` ")
