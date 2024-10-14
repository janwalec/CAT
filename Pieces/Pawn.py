from Pieces.Piece import Piece

class Pawn(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.set_letter()

    def set_letter(self):
        self.letter = 'P'

    def check_if_move_legal(self, go_to_y, go_to_x, board):

        if self.position[0] < go_to_y and not self.is_white():
            return False
        if self.position[0] > go_to_y and not self.is_white():
            return False

        return True



