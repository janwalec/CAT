from game_board import GameBoard
from Player import Player
from Pieces_enum import *
import re
import Pieces_enum


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

class GameManager:

    def __init__(self):
        self.game_board = GameBoard()
        self.white_player, self.black_player = self.create_players()
        self.white_turn = True

    def create_players(self):
        white_player = Player(True)
        black_player = Player(False)
        for i in self.game_board.board:
            for j in i:
                piece = j.get_piece()
                if piece is not None:
                    if piece.is_white():
                        white_player.add_piece(piece)
                        if isinstance(piece, King):
                            white_player.set_king(piece)
                    else:
                        black_player.add_piece(piece)
                        if isinstance(piece, King):
                            black_player.set_king(piece)

        return white_player, black_player


    def get_piece_from_notation(self, is_white, figure, column, row, action, destination, promotion, is_check, is_checkmate):
        destination_column, destination_row = ord(destination[0]) % 97, 8 - int(destination[1])

        player = self.white_player if self.white_turn else self.black_player

        # column - letter in notation "(char)x"
        # row - number in notation "(char)y"
        if column is not None and row is not None:
            x, y = ord(column) % 97, 8 - int(row)
            piece = self.game_board.get_figure_from_coords(y, x)
            print("COLUMN AND ROW GIVEN", column + row)
            if piece is not None:
                print("piece =", piece.get_letter(), piece.get_position())
            else:
                print("piece = None")
            if piece.check_if_move_legal(destination_row, destination_column, self.game_board):
                return piece
            return None
        else:
            list_of_possible_pieces = get_class_from_list(figure, player.player_pieces)
            if column is None and row is None:
                print("NOTHING GIVEN")
                for piece in list_of_possible_pieces:
                    if piece.check_if_move_legal(destination_row, destination_column, self.game_board):
                        print("piece =", piece.get_letter(), piece.get_position())
                        return piece

                print("piece = None")
                return None

            if column is not None:
                print("ONLY COLUMN GIVEN", column)
                x = ord(column) % 97
                for piece in list_of_possible_pieces:
                    if piece.get_position()[1] == x:
                        if piece.check_if_move_legal(destination_row, destination_column, self.game_board):
                            print("piece =", piece.get_letter(), piece.get_position())
                            return piece
                print("piece = None")
                return None

            if row is not None:
                print("ONLY ROW GIVEN", row)
                y = 8 - int(row)
                for piece in list_of_possible_pieces:
                    if piece.get_position()[0] == y:
                        if piece.check_if_move_legal(destination_row, destination_column, self.game_board):
                            print("piece =", piece.get_letter(), piece.get_position())
                            return piece
                print("piece = None")
                return None


    def tell_if_king_under_attack(self, player):
        king_pos_y, king_pos_x = player.king.get_position()
        attacked = player.king.check_if_under_attack(self.game_board, king_pos_y, king_pos_x)
        if attacked:
            return True

        return False


    def process_move(self, move):
        figure, column, row, action, destination, promotion, is_check, is_checkmate = translate_chess_notation(move)

        piece = self.get_piece_from_notation(self.white_turn, figure, column, row, action, destination, promotion, is_check, is_checkmate)
        print(piece)
        player = self.white_player if self.white_turn else self.black_player
        enemy = self.white_player if not self.white_turn else self.black_player
        destination_column, destination_row = ord(destination[0]) % 97, 8 - int(destination[1])


        if action == "Long castle" or action == "Short castle":
            pass
        elif action == "moves":
            if piece is not None:
                if self.game_board.get_figure_from_coords(destination_row, destination_column) is None:
                    player_piece = list(filter(lambda x: x == piece, player.player_pieces))[0]
                    player_piece.set_moved()
                    p_y, p_x = player_piece.get_position()
                    self.game_board.set_figure_on_coords(p_y, p_x, None)
                    self.game_board.set_figure_on_coords(destination_row, destination_column, player_piece)
                    player_piece.set_position(destination_row, destination_column)
                    self.white_turn = not self.white_turn
        else:
            if piece is not None:
                enemy_piece = self.game_board.get_figure_from_coords(destination_row, destination_column)
                if enemy_piece is not None:
                    player_piece = list(filter(lambda x: x == piece, player.player_pieces))[0]
                    player_piece.set_moved()

                    enemy.player_pieces.remove(enemy_piece)

                    p_y, p_x = player_piece.get_position()
                    self.game_board.set_figure_on_coords(p_y, p_x, None)
                    self.game_board.set_figure_on_coords(destination_row, destination_column, player_piece)
                    player_piece.set_position(destination_row, destination_column)
                    self.white_turn = not self.white_turn

        self.tell_if_king_under_attack(player)
        self.tell_if_king_under_attack(enemy)