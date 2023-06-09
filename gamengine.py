import pygame
import json
from entities import Entity, Piece, Chest, Filtre
from player import Player
from map import MapObject
from RESSOURCE import MAP_SEL, REEL_SIZE, DEFAULT_ACTION_COUNT


#class GraphicalGameControlEngine:
class FeurEngine:
    """Class qui sert d'interface intermédiaire pour la communication avec pygame
    aucune autre class ne doit intéragir avec pygame (les fonctions utilisant
    l'API de pygame sont autorisé Ssi c'est FeurEngine qui les appels.)"""
    def __init__(self):
        pygame.init()
        # Display
        self.size: tuple[int,int] = (900, 900)
        self.display = pygame.display.set_mode(self.size)
        # Titre
        pygame.display.set_caption("World Of Feur")
        # active piece
        self.active_pieces = []
        # Active Scene settings
        self.background = pygame.image.load("boards/900x900.png")
        self.darkness = pygame.Surface( (900,900) )
        self.darkness.fill((0,0,0))
        self.darkness.set_alpha(125)
        self.FONT=pygame.font.Font(None, 80)

    def load_background(self, texturemap:list[list[pygame.Surface]]) -> None:
        """Charge un fond d'écran (depreciated -> use FeurEngine.blit_blank)"""
        # self.display.blit(self.background,(0,0))
        for y in range(len(texturemap)):
            for x in range(len(texturemap)):
                self.display.blit(texturemap[y][x], (x*REEL_SIZE, y*REEL_SIZE))

    def load_interface(self, player) -> None:
        """A implémenter - Affiche une interface où le joueur peut voir des statisque
        et voir l'argent accumulé; quand le prochain minion apparait, etc ..."""
        pass

    # def add_active_piece(self,obj) -> None:
    #     self.active_pieces = self.active_pieces | {obj}

    # def remove_active_piece(self,obj) -> None:
    #     self.active_pieces = self.active_pieces - {obj}

    def display_update(self, player:Player, texturemap:list[list[pygame.Surface]]):
        """Update tout le plateau à l'aide d'une matrice de d'image de pygame préchargé"""
        self.load_background(texturemap)
        self.load_interface(player)
        self.blit_pieces()
        # pygame.display.update()
        pygame.display.flip()

    def events(self) -> tuple[int, int]:
        """Renvoie où le pointeur pointe / Arrêt du programme si demandé"""
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit()
                # case pygame.KEYDOWN:
                #     match event.key:
                #         case pygame.K_SPACE:
                #             self.active_pieces[0].goto(y=self.active_pieces[0].pos[1]+1)
                case pygame.MOUSEBUTTONUP:
                    return pygame.mouse.get_pos()

                    # get a list of all sprites that are under the mouse cursor
                    # clicked_sprites = [s for s in [] if s.rect.collidepoint(pos)]

    def blit_pieces(self):
        """Affiche toute les pieces depuis son registre de pieces active"""
        for piece in self.active_pieces:
            piece.blit(self.display)
    
    def blit_blank(self, msg:str | None =None, subtitle:str | None =None):
        """Affiche un écran neutre avec éventuellement titre et/ou/sans sous-titre"""
        toblit: list[tuple] = []
        if msg != None:
            text = self.FONT.render(msg,True,(69,49,229))
            w = (900 - text.get_width())/2
            h = (900 - text.get_height())/2-250
            toblit.append((text, (w,h)))
        if subtitle != None:
            text = self.FONT.render(subtitle,True,(79,59,239))
            w = (900 - text.get_width())/2
            h = toblit[0][1][1]+toblit[0][0].get_height()
            toblit.append((text, (w,h)))
        self.display.blit(self.background, (0,0))
        self.display.blit(self.darkness, (0,0))
        for el in toblit:
            self.display.blit(*el)
        pygame.display.flip()

class MaitreDuJeu:
    """Class de coordination du jeu et des l'ordre de toute choses, elle possède les moyens"""

    def __init__(self) -> None:
        self.players:tuple[Player,Player] = (Player('w'), Player('b'))
        self.players_colors = ('w', 'b')
        self.MO = MapObject()
        self.fengine = FeurEngine()
        self.registery = []
        self.hack = [] # for debug purpose only
        self.highlighted_cases = []

        # Load config
        with open("config-good.json") as jsonconfig:
            self.config = json.load(jsonconfig)
    
    def get_other_player(self, player:Player) -> Player:
        """Obtenir l'autre joueur que celui donné"""
        return [pl for pl in self.players if pl is not player][0]

    # def spwan_entities(self) -> None:
    #     ncoef: float = self.config["Sparse"]["ncoef"]
    #     for unit in self.registery:
    #         if unit.UID not in self.config["Sparse"]:
    #             raise KeyError(f"UID : '{unit.UID}' from '{unit}' not recognized or not in the configuration file")
    #         parsing = self.config["Sparse"][unit.UID]*ncoef

    def update_registery(self, player:Player) -> None:
        """Update le registre des entités depusi différentes sources"""
        alter = self.get_other_player(player)
        self.registery: list[Entity] =  self.highlighted_cases + player.pieces + \
            alter.visible_pieces + self.MO.get_bat()
        self.fengine.active_pieces = self.registery + self.hack

    def update_visible_pieces(self) -> None:
        """Modifie les pieces visibles par les joueurs (respectivement)"""
        for player in self.players:
            player.visible_pieces = []
            alter = self.get_other_player(player)
            for piece in player.pieces:
                try:
                    hiderng = self.MO.attribute_from_coor(piece.get_pos())["Hide"]
                    adj = self.__adjacent(piece.get_pos(), hiderng, alter=False)
                    for pc_al in alter.pieces:
                        if pc_al.get_pos() in adj:
                            player.visible_pieces.append(piece)
                            break
                except KeyError:
                    player.visible_pieces.append(piece)

    def OneTour(self) -> None:
        """Ordre des choses pour un tour des deux joueurs"""
        for player in self.players:
            while self.fengine.events() == None:
                self.fengine.blit_blank("En attente du prochain joueur","Cliquer pour commencer ...")
            while player.action_count > 0 and not self.is_ended():
                self.update_visible_pieces()
                self.update_registery(player)
                self.fengine.display_update(player, self.MO.get_texturemap())
                self.actions(self.fengine.events(), player)
            self.collect_money(player)
            player.action_count = DEFAULT_ACTION_COUNT
            player.pieces_acted = []
            if self.is_ended():break
        self.repercussions()

    def mainloop(self) -> None:
        """Boucle principale qui ordonne l'initialisation du jeu, sa boucle principale 
        et son protocole de fin de jeu"""
        # Initialisation
        while self.fengine.events() == None:
            self.fengine.blit_blank("Hello World","Cliquer pour commencer ...")
        self.MO.load_file("maps/"+MAP_SEL)
        self.MO.load_map()
        self.MO.load_spwan()
        for i in range(2):
            self.players[i].pieces += self.MO.spwan[i]
            for piece in self.players[i].pieces:
                if "AttackAllies" in piece.properties and piece.properties["AttackAllies"] == True:
                    piece.load_camps(self.players[i], self.players[i])
                else:
                    piece.load_camps(self.players[i], self.players[(i+1)%2])
        self.update_visible_pieces()
        self.update_registery(self.players[0])
        # self.spwan_entities()
        while not self.is_ended():
            self.OneTour()
        self.end()

    def repercussions(self) -> None:
        """A implémenter - Répercusion à la fin d'un tour"""
        pass

    def is_ended(self) -> bool:
        """Renvoie si le jeu est terminé"""
        chest = {'w': False, 'b': False}
        for player in self.players:
            for bat in self.MO.get_bat():
                if isinstance(bat, Chest) and bat.appartenance == player.color:
                    chest[player.color] = True
        return False in chest.values()

    def end(self) -> None:
        """Protocole de fin"""
        print("END!")
        exit()

    def collect_money(self, player) -> None:
        """Récuperation de l'argent d'un joueur"""
        communs = [{tuple(z) for x in self.players[0].pieces for z in self.MO.gold_zone if x.pos in z}, {
            tuple(z) for x in self.players[1].pieces for z in self.MO.gold_zone if x.pos in z}]
        for zone in {tuple(z) for z in self.MO.gold_zone} - communs[0].intersection(communs[1]):
            for playerid in [playerid for playerid in range(len(self.players)) if player == self.players[playerid]]:
                if zone in communs[playerid]:
                    self.players[playerid].gold += 10

    def actions(self, mouse:tuple[int,int], player:Player):
        """Cliquer des pieces pour les bougers, 1 grosse, autant de petites voulus"""
        if mouse == None:
            return
        mouse = tuple(co // REEL_SIZE for co in mouse)
        try:
            sel_piece: Piece = [p for p in player.pieces if p.get_pos() == mouse and p not in player.pieces_acted][0]
        except IndexError:
            sel_piece = None
        
        if player.pointing and mouse not in player.possibilite_mvto and mouse not in player.possibilite_attack:
            player.pointing = False
            player.possibilite_mvto = []
            player.possibilite_attack = []
            player.sel_piece = None
            self.disable_highlight_all()
        elif player.pointing and mouse in player.possibilite_mvto:
            player.pointing = False
            player.possibilite_mvto = []
            player.possibilite_attack = []
            self.mvto(player.sel_piece,mouse)
            self.disable_highlight_all()
            player.pieces_acted.append(player.sel_piece)
            player.sel_piece = None
            player.action_count -= 1
        elif player.pointing and mouse in player.possibilite_attack:
            player.pointing = False
            player.possibilite_mvto = []
            player.possibilite_attack = []
            obj = [p for pl in self.players for p in pl.pieces if p.get_pos() == mouse and pl is player.sel_piece.oppocamp] + \
                  [bat for bat in self.MO.bat if bat.appartenance if bat.get_pos() == mouse]
            self.attack(player.sel_piece, obj[0])
            self.disable_highlight_all()
            player.pieces_acted.append(player.sel_piece)
            player.sel_piece = None
            player.action_count -= 1
        elif sel_piece != None:
            player.possibilite_mvto = []
            self.disable_highlight_all()
            player.pointing = True
            player.possibilite_mvto = self.show_mvto(sel_piece)
            player.sel_piece = sel_piece
            player.possibilite_attack = self.show_attack(sel_piece,sel_piece.oppocamp)

    def attack(self, origin:Entity, cible:Entity):
        """Méthode d'attaque depuis 'origin' vers la 'cible'"""
        addons = 0
        if "DPC" in self.MO.attribute_from_coor(origin.get_pos()):
            addons += self.MO.attribute_from_coor(origin.get_pos())["DPC"]
        if "Faiblesse" in self.MO.attribute_from_coor(cible.get_pos()):
            addons += self.MO.attribute_from_coor(cible.get_pos())["Faiblesse"]
        cible.properties["HP"] -= origin.properties["DPC"] + addons
        print(cible.properties)
        if cible.properties["HP"] <= 0:
            self.unreference_piece(cible)
        else:
            if cible.properties["MAXHP"] < cible.properties["HP"]:
                cible.properties["HP"] = cible.properties["MAXHP"]
            cible.update_pv()
        

    def mvto(self, cible:Entity, case:tuple[int,int]):
        """Handler pour bouger une piece, se référer à cible.goto"""
        cible.goto(*case)
        
        

    def show_attack(self, cible:Entity, target:Player) -> list:
        """Méthode d'affichage graphique des cases où la cible peut attacker"""
        adj = self.__adjacent(cible.get_pos(), cible.properties["Range"])
        piece_adv = [p.get_pos() for p in target.pieces]
        chest_adv = [bat.get_pos() for bat in self.MO.get_bat() if isinstance(bat,Chest) and bat.appartenance != target.color]
        piece_att = []
        for case in adj:
            if case in piece_adv + chest_adv:
                self.highlight_case(case,(255,0,0))
                piece_att.append(case)
        return piece_att


    def show_mvto(self, cible:Entity) -> list:
        """Se référer à self.show_attack même principe"""
        try:
            rng = cible.properties["Agilité"] + self.MO.attribute_from_coor(cible.get_pos())["Agilité"]
            #("compo",cible.properties["Agilité"],self.MO.jsonconfig["Properties"][self.MO.mmap[y][x]]["Base"]["Agilité"])
        except KeyError:
            rng = cible.properties["Agilité"]
            #("agilite alone")
        if rng == 0:
            rng = 1
        adj = self.__adjacent(cible.get_pos(), rng)
        exclusion = [obj.get_pos() for obj in self.players[0].pieces + self.players[1].pieces + self.MO.get_bat()]+self.MO.solid
        valide = []
        for case in adj:
            if case not in exclusion:
                valide.append(case)
                self.highlight_case(case,(0,0,255))
        return valide


    def highlight_case(self, case:tuple[int,int],color:tuple[int,int,int]):
        """Surligne la case 'case' avec une couleur"""
        self.highlighted_cases.append(Filtre(case,color))

    def disable_highlight_all(self) -> None:
        """Supprime tous les surlignages"""
        self.highlighted_cases = []


    def unreference_piece(self, piece:Piece) -> None:
        """Suprrime une piece du jeu"""
        for player in self.players:
            if piece in player.pieces:
                player.pieces.remove(piece)
        for bat in self.MO.bat:
            if bat == piece:
                self.MO.bat.remove(piece)
        del piece


    def __adjacent(self, case: tuple[int, int], range: int, start: int = 0, solid: bool = True, alter: bool = True) -> list:
        if start > range:
            raise ValueError("The start point cannot be superior to the total range")

        def get_case(lstcases):
            return [case[0] for case in lstcases]
        
        lstcases: list[list[tuple[int, int], int]] = [[case, 0]]
        if alter:
            camp_sel = [player for player in self.players for p in player.pieces if p.get_pos() == case][0]
            piecespos_al = [p.get_pos() for player in self.players for p in player.pieces if p.get_pos() != case and player != camp_sel]

        # Créer les cases
        for case_d in lstcases:
            cond = case_d[1] >= range
            if solid:
                cond = cond or case_d[0] in self.MO.solid
            if alter:
                cond = cond or case_d[0] in piecespos_al
            if cond:
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

if __name__=="__main__":
    print("Please don't run this file ! \n" \
          "Run this instead : \n " \
          "* (windows) `py main.py` \n " \
          "* (linux) `chmod +x main.py` then `./main.py` ")