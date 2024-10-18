from enum import Enum
from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Bishop import Bishop
from Pieces.Knight import Knight
from Pieces.Queen import Queen
from Pieces.King import King

# to get classes from letters (isinstance)
class PE(Enum):
    P = Pawn
    R = Rook
    N = Knight
    Q = Queen
    K = King
    B = Bishop

def get_class_from_list(letter, list_of_pieces):
    piece_class = PE[letter].value
    return [piece for piece in list_of_pieces if isinstance(piece, piece_class)]