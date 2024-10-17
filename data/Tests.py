import csv
import os
from pathlib import Path
import time
from Managers.game_manager import *
from Managers.notation_translator import print_move_description
from Managers.game_manager import GameManager


def test_manually():
    # print("# pawn move to a3")
    print(translate_chess_notation("a3"))
    print()

    # print("# b takes c3")
    print(translate_chess_notation("bxc3+"))
    print()

    # print("# bishop goes to e3")
    print(translate_chess_notation("Be3"))
    print()

    # print("# bishop from column d goes to e3")
    print(translate_chess_notation("Bde3"))
    print()

    # print("# bishop from field 7 goes to e3 (2 bishops)")
    print(translate_chess_notation("B7e3"))
    print()

    # print("# bishop from field d5 goes to e3 (> 2 bishops)")
    print(translate_chess_notation("Bd5e3"))
    print()

    # print("# pawn from collumn c takes d7")
    print(translate_chess_notation("cxd7"))
    print()

    # print("# pawn from collumn d takes e8")
    print(translate_chess_notation("dxe6"))
    print()

    # print("# bishop takes e8")
    print(translate_chess_notation("Bxe8"))
    print()

    # print("# bishop from column d takes e8")
    print(translate_chess_notation("Bdxe8"))
    print()

    # print("# bishop from column d takes e8")
    print(translate_chess_notation("O-O-O+"))
    print()

    print(translate_chess_notation("Qxf7#"))
    print()

    print(translate_chess_notation("e8=Q+"))
    print()

    print(translate_chess_notation("c8=N#"))
    print()

    # print( translate_chess_notation("") ) #


def test_automatically():
    tests = [
        ("a3", "Pawn moves a3"),
        ("h4", "Pawn moves h4"),
        ("bxc3+", "Pawn from field b takes c3 and gives check"),
        ("Be3", "Bishop moves e3"),
        ("Bde3", "Bishop from field d moves e3"),
        ("B7e3", "Bishop from field 7 moves e3"),
        ("Bd5e3", "Bishop from field d5 moves e3"),
        ("cxd7", "Pawn from field c takes d7"),
        ("dxe6", "Pawn from field d takes e6"),
        ("Bxe8", "Bishop takes e8"),
        ("Bdxe8", "Bishop from field d takes e8"),
        ("Bd3xe7+", "Bishop from field d3 takes e7 and gives check"),

        ("O-O-O+", "Long castle and gives check"),
        ("O-O", "Short castle"),

        ("Qxf7#", "Queen takes f7 and gives checkmate"),
        ("e8=Q+", "Pawn moves e8 and promotes to Queen and gives check"),
        ("c8=N#", "Pawn moves c8 and promotes to Knight and gives checkmate"),
        ("g8=B", "Pawn moves g8 and promotes to Bishop"),

        ("d4", "Pawn moves d4"),
        ("Nf3", "Knight moves f3"),
        ("dxe5", "Pawn from field d takes e5"),
        ("fxe5", "Pawn from field f takes e5"),
        ("R1e8", "Rook from field 1 moves e8"),
        ("Rxe1", "Rook takes e1"),
        ("Ng5", "Knight moves g5"),
        ("Kf2", "King moves f2"),
        ("Kg1", "King moves g1"),

        ("c3", "Pawn moves c3"),
        ("Nc3", "Knight moves c3"),
        ("Rxe5+", "Rook takes e5 and gives check"),
        ("Qxe5", "Queen takes e5"),
        ("Bd6", "Bishop moves d6"),
        ("Rxe8#", "Rook takes e8 and gives checkmate"),
        ("Qh6", "Queen moves h6"),
        ("Qh8+", "Queen moves h8 and gives check"),
    ]
    for notation, expected_output in tests:
        figure, column, row, action, destination, promotion, is_check, is_checkmate = translate_chess_notation(notation)
        result = print_move_description(figure, column, row, action, destination, promotion, is_check, is_checkmate)
        assert result == expected_output, f"Test failed for {notation}: expected '{expected_output}', got '{result}'"

    print("All tests passed!")


def test_set_of_games(path):
    check_if_exists = Path(path)
    arr = []

    if check_if_exists.is_file():
        print("file exists")
        with open(path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                result = row[0]
                moves = row[1].split()
                arr.append([result, moves])

    else:
        print("file doesnt exist")
        return


    it = 0
    time_start = time.time()
    total_time = time.time()
    for game in arr:

        gm = GameManager("data/starting_position.txt")
        for i in game[1]:
            error_message = gm.process_move(i)
            if not '#' in i and error_message is None:
                print("ERROR")
                print("done ", it, "/", len(arr))
                print(game[1])
                assert error_message is not None, f"Test failed: piece should not be None for game {i}"

        if it % 1000 == 0:
            elapsed_time = time.time() - time_start
            print("done ", it, "/", len(arr), " (", round(100 * it/len(arr), 3), "%)", "took ", round(elapsed_time, 2), "seconds")
            time_start = time.time()
            print("total time:", round(time.time() - total_time, 2), "\n")

        it += 1


        gm = None


test_set_of_games("data/games/arr_lichess_db_standard_rated_2013-01.csv")






