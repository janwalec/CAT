from math import sqrt

from Pieces.Piece import Piece


def is_in_range(val):
    # range for the board array (8x8 arr)
    return 0 <= val < 8

class King(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.set_letter('K')
        self.under_attack = False
        self.set_value(0)


    def check_if_move_legal(self, go_to_y, go_to_x, board):
        if self.position[0] == go_to_y and self.position[1] == go_to_x:
            return False # cannot stand on the same field

        if sqrt( (self.position[0] - go_to_y)**2 + (self.position[1] - go_to_x)**2 ) > sqrt(2):
            return False # max distance sqrt(2)

        occupant = board.get_figure_from_coords(go_to_y, go_to_x)
        if occupant is not None and occupant.is_white() == self.is_white():
            return False # destination field is an ally

        if self.check_if_under_attack(board, go_to_y, go_to_x):
            return False # under attack on this field

        return True

    def check_if_under_attack(self, board, go_to_y, go_to_x):
        pawn_direction = 1 if not self.is_white() else -1
        # white pawns go towards smaller y, black towards bigger y

        if is_in_range(go_to_x - 1): #check if in range of the piece
            if is_in_range(go_to_y + pawn_direction): #check if pawn in range
                # check if occupant is opposite color pawn
                occupant = board.get_figure_from_coords(go_to_y + pawn_direction, go_to_x - 1)
                if occupant is not None and occupant.is_white() != self.is_white() and occupant.get_letter() == 'P':
                    return True # it would attack the king

        if is_in_range(go_to_x + 1): # the same as above
            if is_in_range(go_to_y + pawn_direction):
                occupant = board.get_figure_from_coords(go_to_y + pawn_direction, go_to_x + 1)
                if occupant is not None and occupant.is_white() != self.is_white() and occupant.get_letter() == 'P':
                    return True

        # for opponent king
        king_move = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dx, dy in king_move:
            king_x = go_to_x + dx
            king_y = go_to_y + dy
            if is_in_range(king_x) and is_in_range(king_y): # possible king on this field
                # check if occupant is opposite color king
                occupant = board.get_figure_from_coords(king_y, king_x)
                if occupant is not None and occupant.is_white() != self.is_white() and occupant.get_letter() == 'K':
                    return True # it would attack the king

        # for opponent knight
        knight_move = [
            (-1, -2), (1, -2),  # x-1, y-2 and x+1, y-2
            (2, -1), (2, 1),  # x+2, y-1 and x+2, y+1
            (-1, 2), (1, 2),  # x-1, y+2 and x+1, y+2
            (-2, 1), (-2, -1)  # x-2, y+1 and x-2, y-1
        ]

        for dx, dy in knight_move:
                knight_x = go_to_x + dx
                knight_y = go_to_y + dy
                if is_in_range(knight_x) and is_in_range(knight_y): # possible knight on the field
                    # check if occupant is opposite color knight
                    occupant = board.get_figure_from_coords(knight_y, knight_x)
                    if occupant is not None and occupant.is_white() != self.is_white() and occupant.get_letter() == 'N':
                        return True # it would attack the king

        # for opponent rook/queen
        rook_move = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dx, dy in rook_move:
            i = 1
            # has to check if something is between rook/queen and the king
            while is_in_range(go_to_x + i * dx) and is_in_range(go_to_y + i * dy):
                # check if occupant is opposite color rook/queen
                occupant = board.get_figure_from_coords(go_to_y + i * dy, go_to_x + i * dx)
                if occupant is not None and occupant.is_white() != self.is_white() and (occupant.get_letter() == "R" or occupant.get_letter() == "Q"):
                    return True # it would attack a king
                elif occupant is not None:
                    break # it is something different, which blocks the way to the king
                i += 1

        # for opponent bishop/queen
        bishop_move = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in bishop_move:
            i, j = 1, 1
            # has to check if something is between bishop/queen and the king
            while is_in_range(go_to_y + i * dy) and is_in_range(go_to_x + j * dx):
                # check if occupant is opposite color bishop/queen
                occupant = board.get_figure_from_coords(go_to_y + i * dy, go_to_x + j * dx)
                if (occupant is not None and occupant.is_white() != self.is_white()
                        and (occupant.get_letter() == 'B'or occupant.get_letter() == 'Q')):
                    return True # it would attack a king
                elif occupant is not None:
                    break # it is something different, which blocks the way to the king

                i += 1
                j += 1
        return False


    def get_under_attack(self):
        return self.under_attack

    def set_under_attack(self, under_attack):
        self.under_attack = under_attack

    def can_castle(self, castle_type, board):
        if self.get_moved():
            return False # king was moved, cannot castle
        if self.get_under_attack():
            return False # king is under attack, cannot castle

        king_y, king_x = self.get_position()

        if castle_type == "Short castle":
            if (board.get_figure_from_coords(king_y, king_x + 3) is None
                    or board.get_figure_from_coords(king_y, king_x + 3).get_moved()):
                return False # rook is moved or there is no rook

            for i in range(1, 3):
                if board.get_figure_from_coords(king_y, king_x + i) is not None:
                    return False # something in between king and rook
                if self.check_if_under_attack(board, king_y, king_x + i):
                    return False # something attacked king in his way (chess rule for castling)

        else:
            # same as above, just long castle
            if (board.get_figure_from_coords(king_y, king_x - 4) is not None
                    and board.get_figure_from_coords(king_y, king_x -4).get_moved()):
                return False
            for i in range(1, 3):
                if board.get_figure_from_coords(king_y, king_x - i) is not None:
                    return False
                if self.check_if_under_attack(board, king_y, king_x - i):
                    return False

        return True
