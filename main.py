from Managers.display_manager import DisplayManager
from Managers.game_manager import *

game_manager = GameManager("data/test_position.txt")
display_manager = DisplayManager(game_manager)


game = ['e4', 'e5', 'Nf3', 'Nc6', 'Bc4', 'Nf6', 'Ng5', 'd5', 'exd5', 'Na5', 'Na3', 'Nxc4', 'Nxc4', 'Qxd5', 'Ne3', 'Qc6', 'O-O', 'h6', 'Nf3', 'e4', 'Ne5', 'Qe6', 'd4', 'exd3', 'Nxd3', 'Bd6', 'Rfe1', 'O-O', 'c4', 'Rfd8', 'b4', 'Bxb4', 'Re2', 'b6', 'Qb3', 'Bc5', 'Nxc5', 'bxc5', 'Bb2', 'Rab8', 'Qxb8', 'Ne4', 'Nd5', 'Rxd5', 'cxd5', 'Qxd5', 'Qxc8+', 'Kh7', 'f3', 'Nd2', 'Rd1', 'Nxf3+', 'Kf2', 'Qxd1', 'Qf5+', 'g6', 'Qxf3']

display_manager.run(None)

