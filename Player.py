

class Player:
    def __init__(self, is_white):
        self.white = is_white
        self.under_check = False
        self.player_pieces = []
        self.king = None
        self.last_move_piece = None
        self.last_move_og_field_y, self.last_move_og_field_x = None, None
        self.last_move_new_field_y, self.last_move_new_field_x = None, None

    def add_piece(self, piece):
        self.player_pieces.append(piece)

    def set_king(self, king):
        self.king = king

    def get_white(self):
        return self.white

    def set_last_move(self, piece, y, x, go_to_y, go_to_x):
        self.last_move_piece = piece
        self.last_move_og_field_y, self.last_move_og_field_x = y, x
        self.last_move_new_field_y, self.last_move_new_field_x = go_to_y, go_to_x

    def get_last_move(self):
        return (self.last_move_piece,
                self.last_move_og_field_y, self.last_move_og_field_x,
                self.last_move_new_field_y, self.last_move_new_field_x)

    def print_last_move(self):
        if self.white:
            print("white", end = " ")
        else:
            print("black", end = " ")
        print("moved " + self.last_move_piece.get_letter(), end = " ")
        print("from (", self.last_move_og_field_y, self.last_move_og_field_x, end = " ) ")
        print("to (", self.last_move_new_field_y, self.last_move_new_field_x, end = " )\n")



