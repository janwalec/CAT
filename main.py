from Managers.display_manager import DisplayManager
from Managers.game_manager import *

game_manager = GameManager("data/starting_position.txt")
display_manager = DisplayManager(game_manager)


game = ['d4', 'd6', 'e4', 'Nd7', 'Bb5', 'c6', 'Bc4', 'e5', 'd5', 'Ngf6', 'Bg5', 'h6', 'Bh4', 'c5', 'Qf3', 'a6', 'a4', 'Qb6', 'b3', 'Qa5+', 'Nd2', 'b5', 'Be2', 'Be7', 'Bxf6', 'Bxf6', 'Qh3', 'Bg5', 'Nf3', 'Nf6', 'Qg3', 'Nxe4', 'Rd1', 'Nxg3', 'fxg3', 'Be3', 'Nh4', 'bxa4', 'Nf5', 'Bxf5', 'bxa4', 'Bxc2', 'Ra1', 'Qxd2+', 'Kf1', 'Bd3', 'Re1', 'Rb8']

display_manager.run(game)

