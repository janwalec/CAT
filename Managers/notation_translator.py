import re


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
        #TODO en passant
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