from math import sqrt
from Pieces.Piece import Piece


class King(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.set_letter()

    def set_letter(self):
        self.letter = 'K'

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

        return True
