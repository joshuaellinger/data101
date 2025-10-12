# Simple pygame programs

import pygame
from pygame.locals import *
import time
from ui import *
from game_engine import GameEngine, GameEvents, advance_game_state, Monster
from typing import List


class GameEventsGUI(GameEvents):
    def __init__(self, display:UI_MultiLineText):
        self.display=display
        super().__init__()
    def print(self, msg:str=""):
        print(msg)
        self.display.add_line(msg)
    def signal_start_of_round(self, round:int):
        pass

class ViewFight(UI_View):
    "display a screen to show fight match, text, and button widgets"
    def __init__(self, engine:GameEngine):
        self.engine=engine
        super().__init__("viewFight", "FIGHT!!!")

    def activate(self, host: UI_Host):

        self.counter=0
        self.go_to_next_screen = False
        self.has_printed_result = False
        
        screen = host.screen
        screen.fill(GRAY)

        rect3 = UI_MultiLineText("rect3", (310,180,404,350))          
        self.add_element(rect3)
        self.rect3 = rect3

        self.engine.events=GameEventsGUI(rect3)

        self.engine.start_fight()

        #rect1=Label("monster 1",(30,30,250,590))
        image1 = UI_Image("image1", (30,170,250,250), image=self.engine.m1.get_image())
        self.add_element(image1)
        self.image1 = image1
        
        name1 = UI_Text("name1", (30,40,250,100), text=self.engine.m1.name)
        self.add_element(name1)
        self.name1 = name1

        hp = self.engine.m1.hp
        health1 = UI_ProgressBar("health1", (30,450,250,40), current=hp, maximum=hp)
        self.add_element(health1)
        self.health1 = health1

        stats1 = UI_Text("stats1", (30,490,250,40), text="-- / -- HP")
        self.add_element(stats1)
        self.stats1 = stats1
        
        #rect2=Label("monster 2",(744,30,250,590))
        image2 = UI_Image("image2", (744,170,250,250), image=self.engine.m2.get_image())
        self.add_element(image2)
        self.rect2 = image2

        name2 = UI_Text("name2", (744,40,250,100), text=self.engine.m2.name)
        self.add_element(name2)
        self.name2 = name2

        hp = self.engine.m2.hp
        health2 = UI_ProgressBar("health2", (744,450,250,40), current=hp, maximum=hp)
        self.add_element(health2)
        self.health2 = health2

        stats2 = UI_Text("stats2", (744,490,250,40), text="-- / -- HP")
        self.add_element(stats2)
        self.stats2 = stats2
        
        #rect3=Label("fight log",(310,180,404,350))

        title1 = UI_Image("title1", (310,55,404,110, ), image="images/Default-Plant.jpg")
        self.add_element(title1)
        self.title1 = title1
        
        #rect4=Label("     auto",(310,550,187,70))
        #rect4 = UI_Text("rect4", (310,550,187,70), text="     Auto")
        #self.add_element(rect4)
        #self.rect4 = rect4

        #label_result=Label("    result",(527,550,187,70))

        
        
        checkbox = UI_Checkbox("checkbox", (310,550,187,70), "Auto")
        #on click it switches between auto and manual mode. when manual, the box displays auto. if u click it u go in auto mode and the text changes to manual.
        def onChecked(x: UI_Text):
            self.checkbox.checked = not self.checkbox.checked
            self.buttonNext.enabled = not self.checkbox.checked
        checkbox.onclick = onChecked
        self.add_element(checkbox)

        self.checkbox = checkbox

        buttonNext = UI_Button("buttonNext", (527,550,187,70 ), "Next >>")
        def onclickNext(x: UI_Text):
            if self.go_to_next_screen:
                host.select_new_view("viewResult")
            if not advance_game_state(self.engine):
                self.go_to_next_screen = True
            self.update_screen(host)

        buttonNext.onclick = onclickNext
        self.buttonNext=buttonNext
        self.add_element(buttonNext)

    def update_screen(self,host):
        if self.engine.is_fight_over() and self.has_printed_result == False:
            winner=self.engine.get_winner()
            if winner != None:
                self.engine.events.print(f"{winner.name} wins with {winner.hp} HP left!")
            else:
                self.engine.events.print("Both die.")
                self.engine.events.print()
            self.has_printed_result = True
        self.health1.current=self.engine.m1.hp
        self.health2.current=self.engine.m2.hp

        self.stats1.text = f"{self.engine.m1.hp}/{self.engine.m1.max_hp}"
        self.stats2.text = f"{self.engine.m2.hp}/{self.engine.m2.max_hp}"

        p = self.engine.m1.hp/self.engine.m1.max_hp
        if p <= .15:
            self.health1.background=RED
        else:
            self.health1.background=BLUE
            
        p = self.engine.m2.hp/self.engine.m2.max_hp
        if p <= .15:
            self.health2.background=RED
        else:
            self.health2.background=BLUE

        self.rect3.show_last_row()

    def deactivate(self, host: UI_Host):
        self.rect3.clear()
        self.clear()

    def tick(self, host: UI_Host):

        if not self.checkbox.checked:
            pass

        elif self.counter<10:
            self.counter+=1
            
        else : 
            self.counter=0

            if not advance_game_state(self.engine):
                self.buttonNext.enabled = True
                self.go_to_next_screen = True
            self.update_screen(host)
        super().tick(host)



def screen_fight(is_started):
    #draw_text(is_started)


    host = UI_Host()
    host.register_view(ViewFight())
    host.run_game()
    
if __name__ == "__main__":
    screen_fight(False)