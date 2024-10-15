from Pieces.Piece import Piece
from Pieces.Bishop import Bishop
from Pieces.Rook import Rook

class Queen(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.set_letter('Q')
        self.set_value(9)


    def check_if_move_legal(self, go_to_y, go_to_x, board):

        b, r = Bishop(self.is_white()), Rook(self.is_white())
        b.set_position(self.position[0], self.position[1])
        r.set_position(self.position[0], self.position[1])

        if not (b.check_if_move_legal(go_to_y, go_to_x, board) or r.check_if_move_legal(go_to_y, go_to_x, board)):
            return False
        b, r = None, None

        return True
