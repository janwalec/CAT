from Pieces.Piece import Piece

class Pawn(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.set_letter('P')
        self.set_value(1)


    def check_if_move_legal(self, go_to_y, go_to_x, board):
        dir_y = self.position[0] - go_to_y
        if not self.is_white() and dir_y > 0:
            #print("WRONG COLOR DIRECTION")
            return False
        if self.is_white() and dir_y < 0:
            #print("WRONG COLOR DIRECTION")
            return False
        if self.get_moved() and abs(dir_y) > 1:
            #print("WRONG DIRECTION, PAWN HAS ALREADY MOVED")
            return False
        if not self.get_moved() and abs(dir_y) > 2:
            #print("WRONG DIRECTION, MORE THEN 2")
            return False

        dir_x = self.position[1] - go_to_x
        if abs(dir_x) == 1 and abs(dir_y) == 0:
            #print("WRONG DIRECTION, MOVE IN X BUT NOT IN Y")
            return False
        if abs(dir_x) > 1:
            #print("WRONG DIRECTION, MORE THAN 2 IN X AXIS")
            return False
        if abs(dir_x) > 0 and abs(dir_y) == 2:
            #print("WRONG DIRECTION, 2 IN Y AXIS AND MOVE IN X AXIS")
            return False

        occupant = board.get_figure_from_coords(go_to_y, go_to_x)
        if occupant is not None and occupant.is_white() == self.is_white():
            #print("SAME COLOR")
            return False

        if abs(dir_x) == 1 and occupant is None:
            #print("NO FIGURE TO TAKE ON X AXIS")
            return False

        if abs(dir_x) == 0:
            if occupant is not None:
                #print("CROSSED PIECE")
                return False
            if abs(dir_y) == 2:
                if board.get_figure_from_coords(go_to_y + int(dir_y / 2), go_to_x) is not None:
                    #print("CROSSED PIECE")
                    return False

        return True



