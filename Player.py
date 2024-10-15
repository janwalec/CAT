

class Player:
    def __init__(self, is_white):
        self.white = is_white
        self.under_check = False
        self.player_pieces = []
        self.king = None

    def add_piece(self, piece):
        self.player_pieces.append(piece)

    def set_king(self, king):
        self.king = king

    def get_white(self):
        return self.white


