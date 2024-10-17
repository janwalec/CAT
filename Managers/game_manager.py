from Board.game_board import GameBoard
from Managers.notation_translator import translate_chess_notation, check_if_en_passant
from Player import Player
from Pieces.Pieces_enum import *


class GameManager:

    def __init__(self, path):
        self.game_board = GameBoard(path)
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


    def get_piece_from_notation(self, figure, column, row, destination, player, enemy):
        destination_column, destination_row = ord(destination[0]) % 97, 8 - int(destination[1])

        player = self.white_player if self.white_turn else self.black_player

        # column - letter in notation "(char)x"
        # row - number in notation "(char)y"
        if column is not None and row is not None:
            x, y = ord(column) % 97, 8 - int(row)
            piece = self.game_board.get_figure_from_coords(y, x)
            # print("COLUMN AND ROW GIVEN", column + row)

            if piece.check_if_move_legal(destination_row, destination_column, self.game_board):
                return piece
            return None
        else:
            list_of_possible_pieces = get_class_from_list(figure, player.player_pieces)
            if column is None and row is None:
                # print("NOTHING GIVEN")
                for piece in list_of_possible_pieces:
                    if piece.check_if_move_legal(destination_row, destination_column, self.game_board):
                        # print("piece =", piece.get_letter(), piece.get_position())
                        if player.king.get_under_attack():
                            if self.check_if_move_removes_check(player, piece, destination_row, destination_column):
                                return piece
                        else:
                            p_y, p_x = piece.get_position()
                            if self.search_for_check_after_move(player, piece, p_y, p_x, destination_row, destination_column):
                                return piece

                return None

            elif column is not None:
                # print("ONLY COLUMN GIVEN", column)
                x = ord(column) % 97
                for piece in list_of_possible_pieces:
                    if piece.get_position()[1] == x:
                        if piece.check_if_move_legal(destination_row, destination_column, self.game_board):
                            # print("piece =", piece.get_letter(), piece.get_position())
                            return piece
                return None

            if row is not None:
               #  print("ONLY ROW GIVEN", row)
                y = 8 - int(row)
                for piece in list_of_possible_pieces:
                    if piece.get_position()[0] == y:
                        if piece.check_if_move_legal(destination_row, destination_column, self.game_board):
                            # print("piece =", piece.get_letter(), piece.get_position())
                            return piece
                return None


    def tell_if_king_under_attack(self, player):
        king_pos_y, king_pos_x = player.king.get_position()
        attacked = player.king.check_if_under_attack(self.game_board, king_pos_y, king_pos_x)
        if attacked:
            # print("ATTACKED")
            player.king.set_under_attack(True)
            return True

        player.king.set_under_attack(False)
        return False

    def complete_move(self, player, enemy, piece_to_move, destination_row, destination_column, occupant):
        player_piece = list(filter(lambda x: x == piece_to_move, player.player_pieces))[0]
        player_piece.set_moved()
        p_y, p_x = player_piece.get_position()
        self.game_board.set_figure_on_coords(p_y, p_x, None)
        self.game_board.set_figure_on_coords(destination_row, destination_column, player_piece)
        player_piece.set_position(destination_row, destination_column)
        self.white_turn = not self.white_turn

        if occupant is not None:
            enemy.player_pieces.remove(occupant)

    def search_for_check_after_move(self, player, piece_to_move, p_y, p_x, destination_row, destination_column):
        player_piece = list(filter(lambda x: x == piece_to_move, player.player_pieces))[0]

        occupant = self.game_board.get_figure_from_coords(destination_row, destination_column)
        self.game_board.set_figure_on_coords(p_y, p_x, None)
        self.game_board.set_figure_on_coords(destination_row, destination_column, player_piece)
        player_piece.set_position(destination_row, destination_column)

        king_y, king_x = player.king.get_position()
        legal = not player.king.check_if_under_attack(self.game_board, king_y, king_x)

        self.game_board.set_figure_on_coords(p_y, p_x, player_piece)
        self.game_board.set_figure_on_coords(destination_row, destination_column, occupant)

        player_piece.set_position(p_y, p_x)
        return legal

    def complete_promotion(self, player, piece, promotion):
        p_y, p_x = piece.get_position()
        new_piece = PE[promotion].value(piece.is_white())
        new_piece.set_moved()
        new_piece.set_position(p_y, p_x)
        player.player_pieces.remove(piece)
        player.player_pieces.append(new_piece)
        self.game_board.set_figure_on_coords(p_y, p_x, new_piece)
        #print(new_piece)

    def process_move(self, move):
        figure, column, row, action, destination, promotion, is_check, is_checkmate = translate_chess_notation(move)

        destination_column, destination_row = -1, -1
        p_y, p_x = 0, 0
        piece = None

        player = self.white_player if self.white_turn else self.black_player
        enemy = self.white_player if not self.white_turn else self.black_player

        if action != "Long castle" and action != "Short castle":
            piece = self.get_piece_from_notation(figure, column, row, destination, player, enemy)
            destination_column, destination_row = ord(destination[0]) % 97, 8 - int(destination[1])


        king_y, king_x = player.king.get_position()
        if action == "Long castle":
            if player.king.can_castle(action, self.game_board):
                #print("COULD LONG CASTLE")
                piece = self.game_board.get_figure_from_coords(king_y, king_x - 4) # rook

                piece.set_moved()
                player.king.set_moved()

                piece.set_position(king_y, 3)
                player.king.set_position(king_y, 2)
                self.game_board.set_figure_on_coords(king_y, 3, piece)
                self.game_board.set_figure_on_coords(king_y, 2, player.king)
                self.game_board.set_figure_on_coords(king_y, 0, None)
                self.game_board.set_figure_on_coords(king_y, 4, None)

                self.white_turn = not self.white_turn
            else:
                print("COULD NOT LONG CASTLE")

        elif action == "Short castle":
            if player.king.can_castle(action, self.game_board):
                #print("COULD SHORT CASTLE")
                piece = self.game_board.get_figure_from_coords(king_y, king_x + 3)  # rook

                piece.set_moved()
                player.king.set_moved()
                p_y, p_x = piece.get_position()
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
                    p_y, p_x = piece.get_position()
                    if self.search_for_check_after_move(player, piece, p_y, p_x, destination_row, destination_column):
                        self.complete_move(player, enemy, piece, destination_row, destination_column, None)

        else:
            if piece is not None:
                enemy_figure = self.game_board.get_figure_from_coords(destination_row, destination_column)
                if enemy_figure is not None:

                    if player.king.get_under_attack():
                        if not self.check_if_move_removes_check(player, piece, destination_row, destination_column):
                            return

                    p_y, p_x = piece.get_position()
                    if self.search_for_check_after_move(player, piece, p_y, p_x, destination_row, destination_column):
                        self.complete_move(player, enemy, piece, destination_row, destination_column, enemy_figure)
            else:
                if figure == 'P':
                    en_passant_figure = check_if_en_passant(figure, column, destination_column, destination_row, enemy, player)
                    if en_passant_figure is not None:
                        #print("EN PASSANT")
                        self.process_en_passant(en_passant_figure, destination_column, destination_row, enemy, player)
                        piece = en_passant_figure
                        self.white_turn = not self.white_turn
                    else:
                        print("NOT EN PASSANT")

        if promotion != "":
            self.complete_promotion(player, piece, promotion)
        self.tell_if_king_under_attack(player)
        self.tell_if_king_under_attack(enemy)

        if piece is not None and p_y >= 0:
            player.set_last_move(piece, p_y, p_x, destination_row, destination_column)
            #player.print_last_move()

        return piece

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

    def process_en_passant(self, player_pawn, destination_column, destination_row, enemy, player):
        enemy_pawn, enemy_last_y, enemy_last_x, enemy_went_to_y, enemy_went_to_x = enemy.get_last_move()

        # set pawn as it was 1 field above/below from og move
        enemy_pawn_og_y, enemy_pawn_og_x = enemy_pawn.get_position()
        self.game_board.set_figure_on_coords(destination_row, destination_column, enemy_pawn)
        self.game_board.set_figure_on_coords(enemy_went_to_y, enemy_went_to_x, None)

        player_pawn_y, player_pawn_x = player_pawn.get_position()

        legal = False
        removes_check = False


        if player_pawn.check_if_move_legal(destination_row, destination_column, self.game_board):
            legal = True
            if player.king.get_under_attack():
                # print("en passant under attack")
                if self.check_if_move_removes_check(player, player_pawn, destination_row, destination_column):
                    removes_check = True
            else:
                removes_check = True

        if legal and removes_check:
            # print("legal, checking for new check")
            self.game_board.set_figure_on_coords(player_pawn_y, player_pawn_x, None)
            self.game_board.set_figure_on_coords(destination_row, destination_column, player_pawn)

            king_y, king_x = player.king.get_position()
            if player.king.check_if_under_attack(self.game_board, king_y, king_x):
                # print("king is now under attack")
                legal = False

        if not legal:
            # print("illegal", legal, removes_check)
            self.game_board.set_figure_on_coords(enemy_pawn_og_y, enemy_pawn_og_x, enemy_pawn)
            self.game_board.set_figure_on_coords(player_pawn_y, player_pawn_x, player_pawn)
            self.game_board.set_figure_on_coords(destination_row, destination_column, None)
        else:
            # print("no check found")
            enemy.player_pieces.remove(enemy_pawn)
            player_pawn.set_position(destination_row, destination_column)
