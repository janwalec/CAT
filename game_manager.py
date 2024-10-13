from game_board import GameBoard
from Player import Player
import re


class GameManager:

    def __init__(self):
        self.game_board = GameBoard()
        self.white_player, self.black_player = self.create_players()
        self.white_turn = False


    def translate_chess_notation(self, notation):
        is_capture = True if ('x' in notation) else False
        is_check = True if ('+' in notation) else False
        is_checkmate = True if ('#' in notation) else False
        is_promotion = True if ('=' in notation) else False

        column, row, action = None, None, None
        # action is either moves or takes

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


            # pawn can be described by:
            #   nothing - empty string
            #   (lowercased) letter of it's column
            if len(figure) == 0:
                figure = " " # replace for a name of a pawn
            elif len(figure) == 1 and figure.islower():
                column = figure
                figure = " "

            # figure can be described by:
            #   single capital letter
            #   single capital letter and a number of row (char)*(int)
            #   single capital letter and a number of column (char)*(char)
            #   single capital letter, a number of column and a number of row (char)*(char)*(int)
            elif len(figure) == 1:
                pass

            elif len(figure) == 3:
                column = figure[1]
                row = figure[2]
                figure = figure[0]

            else: # len(figure) == 2
                if re.search(r'\d', figure): # there was a number in a string (row)
                    row = figure[1]
                    figure = figure[0]
                else:
                    column = figure[1]
                    figure = figure[0]

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

        if is_promotion:
            description += " and promotes to " + pieces.get(promotion, "Pawn")

        if is_check:
            description += " and gives check"
        elif is_checkmate:
            description += " and gives checkmate"






        return description





    def create_players(self):
        white_player = Player(True)
        black_player = Player(False)
        for i in self.game_board.board:
            for j in i:
                piece = j.get_piece()
                if piece is not None:
                    if piece.is_white():
                        white_player.add_piece(piece)
                    else:
                        black_player.add_piece(piece)

        return white_player, black_player



