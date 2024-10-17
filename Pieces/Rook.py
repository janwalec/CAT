from Pieces.Piece import Piece


class Rook(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.set_letter('R')
        self.set_value(5)


    def check_if_move_legal(self, go_to_y, go_to_x, board):
        if go_to_y == self.position[0] and go_to_x == self.position[1]:
            #print("SAME FIELD")
            return False

        occupant = board.get_figure_from_coords(go_to_y, go_to_x)
        if occupant is not None and occupant.is_white() == self.is_white():
            #print("SAME COLOR")
            return False

        p = self.position[1] == go_to_x
        q = self.position[0] == go_to_y
        if (not p or q) and (p or not q):
            #print("WRONG DIRECTION")
            return False

        sign_y_rook = -1 if (go_to_y - self.position[0] < 0) else 0 if (go_to_y - self.position[0] == 0) else 1
        sign_x_rook = -1 if (go_to_x - self.position[1] < 0) else 0 if (go_to_x - self.position[1] == 0) else 1

        i, j = self.position[0] + sign_y_rook, self.position[1] + sign_x_rook

        while i * abs(sign_y_rook) != go_to_y * abs(sign_y_rook) or j * abs(sign_x_rook) != go_to_x * abs(sign_x_rook):
            if board.get_figure_from_coords(i, j) is not None:
                #print("crossed another piece")
                return False
            i += sign_y_rook
            j += sign_x_rook

        return True