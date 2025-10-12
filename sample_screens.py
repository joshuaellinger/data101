# Simple example of using UI_Host

import pygame
from pygame.locals import *
from datetime import datetime, time

from typing import List

from ui import *
from ui.effects import UI_Effect_Fade, UI_Effect_Burn, UI_Effect_Fractal, UI_Effect_Melt

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

        host.play_background_music("./sounds/473_Prison_Block.mp3")

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

        buttonImageGiantAnt = UI_Button("buttonGiantAnt", (40,40,100,100), "", background="./images/Giant Ant.jpg")
        buttonImageGiantAnt.onclick = onclickSelect
        self.add_element(buttonImageGiantAnt)
        buttonImageDeepOne = UI_ImageButton("buttonDeepOne", (40,40+110,100,100), image="./images/Deep One.jpg")
        buttonImageDeepOne.onclick = onclickSelect
        self.add_element(buttonImageDeepOne)

        buttonBack = UI_Button("buttonBack", (40,40+4*100,150,50), "<< Back")
        def onclickBack(x: UI_Element):
            host.select_new_view("view2")
        buttonBack.onclick = onclickBack
        self.add_element(buttonBack)

        buttonNext = UI_Button("buttonNext", (40+150+20,40+4*100,150,50), "Next >>")
        def onclickNext(x: UI_Text):
            host.select_new_view("view4")
        buttonNext.onclick = onclickNext
        self.add_element(buttonNext)

    def deactivate(self, host: UI_Host):
        self.text1.text = ""
        host.stop_music()
        pass
    
    def tick(self, host: UI_Host):
        super().tick(host)

    def update(self, surface: pygame.Surface):        
        super().update(surface)

# ------------------------------------------------------------------

class View4(UI_View):
    "display a screen to show effects"
    def __init__(self):
        super().__init__("view4", "Effects")

        self._effect: UI_Effect = None
        self._last_time = datetime.now().time()
        self.effect_buttons = []

    def activate(self, host: UI_Host):
        screen = host.screen
        screen.fill(GRAY)

        image1 = UI_Image("image1", (40,40, 500,300), border_color=RED)
        self.add_element(image1)
        self.image1 = image1

        buttonAnt = UI_Button("buttonAnt", (40,40+5*100,150,50), "Ant")
        def onclickAnt(x: UI_Text):
            self.image1.image = "images/Giant Ant.jpg"
            self.image1.changed = True
        buttonAnt.onclick = onclickAnt
        self.add_element(buttonAnt)

        buttonBack = UI_Button("buttonBack", (40+200,40+5*100,150,50), "<< Back")
        def onclickBack(x: UI_Element):
            host.select_new_view("view3")
        buttonBack.onclick = onclickBack
        self.add_element(buttonBack)

        self.effect_buttons = []

        # -- helper
        def make_effect_test_button(name, x, y, effect) -> UI_Button:
            button = UI_Button("button" + name, (40+x*200,60+300+y*60,150,50), name)
            self.effect_buttons.append(button)
            def onclick(x: UI_Element):
                image1.border = 2
                for b in self.effect_buttons:
                    b.enabled = False
                           
                effect.reset()
                self.add_effect(effect)
            
                def ondone(effect):
                    #self.redraw()
                    for b in self.effect_buttons:
                        b.enabled = True
                effect.ondone = ondone

            button.onclick = onclick
            return button

        buttonFade = make_effect_test_button("Fade", 0, 0,
            UI_Effect_Fade(image1.rect.inflate(-4,-4))
        )
        self.add_element(buttonFade)

        buttonBurn = make_effect_test_button("Burn", 1, 0,
            UI_Effect_Burn(image1.rect.inflate(-4,-4))
        )
        self.add_element(buttonBurn)

        buttonMelt = make_effect_test_button("Melt", 2, 0,
            UI_Effect_Melt(image1.rect.inflate(-4,-4))
        )
        self.add_element(buttonMelt)

        from ui.effects import FractalNamesEnum
        buttonFractal = make_effect_test_button("Mandel", 0, 1,
            UI_Effect_Fractal(image1.rect.inflate(-4,-4), fractal=FractalNamesEnum.MANDELBRIOT))
        self.add_element(buttonFractal)

        buttonFractal = make_effect_test_button("Julia", 1, 1,
            UI_Effect_Fractal(image1.rect.inflate(-4,-4), fractal=FractalNamesEnum.JULIA, version=3))
        self.add_element(buttonFractal)

        buttonFractal = make_effect_test_button("IFS", 2, 1,
            UI_Effect_Fractal(image1.rect.inflate(-4,-4), fractal=FractalNamesEnum.IFS))
        self.add_element(buttonFractal)

    def deactivate(self, host: UI_Host):
        self.effect_buttons = []
        pass
    
    def tick(self, host: UI_Host):
        super().tick(host)

    def update(self, surface: pygame.Surface):        
        super().update(surface)


# main loop for sample
def main():
    host = UI_Host()
    host.register_view(View1())
    host.register_view(View2())
    host.register_view(View3())
    host.register_view(View4())
    host.run_game("view4")
    
if __name__ == "__main__":
    main()