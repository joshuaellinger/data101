# Simple pygame programs

from pygame.locals import *
from ui import *
from datetime import datetime

class ViewWelcome(UI_View):
    "display a screen to show progress bar, text, and button widgets"
    def __init__(self):
        super().__init__("viewWelcome", "Welcome to MONSTER SMASH")

        self._last_time = datetime.now().time()

    def activate(self, host: UI_Host):

        print("welcome - activate")
        screen = host.screen
        screen.fill(GRAY)
        #rect1 = UI_Image("rect1", (310,40,404,110), image="./images/logo.png")
        rect1 = UI_Image("rect1", (400,40,250,108), image="./images/logo_temp.png")
        self.add_element(rect1)

        self.counter = 0
        self.selected = 0
        self.image_list = ["Owlbear", "DeepOne", "GiantAnt", "Ogre"]

        rect2 = UI_Image("rect2", (310,195,404,350), image=f"./images/owlbear-O.png", border=1)
        self.add_element(rect2)
        self.rect2 = rect2
        def onclickNext(x: UI_Text):
            host.select_new_view("viewMonsterSelect")
        rect2.onclick = onclickNext
        

    def deactivate(self, host: UI_Host):
        self.clear()

    def tick(self, host: UI_Host):
        # update the time every 1/30 of a second
        
        self.counter += 1
        if self.counter > 30*5:
            self.counter = 0
            self.selected += 1
            if self.selected >= len(self.image_list):
                self.selected = 0
            self.rect2.image=f"./images/{self.image_list[self.selected]}.jpg"
        
        super().tick(host)



async def screen_welcome():
    host = UI_Host()
    host.register_view(ViewWelcome())
    await host.run_game()
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(screen_welcome())