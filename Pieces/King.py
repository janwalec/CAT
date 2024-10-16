from math import sqrt

from Pieces.Piece import Piece


def is_in_range(val):
    return 0 <= val < 8

class King(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.set_letter('K')
        self.under_attack = False
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
                if occupant is not None and occupant.is_white() != self.is_white() and occupant.get_letter() == 'P':
                    return True
        if is_in_range(go_to_x + 1):
            if is_in_range(go_to_x + pawn_direction):
                occupant = board.get_figure_from_coords(go_to_y + pawn_direction, go_to_x + 1)
                if occupant is not None and occupant.is_white() != self.is_white() and occupant.get_letter() == 'P':
                    return True

        king_move = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dx, dy in king_move:
            king_x = go_to_x + dx
            king_y = go_to_y + dy
            if is_in_range(king_x) and is_in_range(king_y):
                occupant = board.get_figure_from_coords(king_y, king_x)
                if occupant is not None and occupant.is_white() != self.is_white() and occupant.get_letter() == 'K':
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
                    if occupant is not None and occupant.is_white() != self.is_white() and occupant.get_letter() == 'N':
                        return True


        rook_move = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dx, dy in rook_move:
            i = 1
            while is_in_range(go_to_x + i * dx) and is_in_range(go_to_y + i * dy):
                occupant = board.get_figure_from_coords(go_to_y + i * dy, go_to_x + i * dx)

                if occupant is not None and occupant.is_white() != self.is_white() and (occupant.get_letter() == "R" or occupant.get_letter() == "Q"):
                    return True
                elif occupant is not None:
                    break
                i += 1

        bishop_move = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in bishop_move:
            i, j = 1, 1
            while is_in_range(go_to_y + i * dy) and is_in_range(go_to_x + j * dx):
                occupant = board.get_figure_from_coords(go_to_y + i * dy, go_to_x + j * dx)

                if (occupant is not None and occupant.is_white() != self.is_white()
                        and (occupant.get_letter() == 'B'or occupant.get_letter() == 'Q')):
                    return True

                elif occupant is not None:
                    break

                i += 1
                j += 1
        return False


    def get_under_attack(self):
        return self.under_attack

    def set_under_attack(self, under_attack):
        self.under_attack = under_attack

    def can_castle(self, castle_type, board):
        if self.get_moved():
            return False
        if self.get_under_attack():
            return False

        king_y, king_x = self.get_position()

        if castle_type == "Short castle":
            if (board.get_figure_from_coords(king_y, king_x + 3) is None
                    or board.get_figure_from_coords(king_y, king_x + 3).get_moved()):
                return False

            for i in range(1, 3):
                if board.get_figure_from_coords(king_y, king_x + i) is not None:
                    return False
                if self.check_if_under_attack(board, king_y, king_x + i):
                    return False

        else:
            if (board.get_figure_from_coords(king_y, king_x -4) is not None
                    and board.get_figure_from_coords(king_y, king_x -4).get_moved()):
                return False
            for i in range(1, 4):
                if board.get_figure_from_coords(king_y, king_x - i) is not None:
                    return False
                if self.check_if_under_attack(board, king_y, king_x - i):
                    return False

        return True





