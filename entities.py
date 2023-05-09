import pygame
import json
from RESSOURCE import REEL_SIZE

class HPBar(pygame.sprite.Sprite):

    def __init__(self,MAXHP:int):
        super().__init__()
        self.MAXHP = MAXHP
        self.hp = MAXHP
        self.size = REEL_SIZE
        self.surface = pygame.Surface((self.size, REEL_SIZE/10))
        self.surface.fill((200,0,0))

    def update_prop(self):
        self.size = self.hp * REEL_SIZE / self.MAXHP
        self.surface = pygame.Surface((self.size, REEL_SIZE/10))
        self.surface.fill((200,0,0))


class Entity(pygame.sprite.Sprite):

    def __init__(self, texture: pygame.image, pos: tuple[int, int], type:str, subtype:str):
        super().__init__()
        if texture != None:
            self.img = texture
        else:
            self.img = pygame.image.load("tiles/no-texture.png")
        self.surface = pygame.Surface((REEL_SIZE, REEL_SIZE))
        self.pos = pos  # By case
        self.UID = None

        # Def properties
        # Load the properties from config.json
        with open("config-good.json", "r", encoding="utf-8") as config:
            data = json.load(config)

        self.properties = data[type][subtype]

        # Prepare HPBAR
        self.hpbar = HPBar(self.properties["HP"])

    def update_pv(self):
        self.hpbar.hp = self.properties["HP"]
        self.hpbar.update_prop()


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
        if self.hpbar.hp < self.hpbar.MAXHP:
            display.blit(self.hpbar.surface, [pos * REEL_SIZE for pos in self.pos])


class Piece(Entity):

    def __init__(self, color, role: str, pos: tuple[int, int]):
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
        self.UID = self.role
    
    def load_camps(self, camp, oppocamp):
        self.camp = camp
        self.oppocamp = oppocamp


class Chest(Entity):

    def __init__(self, appartenance: str, pos: tuple[int, int]):
        # appartenance =  'O','b','w'
        self.appartenance = appartenance

        # pygame stuff
        self.img = pygame.image.load("pieces/chest.png")
        super().__init__(self.img, pos, "Batiment", "Chest")
        self.UID = "Chest"


class Turret(Entity):

    def __init__(self, appartenance: str, pos: tuple[int, int]):
        # appartenance =  'O','b','w'
        self.appartenance = appartenance

        super().__init__("", pos, "Batiment", "Turret")
        self.UID = "Turret"


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

if __name__=="__main__":
    print("Please don't run this file ! \n" \
          "Run this instead : \n " \
          "* (windows) `py main.py` \n " \
          "* (linux) `chmod +x main.py` then `./main.py` ")