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
                        if white_player.king is None and isinstance(piece, King):
                            white_player.set_king(piece)
                    else:
                        black_player.add_piece(piece)
                        if black_player.king is None and isinstance(piece, King):
                            black_player.set_king(piece)

        return white_player, black_player


    def validate_position_before_and_after_move(self, piece, player, destination_row, destination_column):
        # piece move might be illegal
        if piece.check_if_move_legal(destination_row, destination_column, self.game_board):
            if player.king.get_under_attack():
                # if king is under attack, check if move changes it
                if self.check_if_move_removes_check(player, piece, destination_row, destination_column):
                    return piece
            else:
                # king was not under attack, but it could be after a move
                if self.search_for_check_after_move(player, piece, destination_row, destination_column):
                    return piece
        return None


    def get_piece_from_notation(self, figure, column, row, destination):
        player = self.white_player if self.white_turn else self.black_player
        # column - letter in notation "(char)x"
        # row - number in notation "(char)y"
        destination_column, destination_row = ord(destination[0]) % 97, 8 - int(destination[1])

        if column is not None and row is not None:
            # given exact position
            x, y = ord(column) % 97, 8 - int(row)
            piece = self.game_board.get_figure_from_coords(y, x)

            validated = self.validate_position_before_and_after_move(piece, player, destination_row, destination_column)
            if validated is not None: return validated

            return None
        else:
            #TODO wrong notation for pawn (7e3)  errer
            list_of_possible_pieces = get_class_from_list(figure, player.player_pieces) # get all pieces that may fit the column/row
            if None in list_of_possible_pieces:
                return None

            if column is None and row is None:
                for piece in list_of_possible_pieces: # iter through pieces
                    validated = self.validate_position_before_and_after_move(piece, player, destination_row, destination_column)
                    if validated is not None: return validated

                return None

            elif column is not None:
                x = ord(column) % 97
                for piece in list_of_possible_pieces:
                    if piece.get_position()[1] == x:
                        validated = self.validate_position_before_and_after_move(piece, player, destination_row, destination_column)
                        if validated is not None: return validated

                return None

            elif row is not None:
                y = 8 - int(row)
                for piece in list_of_possible_pieces:
                    if piece.get_position()[0] == y:
                        validated = self.validate_position_before_and_after_move(piece, player, destination_row, destination_column)
                        if validated is not None: return validated
                return None
        return None # for safety


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
        # get piece from player's list and set 'moved' to true
        player_piece = list(filter(lambda x: x == piece_to_move, player.player_pieces))[0]
        player_piece.set_moved()

        # set figure on the field
        p_y, p_x = player_piece.get_position()
        self.game_board.set_figure_on_coords(p_y, p_x, None) # old field
        self.game_board.set_figure_on_coords(destination_row, destination_column, player_piece) # new field
        player_piece.set_position(destination_row, destination_column)
        self.white_turn = not self.white_turn

        # if something was captured, remove it from the list
        if occupant is not None:
            enemy.player_pieces.remove(occupant)


    def search_for_check_after_move(self, player, piece_to_move, destination_row, destination_column):
        # after a move, king could be checked

        # get piece from player's list and DO NOT set 'moved' to true
        player_piece = list(filter(lambda x: x == piece_to_move, player.player_pieces))[0]
        # get current occupant of the destination field
        occupant = self.game_board.get_figure_from_coords(destination_row, destination_column)

        # save the original position for a piece
        p_y, p_x = piece_to_move.get_position()

        # simulate the situation after this move
        self.game_board.set_figure_on_coords(p_y, p_x, None)
        self.game_board.set_figure_on_coords(destination_row, destination_column, player_piece)

        # on simulated position, check if king is under attack
        king_y, king_x = player.king.get_position()
        legal = not player.king.check_if_under_attack(self.game_board, king_y, king_x)

        # go back to original position
        self.game_board.set_figure_on_coords(p_y, p_x, player_piece)
        self.game_board.set_figure_on_coords(destination_row, destination_column, occupant)

        return legal

    def complete_promotion(self, player, piece, promotion):
        if piece is None:
            # could be None if promotion ends up with player's king being checked
            return

        # save position and remove piece (pawn)
        p_y, p_x = piece.get_position()
        player.player_pieces.remove(piece)

        # process new piece, given from promotion
        new_piece = PE[promotion].value(piece.is_white())
        new_piece.set_moved()
        new_piece.set_position(p_y, p_x)

        # save new piece
        player.player_pieces.append(new_piece)
        self.game_board.set_figure_on_coords(p_y, p_x, new_piece)


    def process_castle(self, castle_type, player):
        # magic numbers, just fixed values for both players
        # y is taken from the king
        pieces_position = [-4, 3, 2, 0] if castle_type == "Long castle" else [3, 5, 6, 7]
        king_y, king_x = player.king.get_position()
        rook = None

        # king can tell if he/rook has moved or if there is something in between them or if he got checked
        if player.king.can_castle(castle_type, self.game_board):
            rook = self.game_board.get_figure_from_coords(king_y, king_x + pieces_position[0])

            rook.set_moved()
            player.king.set_moved()

            rook.set_position(king_y, pieces_position[1])
            player.king.set_position(king_y, pieces_position[2])
            self.game_board.set_figure_on_coords(king_y, pieces_position[1], rook)
            self.game_board.set_figure_on_coords(king_y, pieces_position[2], player.king)
            self.game_board.set_figure_on_coords(king_y, pieces_position[3], None)
            self.game_board.set_figure_on_coords(king_y, 4, None)

            self.white_turn = not self.white_turn

        return rook


    def process_move(self, move):
        # init values
        figure, column, row, action, destination, promotion, is_check, is_checkmate = translate_chess_notation(move)
        destination_column, destination_row = -1, -1
        p_y, p_x = 0, 0

        player = self.white_player if self.white_turn else self.black_player
        enemy = self.white_player if not self.white_turn else self.black_player

        if action == "Long castle" or action == "Short castle":
            piece = self.process_castle(action, player)

        else: # moves or takes
            piece = self.get_piece_from_notation(figure, column, row, destination)
            destination_column, destination_row = ord(destination[0]) % 97, 8 - int(destination[1])
            if piece is not None:
                enemy_figure = self.game_board.get_figure_from_coords(destination_row, destination_column)
                p_y, p_x = piece.get_position()
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
