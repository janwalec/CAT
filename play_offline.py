from Managers.display_manager import DisplayManager
from Managers.game_manager import *

game_manager = GameManager("data/starting_position.txt")
display_manager = DisplayManager(game_manager)

display_manager.run(None)