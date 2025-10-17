# Simple pygame programs

import pygame
from pygame.locals import *
import time
from ui import *
from game_engine import GameEngine, GameEvents, Monster
from ui.effects import UI_Effect_Burn

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

        self.tick_counter=0
        self.game_over_counter = 0
        
        screen = host.screen
        screen.fill(GRAY)

        title1 = UI_Image("title1", (310,40,404,110, ), image="images/logo.jpg")
        self.add_element(title1)
        self.title1 = title1
        
        textbox = UI_MultiLineText("textbox", (310,170,404,360), font_size=20, 
            border=1, border_color=BLACK)          
        self.add_element(textbox)
        self.textbox = textbox

        self.engine.events=GameEventsGUI(textbox)

        self.engine.start_fight()

        image1 = UI_Image("image1", (30,170,250,250), image=self.engine.m1.get_image(), 
            border=1, border_color=BLACK)
        self.add_element(image1)
        self.image1 = image1
        
        name1 = UI_Text("name1", (30,110,250,50), text=self.engine.m1.name, 
                color=BLACK, background=GRAY, 
                alignment = TextAlignment.Center)
        self.add_element(name1)
        self.name1 = name1

        hp = self.engine.m1.hp
        health1 = UI_ProgressBar("health1", (30,450,250,40), current=hp, maximum=hp,
            border=2, border_color=BLACK)
        self.add_element(health1)
        self.health1 = health1

        stats1 = UI_Text("stats1", (30,490,250,40), text="-- / -- HP", 
            background=GRAY, alignment = TextAlignment.Center)
        self.add_element(stats1)
        self.stats1 = stats1
        
        image2 = UI_Image("image2", (744,170,250,250), image=self.engine.m2.get_image(), 
            border=1, border_color=BLACK)
        self.add_element(image2)
        self.image2 = image2

        name2 = UI_Text("name2", (744,110,250,50), text=self.engine.m2.name, 
            color=BLACK, background=GRAY,
            alignment = TextAlignment.Center)
        self.add_element(name2)
        self.name2 = name2

        hp = self.engine.m2.hp
        health2 = UI_ProgressBar("health2", (744,450,250,40), current=hp, maximum=hp,
            border=2, border_color=BLACK)
        self.add_element(health2)
        self.health2 = health2

        stats2 = UI_Text("stats2", (744,490,250,40), text="-- / -- HP", 
            background=GRAY, alignment = TextAlignment.Center)
        self.add_element(stats2)
        self.stats2 = stats2
        
        checkboxAuto = UI_Checkbox("checkboxAuto", (310,550,187,50), "Auto")
        #on click it switches between auto and manual mode. when manual, the box displays auto. if u click it u go in auto mode and the text changes to manual.
        def onChange(x: UI_Text):
            self.buttonNext.enabled = self.engine.is_game_over() or not self.checkboxAuto.checked 
            self.tick_counter = 0
        checkboxAuto.onchange = onChange
        self.add_element(checkboxAuto)

        self.checkboxAuto = checkboxAuto

        buttonNext = UI_Button("buttonNext", (527,550,187,50 ), "Next >>")
        def onclickNext(x: UI_Text):
            if self.engine.is_game_over():
                if self.game_over_counter >= 5:
                    host.select_new_view("viewResult")
                else:
                    self.update_screen_game_over()
            else:
                self.engine.advance_game_state()
                self.update_screen()

        buttonNext.onclick = onclickNext
        self.buttonNext=buttonNext
        self.add_element(buttonNext)

    def update_screen(self):
        self.health1.current=self.engine.m1.hp
        self.health2.current=self.engine.m2.hp

        self.stats1.text = f"{self.engine.m1.hp}/{self.engine.m1.max_hp}"
        self.stats2.text = f"{self.engine.m2.hp}/{self.engine.m2.max_hp}"

        p = self.engine.m1.hp/self.engine.m1.max_hp
        self.health1.color= RED if p <= .20 else BLUE 
        self.stats1.color= RED if p <= .20 else BLUE 
            
        p = self.engine.m2.hp/self.engine.m2.max_hp
        self.health2.color= RED if p <= .20 else BLUE 
        self.stats2.color= RED if p <= .20 else BLUE 

        self.textbox.show_last_row()

    def update_screen_game_over(self):
        if self.game_over_counter == 0:
            self.checkboxAuto.enabled = False
            self.buttonNext.enabled = False
            winner=self.engine.get_winner()
            if winner != None:
                self.engine.events.print(f"{winner.name} wins with {winner.hp} HP left!")
            else:
                self.engine.events.print("Both die.")
                self.engine.events.print()
            self.textbox.show_last_row()
        elif self.game_over_counter == 2:
            if self.engine.m1.hp <= 0:
                effect = UI_Effect_Burn(self.image1.rect)
                self.add_effect(effect)
            if self.engine.m2.hp <= 0:
                effect = UI_Effect_Burn(self.image2.rect)
                self.add_effect(effect)
        elif self.game_over_counter == 5:
            self.buttonNext.enabled = True

        self.game_over_counter += 1

    def deactivate(self, host: UI_Host):
        self.textbox.clear()
        self.clear()

    def tick(self, host: UI_Host):

        # slow down updates by x10
        if self.tick_counter < 10:
            self.tick_counter += 1  
            super().tick(host)
            return

        self.tick_counter = 0

        if self.engine.is_game_over():
            self.update_screen_game_over()
        else:
            if self.checkboxAuto.checked:
                self.engine.advance_game_state()
            self.update_screen()

        super().tick(host)



def screen_fight(is_started):
    #draw_text(is_started)


    host = UI_Host()
    host.register_view(ViewFight())
    host.run_game()
    
if __name__ == "__main__":
    screen_fight(False)