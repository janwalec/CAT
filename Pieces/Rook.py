from Pieces.Piece import Piece


class Rook(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.set_letter()

    def set_letter(self):
        self.letter = 'R'