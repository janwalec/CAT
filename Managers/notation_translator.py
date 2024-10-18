import re
from Pieces.Pieces_enum import *


def translate_chess_notation(notation):
    is_capture = ('x' in notation)
    is_check = ('+' in notation)
    is_checkmate = ('#' in notation)
    is_promotion = ('=' in notation)

    column, row, action = None, None, None  # action is either castle, moves or takes
    # figure - symbol of a figure; destination - field it goes to; promotion - symbol of a figure pawn promotoes to
    figure, destination, promotion = "", "", ""

    notation = notation.replace('+', '').replace('#', '')

    if notation == "O-O":
        action = "Short castle"

    elif notation == "O-O-O":
        action = "Long castle"
    else:

        if is_promotion:
            promotion = notation.split('=')[1]
            notation = notation[:-2]

        if is_capture:
            figure, destination = notation.split('x')
            action = "takes"

        else:
            destination = notation[-2:]
            figure = notation[:-2]
            action = "moves"

        # it was a pawn
        if len(figure) == 0: # just a pawn move
            figure = "P"
        elif len(figure) == 1 and figure.islower(): # pawn is a number of column (char)
            column = figure
            figure = "P"

        # it was a figure
        elif len(figure) == 1: # figure is just a single capital letter (char)
            pass

        elif len(figure) == 3: # figure is capital letter, a number of column and a number of row (char)*(char)*(int)
            column = figure[1]
            row = figure[2]
            figure = figure[0]

        else: # len(figure) == 2
            if re.search(r'\d', figure): # figure is a single capital letter and a number of row (char)*(int)
                row = figure[1]
                figure = figure[0]
            else:   # figure is a single capital letter and a number of column (char)*(char)
                column = figure[1]
                figure = figure[0]

    return figure, column, row, action, destination, promotion, is_check, is_checkmate


# for testing
def print_move_description(figure, column, row, action, destination, promotion, is_check, is_checkmate):
    description = ""
    pieces = {"K": "King", "Q": "Queen", "R": "Rook", "B": "Bishop", "N": 'Knight'}
    if action != "Short castle" and action != "Long castle":
        description += pieces.get(figure, "Pawn")

        if column is not None and row is not None:
            description += " from field "
            description += column
            description += row

        if column is not None and row is None:
            description += " from field "
            description += column
        elif row is not None and column is None:
            description += " from field "
            description += row

        description += " " + action + " " + destination
    else:
        description += action

    if promotion != "":
        description += " and promotes to " + pieces.get(promotion, "Pawn")

    if is_check:
        description += " and gives check"
    elif is_checkmate:
        description += " and gives checkmate"

    return description


def check_if_en_passant(figure, column, destination_column, destination_row , enemy, player):
    enemy_piece, enemy_last_y, enemy_last_x, enemy_went_to_y, enemy_went_to_x = enemy.get_last_move()

    pawn_to_do_en_passant = None

    if column is None or figure != 'P':
        return None
    if not isinstance(enemy_piece, Pawn):
        return None
    if abs(enemy_last_y - enemy_went_to_y) < 2:
        return None

    if destination_column != enemy_last_x:
        return None

    if not enemy.get_white() and destination_row + 1 != enemy_went_to_y:
        return None
    elif enemy.get_white() and destination_row - 1 != enemy_went_to_y:
        return None

    column = ord(column) % 97
    list_of_possible_pieces = get_class_from_list(figure, player.player_pieces)
    for piece in list_of_possible_pieces:
        p_y, p_x = piece.get_position()
        if p_x == column and p_y == enemy_went_to_y:
            pawn_to_do_en_passant = piece
            break

    return pawn_to_do_en_passant