import pygame
from _typeshed import Incomplete
from player import Color

class HPBar(pygame.sprite.Sprite):
    MAXHP: Incomplete
    hp: Incomplete
    size: Incomplete
    surface: Incomplete
    def __init__(self, MAXHP: int) -> None: ...
    def update_prop(self) -> None: ...

class Entity(pygame.sprite.Sprite):
    img: Incomplete
    surface: Incomplete
    pos: Incomplete
    UID: Incomplete
    properties: Incomplete
    hpbar: Incomplete
    def __init__(self, texture: pygame.image, pos: tuple[int, int], type: str, subtype: str) -> None: ...
    def update_pv(self) -> None: ...
    def goto(self, x: int = ..., y: int = ...) -> None: ...
    def get_rect(self) -> tuple[float, float]: ...
    def get_pos(self) -> tuple[int, int]: ...
    def blit(self, display: pygame.Surface) -> None: ...

class Piece(Entity):
    roles: Incomplete
    colors: Incomplete
    camp: Incomplete
    oppocamp: Incomplete
    img: Incomplete
    UID: Incomplete
    def __init__(self, color: Color, role: str, pos: tuple[int, int]) -> None: ...
    def load_camps(self, camp: object, oppocamp: object): ...

class Chest(Entity):
    appartenance: Incomplete
    img: Incomplete
    UID: str
    def __init__(self, appartenance: str, pos: tuple[int, int]) -> None: ...

class Filtre(pygame.sprite.Sprite):
    pos: Incomplete
    rect: Incomplete
    image: Incomplete
    def __init__(self, pos: tuple[int, int], color_asrgb: tuple[int, int, int] = ...) -> None: ...
    def blit(self, DISPLAY_SURF) -> None: ...
