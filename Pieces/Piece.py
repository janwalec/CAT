
class Piece:
    def __init__(self, is_white):
        self.killed = False
        self.white = is_white
        self.position = (0, 0)
        self.letter = '*'

    def set_position(self, y, x):
        self.position = (y, x)

    def get_position(self):
        return self.position

    def set_killed(self, is_killed):
        self.killed = is_killed

    def is_white(self):
        return self.white

    def is_killed(self):
        return self.killed

    def move(self, position):
        raise Exception("NotImplementedException")

    def check_if_move_legal(self, position, board):
        raise Exception("NotImplementedException")

    def set_letter(self):
        raise Exception("NotImplementedException")

    def get_letter(self):
        return self.letter