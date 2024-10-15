from math import sqrt

from Pieces.Bishop import Bishop
from Pieces.Piece import Piece
from Pieces.Pawn import Pawn
from Pieces.Knight import Knight
from Pieces.Queen import Queen
from Pieces.Rook import Rook


def is_in_range(val):
    return 0 <= val < 8

class King(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.set_letter('K')
        self.set_value(0)


    def check_if_move_legal(self, go_to_y, go_to_x, board):
        if self.position[0] == go_to_y and self.position[1] == go_to_x:
            print("SAME FIELD")
            return False

        if sqrt( (self.position[0] - go_to_y)**2 + (self.position[1] - go_to_x)**2 ) > sqrt(2):
            print("WRONG DIRECTION")
            return False

        occupant = board.get_figure_from_coords(go_to_y, go_to_x)
        if occupant is not None and occupant.is_white() == self.is_white():
            print("SAME COLOR")
            return False

        if self.check_if_under_attack(board, go_to_y, go_to_x):
            print("UNDER ATTACK")
            return False

        return True

    def check_if_under_attack(self, board, go_to_y, go_to_x):
        pawn_direction = 1 if not self.is_white() else -1

        if is_in_range(go_to_x - 1):
            if is_in_range(go_to_y + pawn_direction):
                occupant = board.get_figure_from_coords(go_to_y + pawn_direction, go_to_x - 1)
                if occupant is not None and occupant.is_white() != self.is_white() and isinstance(occupant, Pawn):
                    return True
        if is_in_range(go_to_x + 1):
            if is_in_range(go_to_x + pawn_direction):
                occupant = board.get_figure_from_coords(go_to_y + pawn_direction, go_to_x + 1)
                if occupant is not None and occupant.is_white() != self.is_white() and isinstance(occupant, Pawn):
                    return True

        knight_move = [
            (-1, -2), (1, -2),  # x-1, y-2 and x+1, y-2
            (2, -1), (2, 1),  # x+2, y-1 and x+2, y+1
            (-1, 2), (1, 2),  # x-1, y+2 and x+1, y+2
            (-2, 1), (-2, -1)  # x-2, y+1 and x-2, y-1
        ]
        for dx, dy in knight_move:
                knight_x = go_to_x + dx
                knight_y = go_to_y + dy
                if is_in_range(knight_x) and is_in_range(knight_y):
                    occupant = board.get_figure_from_coords(knight_y, knight_x)
                    if occupant is not None and occupant.is_white() != self.is_white() and isinstance(occupant, Knight):
                        return True


        rook_move = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dx, dy in rook_move:
            i = 0
            while is_in_range(go_to_x + i * dx) and is_in_range(go_to_y + i * dy):
                occupant = board.get_figure_from_coords(go_to_y + i * dy, go_to_x + i * dx)
                if (occupant is not None and occupant.is_white() != self.is_white()
                        and (isinstance(occupant, Rook) or isinstance(occupant, Queen))):
                    return True
                elif occupant is not None:
                    break
                i += 1

        bishop_move = [(1,1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in bishop_move:
            i, j = 0, 0
            while is_in_range(go_to_y + i * dy) and is_in_range(go_to_x + j * dx):
                occupant = board.get_figure_from_coords(go_to_y + i * dy, go_to_x + j * dx)

                if (occupant is not None and occupant.is_white() != self.is_white()
                        and (isinstance(occupant, Bishop) or isinstance(occupant, Queen))):
                    return True

                elif occupant is not None:
                    break

                i += 1
                j += 1

        return False



