from Pieces.Piece import Piece


class Knight(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.set_letter('N')
        self.set_value(3)


    def check_if_move_legal(self, go_to_y, go_to_x, board):
        occupant = board.get_figure_from_coords(go_to_y, go_to_x)
        if occupant is not None and occupant.is_white() == self.is_white():
            print("SAME COLOR")
            return False
        div_y = abs(self.position[0] - go_to_y)
        div_x = abs(self.position[1] - go_to_x)
        return div_y * div_x == 2
