from Pieces.Piece import Piece


class Rook(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.set_letter('R')
        self.set_value(5)


    def check_if_move_legal(self, go_to_y, go_to_x, board):
        if go_to_y == self.position[0] and go_to_x == self.position[1]:
            return False # cannot stand on the same field

        occupant = board.get_figure_from_coords(go_to_y, go_to_x)
        if occupant is not None and occupant.is_white() == self.is_white():
            return False  # destination field is an ally

        # some logic expression. wrote it on paper
        '''p, q = False, Falses
        print( (p and not q) or (not p and q) )
        print( (not p or q) and (p or not q) )'''

        p = self.position[1] == go_to_x
        q = self.position[0] == go_to_y
        if (not p or q) and (p or not q):
            return False # wrong direction

        # direction of the move
        sign_y_rook = -1 if (go_to_y - self.position[0] < 0) else 0 if (go_to_y - self.position[0] == 0) else 1
        sign_x_rook = -1 if (go_to_x - self.position[1] < 0) else 0 if (go_to_x - self.position[1] == 0) else 1

        i, j = self.position[0] + sign_y_rook, self.position[1] + sign_x_rook


        while i * abs(sign_y_rook) != go_to_y * abs(sign_y_rook) or j * abs(sign_x_rook) != go_to_x * abs(sign_x_rook):
            if board.get_figure_from_coords(i, j) is not None:
                return False # something was in between rook and destination field
            i += sign_y_rook
            j += sign_x_rook

        return True