from typing import List, Tuple

import streamlit as st
from treys import Card, Deck
from treys import Evaluator

from models import Hand, SC


# credits
# Treys python package
# https://github.com/ihendley/treys
# StreamLit - statefull webapp
# https://blog.streamlit.io/session-state-for-streamlit/


def app():
    placeholder = st.empty()
    # INIT
    st.title('Poker play')
    if 'count' not in st.session_state:
        st.session_state.count = 0
        st.session_state.sc = SC(st)
    # END INIT

    # Streamlit runs from top to bottom on every iteraction so
    st.session_state.count += 1
    placeholder.write('INIT:')
    st.write('Count of screen refresh = ', st.session_state.count)

    # shuffle cards
    btn_shuffle_cards = st.button('shuffle cards')
    if btn_shuffle_cards:
        _sc: SC = st.session_state.sc
        _sc.deck = Deck()
        _sc.isTableSet = True
        placeholder.write('INIT:TableSet')

    btnTablePreflop = st.button('Table : preFlop')
    if btnTablePreflop:
        print('-btn preFlop')
        _sc: SC = st.session_state.sc
        # check pre condition
        # draw preFlop to players
        for index, player in enumerate(_sc.players_dict.values()):
            player.hand.card1 = _sc.deck.draw(1)
        for index, player in enumerate(_sc.players_dict.values()):
            player.hand.card2 = _sc.deck.draw(1)

        st.session_state.isPreFlop = True
        placeholder.write('INIT:TableSet:PreFlop')

    btn_flop = st.button('Table : flop')
    if btn_flop:
        print('-btn Flop')
        _sc: SC = st.session_state.sc
        _sc.board_flop = _sc.deck.draw(3)
        _sc.isFlop = True
        print('-btn Flop done')
        placeholder.write('INIT:TableSet:PreFlop:Flop')

    btn_turn = st.button('Table : turn')
    if btn_turn:
        _sc: SC = st.session_state.sc
        _sc.board_turn = _sc.deck.draw(1)
        _sc.isTurn = True
        placeholder.write('INIT:TableSet:PreFlop:Flop:Turn')

    btn_river = st.button('Table : river')
    if btn_river:
        _sc: SC = st.session_state.sc
        _sc.board_river = _sc.deck.draw(1)
        _sc.isRiver = True
        placeholder.write('INIT:TableSet:PreFlop:Flop:Turn:River')

    btn_show = st.button('Table : show')
    if btn_show:
        placeholder.write('INIT:TableSet:PreFlop:Flop:Turn:River===showing')
        layTable(st.session_state.sc)


def eval_print(msg: str, player_num: int, player_hand: Hand, rankDesc: str, score: int):
    st.write(msg, 'Player ', player_num, ' hand is '
             , Card.print_pretty_cards([player_hand.card1, player_hand.card2])
             , 'desc:', rankDesc
             , 'score:', score
             )
    st.write('            ')


def eval_player(board: List[Card], hand: Hand, evaluator: Evaluator) -> Tuple[int, str]:
    eval_score = evaluator.evaluate(board, [hand.card1, hand.card2])  # Important Treys looks at hand as array of int
    rank_class = evaluator.get_rank_class(eval_score)
    descClass = evaluator.class_to_string(rank_class)  # description of the rank class
    return eval_score, descClass


def layTable(sc: SC):
    _board = None
    if sc.isFlop:
        st.write('Flop  = ', Card.print_pretty_cards(sc.board_flop))
        _board = sc.board_flop.copy()
    if sc.isTurn:
        st.write('Turn  = ', Card.print_pretty_card(sc.board_turn))
        _board.append(sc.board_turn)
    if sc.isRiver:
        st.write('River  = ', Card.print_pretty_card(sc.board_river))
        _board.append(sc.board_river)

    # eval now
    evaluator = Evaluator()

    for index, player in enumerate(sc.players_dict.values()):
        tuple2 = eval_player(_board, player.hand, evaluator)
        player.score_abs = tuple2[0]
        player.score_desc = tuple2[1]

    from collections import OrderedDict
    # order the players : key is auto generated 0,1,2,3..., value is x[1].score_abs ->translated to -- 1,2,3...
    orderd = OrderedDict(sorted(sc.players_dict.items(), key=lambda x: x[1].score_abs))
    # get the tuple example (3)
    winner = next(iter(orderd.items()))

    for index, (k, player) in enumerate(sc.players_dict.items()):
        if k == winner[0]:
            # eval_print(msg, player_num, player_hand, rankDesc):
            eval_print('winner', player.pos, player.hand, player.score_desc, player.score_abs)
        else:
            eval_print(' - ', player.pos, player.hand, player.score_desc, player.score_abs)

    # print summy on the console
    # evaluator.hand_summary(_board, all-hands)

    st.write('game ended')


# run
app()
