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
        self.click_counter = 0
        self._last_time = datetime.now().time()

    def four_by_four_grid(self,onclickSelect):
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

        return monsters

    def two_by_two_grid(self, onclickSelect):
        monsters=[]
        idx=0
        for row in range(2):
            monster_row=[]
            for col in range(2):
                if idx >= len(self.engine.available_monsters): 
                    buttonImage = UI_ImageButton(f"m{row}{col}",(500+col*100,40+row*160,150,150), image="")
                    buttonImage.enabled=False
                else:
                    m=self.engine.available_monsters[idx]
                    buttonImage = UI_ImageButton(f"{m.name}",(500+col*160,40+row*160,150,150), image=m.get_image())
                buttonImage.onclick = onclickSelect
                self.add_element(buttonImage)
                idx=idx+1

                monster_row.append(buttonImage)
            monsters.append(monster_row)
            
        return monsters

    def three_by_three_grid(self, onclickSelect):
        monsters=[]
        idx=0
        for row in range(3):
            monster_row=[]
            for col in range(3):
                if idx >= len(self.engine.available_monsters): 
                    buttonImage = UI_ImageButton(f"m{row}{col}",(510+col*160,40+row*160,150,150), image="")
                    buttonImage.enabled=False
                else:
                    m=self.engine.available_monsters[idx]
                    buttonImage = UI_ImageButton(f"{m.name}",(510+col*160,40+row*160,150,150), image=m.get_image())
                buttonImage.onclick = onclickSelect
                self.add_element(buttonImage)
                idx=idx+1

                monster_row.append(buttonImage)
            monsters.append(monster_row)
            
        return monsters

    def activate(self, host: UI_Host):

        self.click_counter = 0

        screen = host.screen
        screen.fill(GRAY)

        image1 = UI_Image("image1", (40,40, 200,200), border=1, border_color=BLACK)
        self.add_element(image1)

        text1 = UI_Text("text1", (30,40+220, 220, 40), color=BLACK, background=GRAY,
          alignment = TextAlignment.Center)
        self.add_element(text1)
        self.text1 = text1

        image2 = UI_Image("image2", (40+220,40, 200,200), border=1, border_color=BLACK)
        self.add_element(image2)

        text2 = UI_Text("text2", (30+220,40+220, 220, 40), color=BLACK, background=GRAY,
          alignment = TextAlignment.Center)
        self.add_element(text2)
        self.text2 = text2

     

        buttonFight = UI_Button("buttonFight", (40,40+4*100,150,50), "Fight")
        def onclickFight(x: UI_Element):
            self.engine.select_monsters([self.m1,self.m2])
            host.select_new_view("viewFight")
        buttonFight.onclick = onclickFight
        self.add_element(buttonFight)
        buttonFight.enabled=False
        self.buttonFight = buttonFight

        def onclickSelect(x: UI_Element):
            tag = x.id.replace("button", "")
            if self.click_counter == 0:
                text1.text = f"{tag}"
                image1.image = x.background
                self.m1= self.engine.find_monster_by_name(tag)
                self.click_counter = 1
            else:
                text2.text = f"{tag}"
                image2.image = x.background
                buttonFight.enabled=True
                buttonFight.color=RED
                self.m2= self.engine.find_monster_by_name(tag)
                self.click_counter = 0

        #monsters=self.four_by_four_grid()
        #monsters=self.two_by_two_grid(onclickSelect)
        monsters=self.three_by_three_grid(onclickSelect)

        buttonClear = UI_Button("buttonClear", (240,40+4*100,150,50), "Clear")
        def onclickClear(x: UI_Element):
            buttonFight.enabled=False
            buttonFight.color=BLACK
            text1.text = ""
            image1.image = ""
            text2.text = ""
            image2.image = ""
            self.click_counter = 0
        buttonClear.onclick = onclickClear
        self.add_element(buttonClear)
        

    def deactivate(self, host: UI_Host):
        self.text1.text = ""
        self.click_counter = 0
        self.buttonFight.color = BLACK
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