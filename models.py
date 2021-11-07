from typing import Dict
from typing import List

from treys import Deck, Card


class Hand:
    card1: Card = None
    card2: Card = None

    def __init__(self):
        pass


class Player:
    pos: int
    name: str = ""
    hand: Hand = None
    score_abs: int = -1  # absolute score
    score_desc: str = ""
    score_rel: int = -1  # relative score

    def __init__(self, name: str, pos: int):
        self.name = name
        self.pos = pos
        self.hand = Hand()
        print('--INIT: for player ', name, '- at pos', pos, ' -hand is ', self.hand)


# Session class, to be used in StreamLit session
class SC:
    players_dict: Dict[int, Player]
    deck: Deck = None
    board_flop: List[Card] = None
    board_turn: Card = None
    board_river: Card = None
    isTableSet = False
    isPreFlop = False
    isFlop = False
    isTurn = False
    isRiver = False

    def __init__(self, st):
        st.write('Session class initialized')
        # init 7 players
        self.deck = Deck()
        self.players_dict = {1: Player("P1", 1),
                             2: Player("P2", 2),
                             3: Player("P3", 3),
                             4: Player("P4", 4),
                             5: Player("P5", 5),
                             6: Player("P6", 6),
                             7: Player("P7", 7),

                             }
