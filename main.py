from game_manager import GameManager


def test_manually(game_manager):
    # print("# pawn move to a3")
    print(game_manager.translate_chess_notation("a3"))
    print()

    # print("# b takes c3")
    print(game_manager.translate_chess_notation("bxc3+"))
    print()

    # print("# bishop goes to e3")
    print(game_manager.translate_chess_notation("Be3"))
    print()

    # print("# bishop from column d goes to e3")
    print(game_manager.translate_chess_notation("Bde3"))
    print()

    # print("# bishop from field 7 goes to e3 (2 bishops)")
    print(game_manager.translate_chess_notation("B7e3"))
    print()

    # print("# bishop from field d5 goes to e3 (> 2 bishops)")
    print(game_manager.translate_chess_notation("Bd5e3"))
    print()

    # print("# pawn from collumn c takes d7")
    print(game_manager.translate_chess_notation("cxd7"))
    print()

    # print("# pawn from collumn d takes e8")
    print(game_manager.translate_chess_notation("dxe6"))
    print()

    # print("# bishop takes e8")
    print(game_manager.translate_chess_notation("Bxe8"))
    print()

    # print("# bishop from column d takes e8")
    print(game_manager.translate_chess_notation("Bdxe8"))
    print()

    # print("# bishop from column d takes e8")
    print(game_manager.translate_chess_notation("O-O-O+"))
    print()

    print(game_manager.translate_chess_notation("Qxf7#"))
    print()

    print(game_manager.translate_chess_notation("e8=Q+"))
    print()

    print(game_manager.translate_chess_notation("c8=N#"))
    print()

    # print( game_manager.translate_chess_notation("") ) #

def test_automatically(game_manager):
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
        result = game_manager.translate_chess_notation(notation)
        assert result == expected_output, f"Test failed for {notation}: expected '{expected_output}', got '{result}'"

    print("All tests passed!")

game_manager = GameManager()
#game_manager.game_board.print_coords()
#game_manager.game_board.print_letters()

#test_manually(game_manager)
test_automatically(game_manager)




'''a = ""
while a != "*":
    a = input()
    print(game_manager.translate_chess_notation(a))
    a = ""

'''

'''
screen_width, screen_height = 920, 920
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))

running = True
dt = 0


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            pass # event_handler.mouse_interrupt(event)

    pygame.display.flip()

    keys = pygame.key.get_pressed()

    dt = clock.tick(60) / 1000
'''