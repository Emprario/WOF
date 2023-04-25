#!/bin/env python

from entities import Piece, Filtre
from gamengine import MaitreDuJeu

if __name__ == "__main__":
    mdj = MaitreDuJeu()
    #bpion = Piece('b','P',(19,0))
    #mdj.players[1].pieces.append(bpion)
    mdj.mainloop()
