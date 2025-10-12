# Simple pygame programs

import pygame
from pygame.locals import *
import time
from ui import *
from datetime import datetime
from game_engine import GameEngine, Monster



class ViewMonsterSelect(UI_View):
    "display a screen to show image widgets"
    def __init__(self, engine:GameEngine):
        super().__init__("viewMonsterSelect", "SELECT YOUR MONSTER! :D")
        self.engine=engine
        self.m1:Monster=None
        self.m2:Monster=None
        self._last_time = datetime.now().time()

    def activate(self, host: UI_Host):
        screen = host.screen
        screen.fill(GRAY)

        text1 = UI_Text("text1", (40,40+110*2, 350, 50))
        self.add_element(text1)
        self.text1 = text1

        text2 = UI_Text("text2", (40,40+110*3, 350, 50))
        self.add_element(text2)
        self.text2 = text2

        image1 = UI_Image("image1", (40+35,40+55, 100,100))
        self.add_element(image1)

        image2 = UI_Image("image2", (40+220,40+55, 100,100))
        self.add_element(image2)

        buttonFight = UI_Button("buttonFight", (40,40+4*100,150,50), "Fight")
        def onclickFight(x: UI_Element):
            self.engine.select_monsters([self.m1,self.m2])
            host.select_new_view("viewFight")
        buttonFight.onclick = onclickFight
        self.add_element(buttonFight)
        buttonFight.enabled=False

        def onclickSelect(x: UI_Element):
            tag = x.id.replace("button", "")
            if text1.text=="":
                text1.text = f"1: {tag}"
                image1.image = x.background
                self.m1= self.engine.find_monster_by_name(tag)
            else:
                text2.text = f"2:{tag}"
                image2.image = x.background
                buttonFight.enabled=True
                buttonFight.color=RED
                self.m2= self.engine.find_monster_by_name(tag)

        monsters=[]
        idx=0
        for row in range(4):
            monster_row=[]
            for col in range(4):
                if idx >= len(self.engine.available_monsters): 
                    buttonImage = UI_ImageButton(f"m{row}{col}",(500+col*125,87.5+row*125,100,100), image="")
                    buttonImage.enabled=False
                elif col%2==0:
                    m=self.engine.available_monsters[idx]
                    buttonImage = UI_ImageButton(f"{m.name}",(500+col*125,87.5+row*125,100,100), image=m.get_image())
                else:
                    m=self.engine.available_monsters[idx]
                    buttonImage = UI_ImageButton(f"{m.name}",(500+col*125,87.5+row*125,100,100), image=m.get_image())
                buttonImage.onclick = onclickSelect
                self.add_element(buttonImage)
                idx=idx+1

                monster_row.append(buttonImage)
            monsters.append(monster_row)

        buttonClear = UI_Button("buttonClear", (240,40+4*100,150,50), "Clear")
        def onclickClear(x: UI_Element):
            buttonFight.enabled=False
            buttonFight.color=BLACK
            text1.text = ""
            image1.image = ""
            text2.text = ""
            image2.image = ""
        buttonClear.onclick = onclickClear
        self.add_element(buttonClear)
        

    def deactivate(self, host: UI_Host):
        self.text1.text = ""
        pass
    
    def tick(self, host: UI_Host):
        super().tick(host)
    


def screen_monsterselect():
    #draw_text(is_started)
    host=UI_Host()
    host.register_view(ViewMonsterSelect())
    host.run_game()
if __name__ =="__main__":
    screen_monsterselect()