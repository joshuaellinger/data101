# Simple example of using UI_Host

import pygame
from pygame.locals import *
from datetime import datetime, time

from typing import List

from ui import *

class View1(UI_View):
    "display a screen to show progress bar, text, and button widgets"
    def __init__(self):
        super().__init__("view1", "Text/Button/Progress")

        self._last_time = datetime.now().time()

    def activate(self, host: UI_Host):

        screen = host.screen
        screen.fill(GRAY)

        self.last_time = datetime.now()
        label = UI_Text("label1", (40,40,150,50), text="...")
        self.add_element(label)
        self.label = label


        progress1 = UI_ProgressBar("progress1", (40,40+2*75,150,50))
        self.add_element(progress1)
        self.progress1 = progress1

        checkbox1 = UI_Checkbox("checkbox1", (40,40+4*75, 150, 50), text="run", checked=True)
        self.add_element(checkbox1)
        self.checkbox1 = checkbox1

        progress2 = UI_ProgressBar("progress2", (40+200,40,50,150), 
            current=20, maximum=20,
            orientation=Orientation.Vertical)
        self.add_element(progress2)
        self.progress2 = progress2
        
        buttonReset = UI_Button("buttonReset", (40,40+75,150,50), "Reset")
        def onclick(x: UI_Text):
            self.progress2.current = 20
            self.progress2.color = BLUE
        buttonReset.onclick = onclick
        self.add_element(buttonReset)

        buttonNext = UI_Button("buttonNext", (40,40+3*75,150,50), "Next >>")
        def onclickNext(x: UI_Text):
            host.select_new_view("view2")
        buttonNext.onclick = onclickNext
        self.add_element(buttonNext)

    def deactivate(self, host: UI_Host):
        self.clear()

    def tick(self, host: UI_Host):
        t = datetime.now()

        if not self.checkbox1.checked:
            self.last_time = t
        else: 
            # update the time every second
            diff = t - self.last_time
            if diff.total_seconds() >= 1: 
                self.label.text = f"{t.hour:02d}:{t.minute:02d}:{t.second:02d}"
                self.last_time = t
                self.progress1.current += 1
                self.progress2.current -= 1
                if self.progress2.percentage <= 0.5:
                    self.progress2.color = RED 

        super().tick(host)

# ------------------------------------------------------------------

class View2(UI_View):
    "display a screen to show scrolling text widget"
    def __init__(self):
        super().__init__("view2", "ScrollingText")

        self._line_num = 0
        self._last_time = datetime.now()

    def activate(self, host: UI_Host):
        screen = host.screen
        screen.fill(GRAY)

        self._line_num = 0

        textBox1 = UI_MultiLineText("textBox1", (40, 40, 440, 335))
        self.add_element(textBox1)
        self.textBox1 = textBox1

        buttonBack = UI_Button("buttonBack", (40,40+5*75,150,50), "<< Back")
        def onclickBack(x: UI_Text):
            host.select_new_view("view1")
        buttonBack.onclick = onclickBack
        self.add_element(buttonBack)

        buttonNext = UI_Button("buttonNext", (40+150+20,40+5*75,150,50), "Next >>")
        def onclickNext(x: UI_Text):
            host.select_new_view("view3")
        buttonNext.onclick = onclickNext
        self.add_element(buttonNext)

    def deactivate(self, host: UI_Host):
        self.textBox1.clear()
        self.textBox1.deactivate()
    
    def tick(self, host: UI_Host):

        # add a row every second and scroll when full up to 20
        t = datetime.now()
        diff = t - self._last_time
        if diff.total_seconds() >= 0.10 and self._line_num <= 20: 
            self._line_num += 1
            self.textBox1.add_line(f"Line #{self._line_num}")
            self.textBox1.show_last_row()
            self._last_time = t

        super().tick(host)


# ------------------------------------------------------------------

class View3(UI_View):
    "display a screen to show image widgets"
    def __init__(self):
        super().__init__("view3", "Images")
        self._last_time = datetime.now().time()

    def activate(self, host: UI_Host):
        screen = host.screen
        screen.fill(GRAY)


        text1 = UI_Text("text1", (40,40+110*2, 350, 50))
        self.add_element(text1)
        self.text1 = text1

        image1 = UI_Image("image1", (40+150,40+55, 100,100), border_color=RED)
        self.add_element(image1)
        self.image1 = image1

        def onclickSelect(x: UI_Element):
            tag = x.id.replace("button", "")
            text1.text = f"Selected {tag}"
            image1.image = x.background

        buttonImageGiantAnt = UI_Button("buttonGiantAnt", (40,40,100,100), "", background="./images/GiantAnt.jpg")
        buttonImageGiantAnt.onclick = onclickSelect
        self.add_element(buttonImageGiantAnt)
        buttonImageDeepOne = UI_ImageButton("buttonDeepOne", (40,40+110,100,100), image="./images/DeepOne.jpg")
        buttonImageDeepOne.onclick = onclickSelect
        self.add_element(buttonImageDeepOne)

        buttonBack = UI_Button("buttonBack", (40,40+4*100,150,50), "<< Back")
        def onclickBack(x: UI_Element):
            host.select_new_view("view2")
        buttonBack.onclick = onclickBack
        self.add_element(buttonBack)

    def deactivate(self, host: UI_Host):
        self.text1.text = ""
        host.stop_music()
        pass
    
    def tick(self, host: UI_Host):
        super().tick(host)

    def update(self, surface: pygame.Surface):        
        super().update(surface)

# ------------------------------------------------------------------


# main loop for sample
async def main():
    host = UI_Host()
    host.register_view(View1())
    host.register_view(View2())
    host.register_view(View3())
    await host.run_game("view3")
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
