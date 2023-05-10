from entities import Piece

Color = set["w","b"]

class Player:
    gold: int
    color: Color
    pieces: list[Piece]
    visible_pieces: list[Piece]
    pointing: bool
    possibilite_mvto: list[tuple[int, int]]
    possibilite_attack: list[tuple[int, int]]
    sel_piece: Piece
    action_count: int
    pieces_acted: list[Piece]
    def __init__(self, color: str) -> None: ...
