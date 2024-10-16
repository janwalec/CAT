from Managers.display_manager import DisplayManager
from Managers.game_manager import *

game_manager = GameManager()
display_manager = DisplayManager(game_manager)
display_manager.run()

