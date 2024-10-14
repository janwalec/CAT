from Pieces.Piece import Piece
from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Bishop import Bishop
from Pieces.Knight import Knight
from Pieces.Queen import Queen
from Pieces.King import King
from Pieces.Field import Field

class GameBoard:
    def __init__(self):
        self.board = self.load_starting_position()

    @staticmethod
    def create_board():
        board = []

        for i in range(0, 8):
            row = []
            for j in range(0, 8):
                field_to_append = Field(i, j)
                field_to_append.set_notation(8 - i, chr(97 + j % 8))
                row.append(field_to_append)
            board.append(row)

        return board

    @staticmethod
    def load_starting_position():
        array = GameBoard.create_board()
        with open("data/test_position.txt", 'r') as file:
            i, j = 0, 0

            for line in file:
                pieces = line.strip().split()
                for piece in pieces:
                    if piece != "##":
                        is_white = 0
                        if piece[1] == 'w':
                            is_white = 1

                        piece_to_add = Piece(-1)

                        match piece[0]:
                            case 'P':
                                piece_to_add = Pawn(is_white)
                            case 'R':
                                piece_to_add = Rook(is_white)
                            case 'B':
                                piece_to_add = Bishop(is_white)
                            case 'N':
                                piece_to_add = Knight(is_white)
                            case 'Q':
                                piece_to_add = Queen(is_white)
                            case 'K':
                                piece_to_add = King(is_white)

                        piece_to_add.set_position(i, j)

                        array[i][j].set_piece(piece_to_add)
                    else:
                        array[i][j].set_piece(None)

                    j += 1
                i += 1
                j = 0
        return array


    def print_coords(self):
        for i in self.board:
            for j in i:
                print(j.coords, end=" ")
            print()

    def print_letters(self):
        for i in self.board:
            for j in i:
                print(j.notation, end = " ")
            print()

    def print_pieces(self):
        for i in self.board:
            for j in i:
                if j.piece is not None:
                    print(j.piece.get_letter(), end = "")
                    print(j.piece.is_white(), end = " ")
                else:
                    print("__", end = " ")
            print()


    def get_figure_from_coords(self, position_y, position_x):
        return self.board[position_y][position_x].get_piece()
    '''
    def get_figure(self, destination):
        destination_column, destination_row = ord(destination[0]) % 97, 8 - int(destination[1])
        return destination_column, destination_row
    '''

