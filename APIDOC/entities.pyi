import pygame
from _typeshed import Incomplete
from player import Color, Player

class HPBar(pygame.sprite.Sprite):
    MAXHP: int
    hp: int
    size: int
    surface: pygame.Surface
    def __init__(self, MAXHP: int) -> None: ...
    def update_prop(self) -> None: ...

class Entity(pygame.sprite.Sprite):
    img: pygame.Surface
    surface: pygame.Surface
    pos: tuple[int,int]
    properties: dict
    hpbar: HPBar
    def __init__(self, texture: pygame.Surface, pos: tuple[int, int], type: str, subtype: str) -> None: ...
    def update_pv(self) -> None: ...
    def goto(self, x: int = ..., y: int = ...) -> None: ...
    def get_rect(self) -> tuple[float, float]: ...
    def get_pos(self) -> tuple[int, int]: ...
    def blit(self, display: pygame.Surface) -> None: ...

class Piece(Entity):
    roles: tuple[str]
    colors: tuple[str]
    camp: Player
    oppocamp: Player
    img: pygame.Surface
    def __init__(self, color: Color, role: str, pos: tuple[int, int]) -> None: ...
    def load_camps(self, camp: object, oppocamp: object): ...

class Chest(Entity):
    appartenance: str
    img: pygame.Surface
    def __init__(self, appartenance: str, pos: tuple[int, int]) -> None: ...

class Filtre(pygame.sprite.Sprite):
    pos: tuple[int,int]
    rect: pygame.Rect
    image: pygame.Surface
    def __init__(self, pos: tuple[int, int], color_asrgb: tuple[int, int, int] = ...) -> None: ...
    def blit(self, DISPLAY_SURF) -> None: ...
