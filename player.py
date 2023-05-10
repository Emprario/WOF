from RESSOURCE import DEFAULT_ACTION_COUNT
from entities import Piece


Color = set["w","b"]


class Player:
    """Classe stockant les propriétés d'un joueur"""

    def __init__(self, color: str):
        self.gold: int = 100
        self.color: Color = color
        self.pieces: list[Piece] = []  # 1 grosse de chaque + 8 pions
        # Not on a case with the "Hide" attribute
        self.visible_pieces: list[Piece] = []
        self.pointing: bool = False
        self.possibilite_mvto: list[tuple[int, int]] = []
        self.possibilite_attack: list[tuple[int, int]] = []
        self.sel_piece: Piece = None
        self.action_count = DEFAULT_ACTION_COUNT
        self.pieces_acted: list[Piece] = []


if __name__ == "__main__":
    print("Please don't run this file ! \n"
          "Run this instead : \n "
          "* (windows) `py main.py` \n "
          "* (linux) `chmod +x main.py` then `./main.py` ")
