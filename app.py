import streamlit as st
from treys import Card
from treys import Deck
from treys import Evaluator


def app():
    # INIT
    st.title('Poker play')
    if 'count' not in st.session_state:
        st.session_state.count = 0
        st.session_state.deck = Deck()
        st.session_state.isTableSet = False
        st.session_state.isPreFlop = False
        st.session_state.isFlop = False
        st.session_state.isTurn = False
        st.session_state.isRiver = False

        st.session_state.count = 0
    # END INIT

    # Streamlit runs from top to bottom on every iteraction so
    st.session_state.count += 1
    st.write('Count of screen refresh = ', st.session_state.count)

    # shuffle cards
    btnShuffleCards = st.button('shuffle cards')
    if btnShuffleCards:
        st.session_state.isTableSet = False
        st.session_state.isPreFlop = False
        st.session_state.isFlop = False
        st.session_state.isTurn = False
        st.session_state.isRiver = False
        st.session_state.deck = Deck()
        _deck = st.session_state.deck
        st.session_state.isTableSet = True

    btnTablePreflop = st.button('Table : preFlop')
    if btnTablePreflop:
        _deck = st.session_state.deck
        st.session_state.player1_hand = _deck.draw(2)
        st.session_state.player2_hand = _deck.draw(2)
        st.session_state.player3_hand = _deck.draw(2)
        st.session_state.player4_hand = _deck.draw(2)
        st.session_state.player5_hand = _deck.draw(2)
        st.session_state.player6_hand = _deck.draw(2)
        st.session_state.player7_hand = _deck.draw(2)
        st.session_state.isPreFlop = True

    btnTableFlop = st.button('Table : flop')
    if btnTableFlop:
        _deck = st.session_state.deck
        st.session_state.board_flop = _deck.draw(3)
        st.session_state.isFlop = True

    btnTableTurn = st.button('Table : turn')
    if btnTableTurn:
        _deck = st.session_state.deck
        st.session_state.board_turn = _deck.draw(1)
        st.session_state.isTurn = True

    btnTableRiver = st.button('Table : river')
    if btnTableRiver:
        _deck = st.session_state.deck
        st.session_state.board_river = _deck.draw(1)
        st.session_state.isRiver = True

    btnTableShow = st.button('Table : show')
    if btnTableShow:
        layTable(st.session_state)


def eval_print(msg, board, player_hand, evaluator):
    eval_score = evaluator.evaluate(board, player_hand)
    rank_class = evaluator.get_rank_class(eval_score)
    descClass = evaluator.class_to_string(rank_class)  # description of the rank class
    st.write(msg, 'score is ', eval_score, ' hand is ', Card.print_pretty_cards(player_hand), '     :', descClass, '')
    st.write('            ')


def layTable(ss):
    board = None
    if (ss.isFlop):
        st.write('Flop  = ', Card.print_pretty_cards(ss.board_flop))
        board = ss.board_flop.copy()
    if (ss.isTurn):
        st.write('Turn  = ', Card.print_pretty_card(ss.board_turn))
        board.append(ss.board_turn)
    if (ss.isRiver):
        st.write('River  = ', Card.print_pretty_card(ss.board_river))
        board.append(ss.board_river)
    # eval now
    evaluator = Evaluator()

    eval_print('P1', board, ss.player1_hand, evaluator)
    eval_print('P2', board, ss.player2_hand, evaluator)
    eval_print('P3', board, ss.player3_hand, evaluator)
    eval_print('P4', board, ss.player4_hand, evaluator)
    eval_print('P5', board, ss.player5_hand, evaluator)
    eval_print('P6', board, ss.player6_hand, evaluator)
    eval_print('P7', board, ss.player7_hand, evaluator)

    hands = [ss.player1_hand, ss.player2_hand, ss.player3_hand
        , ss.player4_hand, ss.player5_hand, ss.player6_hand
        , ss.player7_hand]

    st.write('summary ', evaluator.hand_summary(board, hands))
