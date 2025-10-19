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
        #rect1 = UI_Image("rect1", (310,40,404,110), image="./images/logo.png")
        rect1 = UI_Image("rect1", (400,40,250,108), image="./images/logo_temp.png")
        self.add_element(rect1)
        winner=self.engine.get_winner()
        monster_image = winner.get_image() if winner else ""
        rect1 = UI_Image("rect1", (100,175,404,350), image=monster_image, border=2, border_color=BLACK)
        self.add_element(rect1)
        
        textDevs = UI_MultiLineText("textDevs", (540,175,404,350), border=2, border_color=BLACK)
        self.add_element(textDevs)
        textDevs.add_line("SmashDevs:")
        textDevs.add_line("")
        textDevs.add_line("  Sam 'The Blonde One' - LASA 2028")
        textDevs.add_line("     D&D Engine")
        textDevs.add_line("")
        textDevs.add_line("  Ruby Ragsdale - LASA 2028")
        textDevs.add_line("     Monster Select")
        textDevs.add_line("")
        textDevs.add_line("  Amelia Saffer - Ann Richards 2028")
        textDevs.add_line("     Fight Screen")
        
        rect1 = UI_Button("rect1", (410,550,200,50), text="Play Again")
        self.add_element(rect1)
        self.rect1 = rect1
        def onclickNext(x: UI_Text):
            host.select_new_view("viewWelcome")
        rect1.onclick = onclickNext
        
    def deactivate(self, host: UI_Host):
        self.clear()

    def tick(self, host:UI_Host):

        # update the time every second
        super().tick(host)

async def screen_result():
    host = UI_Host()
    engine = GameEngine()
    host.register_view(ViewResult(engine))
    await host.run_game()
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(screen_result())