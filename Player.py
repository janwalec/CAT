

class Player:
    def __init__(self, is_white):
        self.white = is_white
        self.castling = False
        self.player_pieces = []

    def add_piece(self, piece):
        self.player_pieces.append(piece)


