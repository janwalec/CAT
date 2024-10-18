from Pieces.Piece import Piece

class Bishop(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.set_letter('B')
        self.set_value(3)


    def check_if_move_legal(self, go_to_y, go_to_x, board):
        if go_to_y == self.position[0] or go_to_x == self.position[1]:
            return False # cannot stand on the same field

        if not (abs(self.position[0] - go_to_y) == abs(self.position[1] - go_to_x)):
            return False # always goes to the same difference in x- and y-axis
        if not (go_to_x != self.position[1] and go_to_y != self.position[0]):
            return False # bishop cannot go on any same x / same y that is stands on

        occupant = board.get_figure_from_coords(go_to_y, go_to_x)
        if occupant is not None and occupant.is_white() == self.is_white():
            return False # destination field is an ally

        # init for direction
        sign_y = -1 if go_to_y - self.position[0] < 0 else 1
        sign_x = -1 if go_to_x - self.position[1] < 0 else 1
        i, j = self.position[0] + sign_y, self.position[1] + sign_x

        # check path to destination field
        while i != go_to_y and j != go_to_x:
            if board.get_figure_from_coords(i, j) is not None:
                return False # it crossed another piece
            i += sign_y
            j += sign_x

        return True
