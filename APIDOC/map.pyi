import pygame
from entities import Entity, Piece

class MapObject:
    bat: list[Entity]
    gold_zone: list[list[tuple[int, int]]]
    mmap: list[list[str]]
    texturemap: list[list[pygame.Surface]]
    solid: list[tuple]
    spwan: list[list[Piece], list[Piece]]
    content: list[str]
    jsonconfig: dict
    def __init__(self) -> None: ...
    def attribute_from_coor(self, case_co: tuple[int, int]) -> dict: ...
    def get_bat(self) -> list[Entity]: ...
    def get_texturemap(self) -> list[list[pygame.Surface]]: ...
    def load_file(self, filepath: str) -> None: ...
    def record_info(self, descriptor: str) -> list[str]: ...
    def load_map(self) -> None: ...
    def load_spwan(self) -> None: ...
