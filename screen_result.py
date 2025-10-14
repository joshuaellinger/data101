# Simple pygame programs

from pygame.locals import *
from ui import *
from datetime import datetime
from game_engine import GameEngine    

class ViewResult(UI_View):
    "display a screen to show progress bar, text, and button widgets"
    def __init__(self, engine:GameEngine):
        super().__init__("viewResult", "Winner")
        self.engine=engine
        self._last_time = datetime.now().time()

    def activate(self, host: UI_Host):

        screen = host.screen
        screen.fill(GRAY)
        #rect1=Label("=== Results ===",(310,80,404,350))
        rect1 = UI_Image("rect1", (310,40,404,110), image="./images/Logo.jpg")
        self.add_element(rect1)
        winner=self.engine.get_winner()
        monster_image = winner.get_image() if winner else ""
        rect1 = UI_Image("rect1", (310,195,404,350), image=monster_image)
        self.add_element(rect1)
        rect1 = UI_Button("rect1", (410,550,200,50), text="Play Again")
        self.add_element(rect1)
        self.rect1 = rect1
        def onclickNext(x: UI_Text):
            host.select_new_view("viewMonsterSelect")
        rect1.onclick = onclickNext
        
    def deactivate(self, host: UI_Host):
        self.clear()

    def tick(self, host:UI_Host):

        # update the time every second
        super().tick(host)

def screen_result():
    host = UI_Host()
    host.register_view(ViewResult())
    host.run_game()
        
if __name__ == "__main__":
    screen_result()