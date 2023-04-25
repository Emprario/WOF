import pygame
import json
from entities import Entity, Piece, Chest, Filtre
from map import MapObject
from RESSOURCE import MAP_SEL, REEL_SIZE


#class GraphicalGameControlEngine:
class FeurEngine:
    def __init__(self):
        pygame.init()
        # Display
        self.size = (900, 900)
        self.display = pygame.display.set_mode(self.size)
        # Titre
        pygame.display.set_caption("World Of Feur")
        # active piece
        self.active_pieces = []
        # Active Scene settings
        self.background = pygame.image.load("boards/900x900.png")

    def load_background(self, texturemap) -> None:
        # self.display.blit(self.background,(0,0))
        for y in range(len(texturemap)):
            for x in range(len(texturemap)):
                self.display.blit(texturemap[y][x], (x*REEL_SIZE, y*REEL_SIZE))

    def load_interface(self, player) -> None:
        pass

    # def add_active_piece(self,obj) -> None:
    #     self.active_pieces = self.active_pieces | {obj}

    # def remove_active_piece(self,obj) -> None:
    #     self.active_pieces = self.active_pieces - {obj}

    def display_update(self, player, texturemap):
        self.load_background(texturemap)
        self.load_interface(player)
        self.blit_pieces()
        # pygame.display.update()
        pygame.display.flip()

    def events(self) -> tuple[int, int]:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                # case pygame.KEYDOWN:
                #     match event.key:
                #         case pygame.K_SPACE:
                #             self.active_pieces[0].goto(y=self.active_pieces[0].pos[1]+1)
                case pygame.MOUSEBUTTONUP:
                    return pygame.mouse.get_pos()

                    # get a list of all sprites that are under the mouse cursor
                    # clicked_sprites = [s for s in [] if s.rect.collidepoint(pos)]

    def blit_pieces(self):
        for piece in self.active_pieces:
            piece.blit(self.display)


class Player:

    def __init__(self, color: str):
        self.gold = 100
        self.played = False
        self.color = color
        self.pieces = []  # 1 grosse de chaque + 8 pions
        self.pointing = False
        self.possibilite_mvto = []
        self.possibilite_attack = []

class MaitreDuJeu:

    def __init__(self) -> None:
        self.players = (Player('w'), Player('b'))
        self.players_colors = ('w', 'b')
        self.MO = MapObject()
        self.fengine = FeurEngine()
        self.registery = []
        self.hack = []
        self.highlighted_cases = []

        # Load config
        with open("config-good.json") as jsonconfig:
            self.config = json.load(jsonconfig)

    # def spwan_entities(self) -> None:
    #     ncoef: float = self.config["Sparse"]["ncoef"]
    #     for unit in self.registery:
    #         if unit.UID not in self.config["Sparse"]:
    #             raise KeyError(f"UID : '{unit.UID}' from '{unit}' not recognized or not in the configuration file")
    #         parsing = self.config["Sparse"][unit.UID]*ncoef

    def update_registery(self) -> None:
        self.registery: list[Entity] = self.highlighted_cases + self.players[0].pieces + \
            self.players[1].pieces + self.MO.get_bat()
        self.fengine.active_pieces = self.registery + self.hack

    def OneTour(self) -> None:
        for player in self.players:
            while not player.played:
                self.update_registery()
                self.fengine.display_update(player, self.MO.get_texturemap())
                self.actions(self.fengine.events(), player)
            self.collect_money(player)
        self.repercussions()

    def mainloop(self) -> None:
        # Initialisation
        self.MO.load_file("maps/"+MAP_SEL)
        self.MO.load_map()
        self.MO.load_spwan()
        for i in range(2):
            self.players[i].pieces += self.MO.spwan[i]
        self.update_registery()
        # self.spwan_entities()
        while not self.is_ended():
            self.OneTour()
        self.end()

    def repercussions(self) -> None:
        pass

    def is_ended(self) -> bool:

        chest = {'w': False, 'b': False}
        # print(self.players)
        for player in self.players:
            for bat in self.MO.get_bat():
                if isinstance(bat, Chest) and bat.appartenance == player.color:
                    chest[player.color] = True
        return False in chest.values()

    def end(self) -> None:
        print("END!")

    def collect_money(self, player) -> None:
        communs = [{z for x in self.players[0].pieces for z in self.MO.glod_zone if x.pos in z}, {
            z for x in self.playersspwan[1].pieces for z in self.MO.glod_zone if x.pos in z}]
        for zone in {z for z in self.MO.glod_zone} - communs[0].intersection(communs[1]):
            for playerid in [playerid for playerid in self.players if player == self.players[playerid]]:
                if zone in communs[playerid]:
                    self.players[playerid].gold += 10

    def actions(self, mouse, player):
        """Cliquer des pieces pour les bougers, 1 grosse, autant de petites voulus"""
        if mouse == None:
            return
        mouse = tuple(co // REEL_SIZE for co in mouse)
        #print(mouse)
        #print(tuple(co // REEL_SIZE for co in mouse))
        sel_piece: list = [p for p in player.pieces if p.get_pos() == mouse]
        
        if len(sel_piece) > 0:
            player.possibilite_mvto = []
            self.disable_highlight_all()
            player.pointing = True
            player.possibilite_mvto = self.show_mvto(sel_piece[0])
            self.show_attack(sel_piece[0],[pl for pl in self.players if pl is not player][0])
        elif player.pointing and mouse not in player.possibilite_mvto:
            player.pointing = False
            player.possibilite_mvto = []
            self.disable_highlight_all()
        else:
            player.pointing = False
            pass

    def attack(self, origin:Entity, cible:Entity):
        cible.properties["HP"] -= origin.properties["DPC"]
        if cible.properties["HP"] < 0:
            del cible
        if cible.properties["MAXHP"] < cible.properties["HP"]:
            cible.properties["HP"] = cible.properties["MAXHP"]

    def mvto(self, cible:Entity):
        pass

    def show_attack(self, cible:Entity, target:Player) -> list:
        adj = self.adjacent(cible.get_pos(), cible.properties["Range"])
        piece_adv = [p.get_pos() for p in target.pieces]
        piece_att = []
        for case in adj:
            if case in piece_adv:
                self.highlight_case(case,(255,0,0))
                piece_att.append(case)
        return piece_att


    def show_mvto(self, cible:Entity) -> list:
        adj = self.adjacent(cible.get_pos(), cible.properties["Agilité"])
        exclusion = [obj.get_pos() for obj in self.players[0].pieces + self.players[1].pieces + self.MO.get_bat()]+self.MO.solid
        for case in adj:
            if case not in exclusion:
                self.highlight_case(case,(0,0,255))
        return adj


    def highlight_case(self, case:tuple[int,int],color:tuple[int,int,int]):
        self.highlighted_cases.append(Filtre(case,color))

    def disable_highlight_all(self) -> None:
        self.highlighted_cases = []


    def adjacent(self, case: tuple[int, int], range: int, start: int = 0) -> list:
        if start >= range:
            raise ValueError(
                "The start point cannot be superior or equal to the total range")

        def get_case(lstcases):
            return [case[0] for case in lstcases]
        lstcases: list[list[tuple[int, int], int]] = [[case, 0]]
        # Créer les cases
        for case_d in lstcases:
            if case_d[1] > range:
                continue
            next = self.__adjacent_one(case_d[0])
            for case in next:
                if case not in get_case(lstcases):
                    lstcases.append([case, case_d[1]+1])

        # supp before start
        i = 0
        while i < len(lstcases):
            if lstcases[i][1] <= start:
                del lstcases[i]
            else:
                i += 1

        # supp les doublons
        Set_cases = set(get_case(lstcases))
        return list(Set_cases)

    def __adjacent_one(self, case):
        return [(case[0] + 1, case[1]), (case[0], case[1] + 1),
                (case[0] - 1, case[1]), (case[0], case[1] - 1)]

