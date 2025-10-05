# Simple pygame programs

import pygame
from pygame.locals import *
import time
from ui import *
from game_engine import GameEngine, GameEvents, next_action, Monster
from typing import List


class GameEventsGUI(GameEvents):
    def __init__(self, display:UI_MultiLineText):
        self.display=display
        super().__init__(self)
    def print(self, msg:str=""):
        self.display.add_line(msg)
    def signal_start_of_round(self, round:int):
        pass

class ViewFight(UI_View):
    "display a screen to show fight match, text, and button widgets"
    def __init__(self, monsters:List[Monster], engine:GameEngine):
        self.monsters=monsters
        self.engine=engine
        super().__init__("viewFight", "FIGHT!!!")

    def activate(self, host: UI_Host):

        screen = host.screen
        screen.fill(GRAY)

        #rect1=Label("monster 1",(30,30,250,590))
        image1 = UI_Image("image1", (30,170,250,250), image="./images/Giant Ant.jpg")
        self.add_element(image1)
        self.image1 = image1
        
        name1 = UI_Text("name1", (30,40,250,100), text="Giant Ant")
        self.add_element(name1)
        self.name1 = name1

        health1 = UI_ProgressBar("health1", (30,450,250,40), current=10, maximum=30)
        self.add_element(health1)
        self.health1 = health1

        stats1 = UI_Text("stats1", (30,490,250,40), text="-- / -- HP")
        self.add_element(stats1)
        self.stats1 = stats1
        
        #rect2=Label("monster 2",(744,30,250,590))
        image2 = UI_Image("image2", (744,170,250,250), image="./images/Deep One.jpg")
        self.add_element(image2)
        self.rect2 = image2

        name2 = UI_Text("name2", (744,40,250,100), text="Deep One")
        self.add_element(name2)
        self.name2 = name2

        health2 = UI_ProgressBar("health2", (744,450,250,40), current=10, maximum=30)
        self.add_element(health2)
        self.health2 = health2

        stats2 = UI_Text("stats2", (744,490,250,40), text="-- / -- HP")
        self.add_element(stats2)
        self.stats2 = stats2
        
        #rect3=Label("fight log",(310,180,404,350))
        rect3 = UI_MultiLineText("rect3", (310,180,404,350))          
        self.add_element(rect3)
        self.rect3 = rect3

        self.engine.events=GameEventsGUI(rect3)
        title1 = UI_Text("title1", (310,55,404,110, ), text="Monster Mash!!!")
        self.add_element(title1)
        self.title1 = title1
        
        #rect4=Label("     auto",(310,550,187,70))
        #rect4 = UI_Text("rect4", (310,550,187,70), text="     Auto")
        #self.add_element(rect4)
        #self.rect4 = rect4

        #label_result=Label("    result",(527,550,187,70))

        
        
        buttonReset = UI_Button("buttonReset", (310,550,187,70), "Manual")
        #on click it switches between auto and manual mode. when manual, the box displays auto. if u click it u go in auto mode and the text changes to manual.
        def onclick(x: UI_Text):
            self.health1.current = 20
            self.health1.color = BLUE
        buttonReset.onclick = onclick
        self.add_element(buttonReset)

        buttonNext = UI_Button("buttonNext", (527,550,187,70 ), "Next >>")
        def onclickNext(x: UI_Text):
            host.select_new_view("viewResult")
        buttonNext.onclick = onclickNext
        self.add_element(buttonNext)

    def deactivate(self, host: UI_Host):
        self.clear()

    def tick(self, host:UI_Host):

        if not next_action(self.monsters, self.engine):
            host.select_new_view("viewResult")
        super().tick()



def screen_fight(is_started):
    #draw_text(is_started)


    host = UI_Host()
    host.register_view(ViewFight())
    host.run_game()
    
if __name__ == "__main__":
    screen_fight(False)