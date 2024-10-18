from Pieces.Piece import Piece

class Pawn(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.set_letter('P')
        self.set_value(1)


    def check_if_move_legal(self, go_to_y, go_to_x, board):
        dir_y = self.position[0] - go_to_y # destinate the direction of white/black pawn
        if not self.is_white() and dir_y > 0:
            return False # black pawns go towards bigger y
        if self.is_white() and dir_y < 0:
            return False # white pawns go toward smaller y

        if self.get_moved() and abs(dir_y) > 1:
            return False # pawn was moved and it wants to go more than 1 squares
        if not self.get_moved() and abs(dir_y) > 2:
            return False # pawn was NOT moved ant it wants to go more than 2 squares

        dir_x = self.position[1] - go_to_x

        if abs(dir_x) == 1 and abs(dir_y) == 0:
            return False # pawns moved only in x-axis
        if abs(dir_x) > 1:
            return False # pawn moved more than 2 squares in x-axis
        if abs(dir_x) > 0 and abs(dir_y) == 2:
            return False # pawn moved 2 squares in y-axis and more than 0 squares in x-axis

        occupant = board.get_figure_from_coords(go_to_y, go_to_x)
        if occupant is not None and occupant.is_white() == self.is_white():
            return False  # destination field is an ally

        if abs(dir_x) == 1 and occupant is None:
            return False # no figure to take on x-axis

        if abs(dir_x) == 0:
            if occupant is not None:
                return False # crossed a piece
            if abs(dir_y) == 2:
                if board.get_figure_from_coords(go_to_y + int(dir_y / 2), go_to_x) is not None:
                    return False # crossed a piece when moving 2 squares

        return True



