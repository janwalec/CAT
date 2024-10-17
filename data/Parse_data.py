import csv
from pathlib import Path


def save_file(file_name, array):
    check_if_exists = Path("games/arr_" + file_name + ".csv")
    if check_if_exists.is_file():
        print("Exists, not saving")
        '''
        arr = []
        with open("games/arr_" + file_name + ".csv", 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                arr.append(row)
        '''

    else:
        print("Doesn't exist, saving")
        with open("games/arr_" + file_name + ".csv", 'w', newline='') as file:
            writer = csv.writer(file)

            for result, moves in array:
                writer.writerow([result, ' '.join(moves)])


def parse_file(file_name):
    games = []

    with open("games/" + file_name + ".pgn", 'r') as file:
        for line in file:

            if line[0] == '[' or line == '\n':
                continue # some statistics
            if '{' in line:
                continue

            curr_game = []
            move_list = line.split()

            game_result = move_list[len(move_list) - 1] # get the result
            move_list.pop(len(move_list) - 1)

            for move in move_list:
                if move.endswith("."):
                    continue # index of a turn (useless)
                curr_game.append(move)

            games.append((game_result, curr_game))

    save_file(file_name, games)


parse_file("lichess_db_standard_rated_2013-01")
