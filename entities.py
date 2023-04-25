import pygame
import json
from RESSOURCE import REEL_SIZE



class Entity(pygame.sprite.Sprite):

    def __init__(self, texture: str, pos: tuple[int, int]):
        super().__init__()
        self.img = texture
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.Surface((REEL_SIZE, REEL_SIZE))
        self.pos = pos  # By case
        self.UID = None

    def goto(self, x: int = None, y: int = None):
        if (x, y) == (None, None):
            raise Exception(
                "Aucune coordonée fournit, alors que changement demandé")
        else:
            if x == None:
                x = self.pos[0]
            if y == None:
                y = self.pos[1]
            self.pos = x, y

    def get_rect(self):
        return self.surface.get_rect()

    def get_pos(self):
        return self.pos

    def blit(self, display):
        display.blit(self.img, [pos * REEL_SIZE for pos in self.pos])


class Piece(Entity):

    def __init__(self, color: str, role: str, pos: tuple[int, int]):
        self.roles = ('B', 'K', 'N', 'P', 'Q', 'R')
        self.colors = ('w', 'b')
        if color not in self.colors or role not in self.roles:
            raise TypeError
        self.role, self.color = role, color

        # Load the properties from config.json
        with open("config-good.json") as config:
            data = json.load(config)

        self.properties = data['Pieces'][self.role]

        # pyame stuff
        self.img = pygame.image.load(
            "pieces/" + self.color + self.role + ".png")
        super().__init__(self.img, pos)
        self.UID = self.role


class Chest(Entity):

    def __init__(self, appartenance: str, pos: tuple[int, int]):
        # appartenance =  'O','b','w'
        self.appartenance = appartenance

        # Load the properties from config.json
        with open("config-good.json") as config:
            data = json.load(config)

        self.properties = data["Batiment"]["Chest"]

        # pygame stuff
        self.img = pygame.image.load("pieces/chest.png")
        super().__init__(self.img, pos)
        self.UID = "Chest"


class Turret(Entity):

    def __init__(self, pos: tuple[int, int]):
        self.UID = "Turret"

        # Load the properties from config.json
        with open("config-good.json") as config:
            data = json.load(config)

        self.properties = data["Batiment"]["Turret"]


class Filtre(pygame.sprite.Sprite):

    def __init__(self,pos:tuple[int,int],color_asrgb: tuple[int,int,int] = (255,0,0)) -> None:
        super().__init__()
        self.pos = pos
        self.rect = pygame.Rect(0,0, REEL_SIZE, REEL_SIZE)
        self.image = pygame.Surface( (self.rect.width, self.rect.height) )
        self.image.fill(color_asrgb)
        self.image.set_alpha(125)

    def blit(self,DISPLAY_SURF):
        DISPLAY_SURF.blit(self.image, [pos * REEL_SIZE for pos in self.pos])
