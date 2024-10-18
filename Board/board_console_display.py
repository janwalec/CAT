# file just for testing

def print_coords(board):
    for i in board:
        for j in i:
            print(j.coords, end=" ")
        print()

def print_letters(board):
    for i in board:
        for j in i:
            print(j.notation, end=" ")
        print()


def print_pieces(board):
    for i in board:
        for j in i:
            if j.piece is not None:
                print(j.piece.get_letter(), end = "")
                print(j.piece.is_white(), end = " ")
            else:
                print("__", end = " ")
        print()