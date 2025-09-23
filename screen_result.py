# Simple pygame programs

from pygame.locals import *
from ui import *
from datetime import datetime
from game_engine import GameEngine    

class ViewResult(UI_View):
    "display a screen to show progress bar, text, and button widgets"
    def __init__(self, engine:GameEngine):
        super().__init__("viewResult", "Text/Button/Progress")
        self.engine=engine
        self._last_time = datetime.now().time()

    def activate(self, host: UI_Host):

        screen = host.screen
        screen.fill(GRAY)
        #rect1=Label("=== Results ===",(310,80,404,350))
        rect1 = UI_Button("rect1", (310,80,404,350), text="=== Results ===")
        self.add_element(rect1)
        self.rect1 = rect1
        def onclickNext(x: UI_Text):
            host.select_new_view("viewWelcome")
        rect1.onclick = onclickNext
        
    def deactivate(self, host: UI_Host):
        self.clear()

    def tick(self):
        # update the time every second
        super().tick()

def screen_result():
    host = UI_Host()
    host.register_view(ViewResult())
    host.run_game()
        
if __name__ == "__main__":
    screen_result()