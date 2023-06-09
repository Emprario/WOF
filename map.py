from entities import Chest, Piece, Entity
from RESSOURCE import JSON_PATH
import json
from random import choice
import pygame


class MapObject:
    """Stocke la map comme un objet manipulable (ainsi que ses attributs)"""

    def __init__(self) -> None:
        self.bat: list[Entity] = []
        self.gold_zone: list[list[tuple[int, int]]] = []
        self.mmap: list[list[str]] = [[]]
        self.texturemap: list[list[pygame.Surface]] = [[]]
        self.solid: list[tuple] = []
        self.spwan: list[list[Piece], list[Piece]] = [[], []]
        self.content: list[str] = None

        # main layout
        tf = open(JSON_PATH)
        self.jsonconfig: dict = json.load(tf)
        tf.close()
    
    def attribute_from_coor(self, case_co:tuple[int,int]) -> dict:
        """Get the attribute from the coordonate of a case"""
        return self.jsonconfig["Properties"][self.mmap[case_co[1]][case_co[0]][0]]

    def get_bat(self) -> list[Entity]:
        """Renvoie la liste des batiments"""
        return self.bat

    def get_texturemap(self) -> list[list[pygame.Surface]]:
        """Renvoie la matrice de texture chargée par pygame"""
        return self.texturemap

    def load_file(self, filepath: str) -> None:
        """Charge le fichier en mémoire sous 'self.content'"""
        with open(filepath, 'r') as map:
            self.content = [line for line in map]

    def record_info(self, descriptor: str) -> list[str]:
        """
        Record une info dans le contenu de la variable 'MapObject.content'
        /!\ Le fichier doit être chargé
        """
        if self.content == None:
            raise Exception("Le fichier doit être chargé d'abord à l'aide de 'MapObject.load_file'")
        record = False
        stack = []
        for line in self.content:
            if line[0] == '[' and line[-2] == ']':  # [-1] <=>  "\n"
                if line == '['+descriptor+']\n':
                    record = True
                elif record:
                    break
            elif record and line != "\n":
                stack.append(line[:-1])
        return stack

    def load_map(self) -> None:
        """
        Charge les composantes de la map dans 
        - 'MapObject.mmap': enregistrement brute de la mattrice de case
        - 'MapObject.solid': enregistre les cases solides
        - 'MapObject.bat': les batiments 
        - 'MapObject.gold_zone': les zones de gold
        - 'MapObject.texturemap': La map des textures chargés dans pygame
        """
        stack = self.record_info("layout")
        self.mmap: list[list[str]] = []
        for line in stack:
            self.mmap.append(line.split())

        solidlist = [bc for bc in self.jsonconfig["Properties"] if "Solid" in self.jsonconfig["Properties"]
                     [bc] and self.jsonconfig["Properties"][bc]["Solid"] == True]

        allzone = []
        for y in range(len(self.mmap)):
            for x in range(len(self.mmap)):
                case = self.mmap[y][x]
                if case[0] in solidlist:
                    self.solid.append((x, y))
                if len(case) > 1:
                    if case[1] == '*':
                        allzone.append((x, y))
                    elif case[1] in ('b', 'w'):
                        self.bat.append(Chest(case[1], (x, y)))
                    # Cas temporairement off
                    # elif case[0] == '8':
                    #   0  self.bat.append()

        #print("solid", self.solid)

        # Gold zone
        while len(allzone) > 0:
            self.gold_zone.append([allzone[0]])
            del allzone[0]
            i = 0
            while i < len(allzone):
                case = allzone[i]
                if case in self.__adjacent(case):
                    self.gold_zone[-1].append(case)
                    del allzone[i]
                else:
                    i += 1

        # Texture
        texturefile = self.jsonconfig["Texture"]
        #connexetxt: list[tuple[str,tuple[int,int]]] = []

        self.texturemap = [[None for j in range(len(self.mmap))]
                           for i in range(len(self.mmap))]
        for y in range(len(self.mmap)):
            for x in range(len(self.mmap)):
                casetype = self.mmap[y][x][0]
                # try:
                #     if texturefile[casetype]["connexe"]:
                #         connexetxt.append((casetype,(y,x)))
                # except KeyError:
                #     try:
                #         self.texturemap[y][x] = pygame.image.load(texturefile["rootpath"] +
                #                                                   choice(texturefile[casetype]["variations"]))
                #     except KeyError:
                #         self.texturemap[y][x] = pygame.image.load(texturefile[
                #             "rootpath"] + "no-texture.png")
                try:
                    self.texturemap[y][x] = pygame.image.load(texturefile["rootpath"] +
                                                            choice(texturefile[casetype]["variations"]))
                except KeyError:
                    self.texturemap[y][x] = pygame.image.load(texturefile[
                    "rootpath"] + "no-texture.png")
        # print(connexetxt)
        # for txt in connexetxt:
        #     adj = self.__adjacent(txt[1])
        #     gene = [xy for xy in connexetxt if xy[0] == txt[0] and xy[1] in adj]
        #     for i in range(5):
        #         if len(gene) == i:
        #             print(self.texturemap)
        #             self.texturemap[txt[1][1]][txt[1][0]] = pygame.image.load(texturefile["rootpath"] + texturefile[txt[0]]["connexe"][str(i)])
            

    def load_spwan(self) -> None:
        """Charge en mémoire dans la variable 'MapObject.spawn' les pieces de chaque camp (bien ordonée) sous forme de listes de Pieces"""
        for camp in (("white", 0), ("black", 1)):
            spawns = self.record_info("spwan "+camp[0])
            squares_b: list[tuple, tuple] = []
            square_space: list[tuple] = []
            for line in spawns:
                if line[0] in ('B', 'K', 'N', 'Q', 'R'):
                    self.spwan[camp[1]].append(
                        Piece(camp[0][0], line[0], self.__str_to_tuple(line[1:])))
                elif line[0:7] == "SQUARE_":
                    squares_b.append(self.__str_to_tuple(line[7:]))
                    if len(squares_b) >= 2:
                        square_space = self.__trace_zone(*squares_b)
            pions = []
            base = [p.get_pos() for i in range(2)
                    for p in self.spwan[i]]+[b.get_pos() for b in self.bat]
            while len(pions) < 8:
                choix = choice(square_space)
                if choix not in [p.get_pos() for p in pions] + base + self.solid:
                    #print("appended choice:", choix)
                    pions.append(Piece(camp[0][0], 'P', choix))
            self.spwan[camp[1]] += pions

    def __trace_zone(self, A: tuple[int, int], B: tuple[int, int]) -> list[tuple[int, int]]:
        minx = min(A[0], B[0])
        miny = min(A[1], B[1])
        maxx = max(A[0], B[0])
        maxy = max(A[1], B[1])
        return [(x, y) for x in range(minx, maxx+1) for y in range(miny, maxy+1)]

    def __str_to_tuple(self, chaine: str) -> tuple[int, int]:
        if chaine[0] != "(" or chaine[-1] != ")" or ',' not in chaine:
            raise ValueError(len(chaine), chaine)
        i = 1
        integer: list[str, str] = ["", ""]
        pos = 0
        while i < len(chaine)-1:
            if chaine[i] == ",":
                pos += 1
                if pos > 1:
                    raise ValueError(chaine)
            elif chaine[i] in "1234567890":
                integer[pos] += chaine[i]
            else:
                raise ValueError(chaine)
            i += 1
        return (int(integer[0]), int(integer[1]))

    def __adjacent(self, case):
        return [(case[0] + 1, case[1]), (case[0], case[1] + 1),
                (case[0] - 1, case[1]), (case[0], case[1] - 1)]


if __name__=="__main__":
    print("Please don't run this file ! \n" \
          "Run this instead : \n " \
          "* (windows) `py main.py` \n " \
          "* (linux) `chmod +x main.py` then `./main.py` ")