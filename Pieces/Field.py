

class Field:
    def __init__(self, y, x):
        self.coords = (y, x)
        self.piece = None
        self.notation = ('*', '*')

    def set_notation(self, num, char):
        self.notation = (num, char)

    def set_piece(self, piece):
        self.piece = piece

    def get_piece(self):
        return self.piece