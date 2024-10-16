from Board.game_board import GameBoard
from Managers.notation_translator import translate_chess_notation
from Player import Player
from Pieces.Pieces_enum import *


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
            print("ATTACKED")
            player.king.set_under_attack(True)
            return True

        player.king.set_under_attack(False)
        return False


    def process_move(self, move):
        figure, column, row, action, destination, promotion, is_check, is_checkmate = translate_chess_notation(move)

        destination_column, destination_row = 0, 0
        piece = None

        if action != "Long castle" and action != "Short castle":
            piece = self.get_piece_from_notation(self.white_turn, figure, column, row, action, destination, promotion, is_check, is_checkmate)
            print(piece)
            destination_column, destination_row = ord(destination[0]) % 97, 8 - int(destination[1])

        player = self.white_player if self.white_turn else self.black_player
        enemy = self.white_player if not self.white_turn else self.black_player


        king_y, king_x = player.king.get_position()
        if action == "Long castle":
            if player.king.can_castle(action, self.game_board):
                print("COULD LONG CASTLE")
                piece = self.game_board.get_figure_from_coords(king_y, king_x - 4) # rook

                piece.set_moved()
                player.king.set_moved()

                piece.set_position(king_y, 2)
                player.king.set_position(king_y, 1)
                self.game_board.set_figure_on_coords(king_y, 2, piece)
                self.game_board.set_figure_on_coords(king_y, 1, player.king)
                self.game_board.set_figure_on_coords(king_y, 0, None)
                self.game_board.set_figure_on_coords(king_y, 4, None)

                self.white_turn = not self.white_turn
            else:
                print("COULD NOT LONG CASTLE")

        elif action == "Short castle":
            if player.king.can_castle(action, self.game_board):
                print("COULD SHORT CASTLE")
                piece = self.game_board.get_figure_from_coords(king_y, king_x + 3)  # rook

                piece.set_moved()
                player.king.set_moved()

                piece.set_position(king_y, 5)
                player.king.set_position(king_y, 6)
                self.game_board.set_figure_on_coords(king_y, 5, piece)
                self.game_board.set_figure_on_coords(king_y, 6, player.king)
                self.game_board.set_figure_on_coords(king_y, 7, None)
                self.game_board.set_figure_on_coords(king_y, 4, None)

                self.white_turn = not self.white_turn
            else:
                print("COULD NOT SHORT CASTLE")


        elif action == "moves":
            if piece is not None:
                if self.game_board.get_figure_from_coords(destination_row, destination_column) is None:

                    if player.king.get_under_attack():
                        if not self.check_if_move_removes_check(player, piece, destination_row, destination_column):
                            return

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

                    if player.king.get_under_attack():
                        if not self.check_if_move_removes_check(player, piece, destination_row, destination_column):
                            return

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

    def check_if_move_removes_check(self, player, piece_moved, destination_row, destination_column):
        player_piece_y, player_piece_x = piece_moved.get_position()
        occupant = self.game_board.get_figure_from_coords(destination_row, destination_column)
        king_y, king_x = player.king.get_position()

        removed = False

        self.game_board.set_figure_on_coords(destination_row, destination_column, piece_moved)
        self.game_board.set_figure_on_coords(player_piece_y, player_piece_x, None)

        if isinstance(piece_moved, King):
            if not player.king.check_if_under_attack(self.game_board, destination_row, destination_column):
                removed = True
        else:
            if not player.king.check_if_under_attack(self.game_board, king_y, king_x):
                removed = True


        self.game_board.set_figure_on_coords(destination_row, destination_column, occupant)
        self.game_board.set_figure_on_coords(player_piece_y, player_piece_x, piece_moved)

        return removed
