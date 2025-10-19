from pygame.locals import *
from ui import *
from datetime import datetime

class ViewTooSmall(UI_View):
    "display a screen to tell user that screen is too small"
    def __init__(self):
        super().__init__("viewTooSmall", "No SMASH For You")

    def activate(self, host: UI_Host):

        screen = host.screen
        screen.fill(GRAY)

        w, h = host.screen_size       
        if w > h:
            sz = h - h//2
        else:
            sz = w - w//4
        x, y = (w - sz) // 2, 20

        rect2 = UI_Image("rect2", (x,y,sz,sz), image=f"./images/owlbear-O.png", border=1)
        self.add_element(rect2)

        y += sz + 10
        sz_w, sz_h  = sz, 80
        text1 = UI_MultiLineText("text1", (x, y, sz_w, sz_h), 
            background=GRAY, color=BLACK, font_size=20)
        self.add_element(text1)
        text1.add_line("Your device is too puny")
        text1.add_line("to contain my magnificence.")
        

    def deactivate(self, host: UI_Host):
        self.clear()

    def tick(self, host: UI_Host):
        # update the time every 1/30 of a second
        
        
        super().tick(host)


async def screen_too_small():
    host = UI_Host(width=400,height=800)
    host.register_view(ViewTooSmall())
    await host.run_game()
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(screen_too_small())


