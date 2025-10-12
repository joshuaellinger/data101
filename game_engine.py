#Music:
#1. Undertale start menu by Toby Fox
#2. Rito village 8-bit by Loeder
#3. Shriek and Ori 8-bit by CODE: Shadow | Compositions Remixes & Arrangements
#4. Victory by Two steps from hell 1:53-3:13(please change if you find a better one; specifically stuff that's 8-bit/has synth)
#To do: /Crits, /Saving throws, \Additional effects

import random
import json
from typing import List, Union, Tuple
from enum import Enum
from abc import ABC, abstractmethod

class GameEvents(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def print(self, msg:str=""):
        pass
    def signal_start_of_round(self, round:int):
        pass

class GameEventsConsole(GameEvents):
    def __init__(self):
        super().__init__()
    def print(self, msg:str=""):
        print(msg)
    def signal_start_of_round(self, round:int):
        pass

class Attack:
    def __init__(self,action: str,dice: str,to_hit: int, attack_name: str,damage_type:str, effects:dict, events:GameEvents):
        self.action = action
        self.dice = dice
        self.to_hit = to_hit
        self.attack_name = attack_name
        self.damage_type = damage_type
        self.effects = effects
        self.events=events
        
    def compute_damage(self,ivr:dict, crit:bool)->Tuple[int,str]:
        x=roll_the_dice(self.dice,crit)
        if self.damage_type in ivr:
            val=ivr[self.damage_type]
            if val=="immune":
                self.events.print("*What?*")
                x=0
            elif val=="resists":
                self.events.print("*Shrug*")
                x=x//2
            elif val=="vulnerable":
                self.events.print("*Ouch*")
                x=x*2
            else:
                raise Exception("invalid value "+val)
        return x, " "+self.damage_type
    
    def apply_effects(self)->Tuple[int,str,bool]:
        if self.attack_name=="Sting":
            save=self.effects["save"]
            damage=self.effects["damage"]
            dt=self.effects["type"]
            #print(save, damage)
            parts=save.split(",")
            #print(parts[0])
            parts=parts[0].split(" ")
            DC=int(parts[1])
            x=roll_the_dice(damage, False)
            s_f=DC<random.randint(1,20)
            if s_f:
                self.events.print(f"Success against {dt}!")
                x=x//2
            else:
                self.events.print(f"Failure against {dt}.")
            return x, f" {dt}", s_f
        return 0, " ", True

    def does_attack_hit(self,AC:int):
        "attacks hit or miss (rolling a d20)"
        to_hit=self.to_hit
        x=random.randint(1,20)
        if x==1: #fumble
            return False, False
        if x==20: #crit
            return True, True
        if x+to_hit>=AC:
            return True, False
        else:
            return False, False
        
def parse_irv(data:dict,name:str):
    if not(name in data):
        return []
    x=data[name]
    if x==None:
        return []
    if type(x)==str:
        return [x]
    else:
        return x

class Monster:
    def __init__(self,data:dict, events:GameEvents):
        self.name = data["Name"]
        self.initiative = 0
        self.hit_dice = data["Hit Dice"]
        self.creature_type = data["CreatureType"]
        self.hp = 0
        self.max_hp = 0
        self.image_file = data["Image"]
        self.actions = data["Actions"]
        self.ac = data["AC"]
        self.multiattack = False
        self.events=events
        self.conditions={}

        self.ivr = {}
        for x in parse_irv(data,"Immunities"):
            self.ivr[x]="immune"
        for x in parse_irv(data,"Resistances"):
            if x in self.ivr:
                raise Exception(f"{self.name} is already immune to {x}")
            self.ivr[x]="resists"
        for x in parse_irv(data,"Vulnerabilities"):
            if x in self.ivr:
                raise Exception(f"{self.name} is already immune or resistant to {x}")
            self.ivr[x]="vulnerable"

        print(f"create new monster named {self.name}")

    def __str__(self):
        return f"<Monster {self.name}>"
    
    def get_image(self):
        if self.image_file=="":
            return f"./images/Default-{self.creature_type}.jpg"
        else:
            return self.image_file
    
    def update_conditions(self):
        for c in self.conditions.copy():
            n=self.conditions[c]-1
            if n > 0:
                self.conditions[c]=n
            else:
                del self.conditions[c]
                self.events.print(f"{self.name} is no longer {c}ed.")

    def get_attacks(self)->List[Attack]:
        "gets attacks for the monsters"
        result=[]
        for action_name in self.actions:
            data=self.actions[action_name]
            if action_name=="Multiattack":
                self.multiattack = data
                continue
            dice=data["base damage"]
            to_hit=data["to hit"]
            damage_type=data["damage type"] if "damage type" in data else None
            effects=data["effect"] if "effect" in data else None
            attack =Attack(action_name,dice,to_hit, action_name,damage_type, effects, self.events)
            result.append(attack)
        
        if self.multiattack:
            return result
        else:
            n=random.randint(0,len(result)-1)
            return [result[n]]

class GameStateEnum(Enum):
    NEW_GAME=1,
    NEW_ROUND=2,
    TAKE_TURN=3,
    GAME_OVER=4

class GameEngine:

    def __init__(self, events:GameEvents=None):
        self.state=GameStateEnum.NEW_GAME
        self.monster_number=0
        self.attack_number=0
        self.round_number=-1
        self.fight_order:List[Monster]=[]
        self.m_active:Monster=None
        self.events=GameEventsConsole() if events==None else events

        f=open("MonsterStats.json")
        text=f.read()
        monsters=json.loads(text)
        self.available_monsters = [Monster(m, self.events) for m in monsters]
    
    def find_monster_by_name(self, name:str):
        for m in self.available_monsters:
            if m.name==name:
                return m
        raise Exception("could not find monster")

    def select_monsters(self, monsters:List[Monster]): 
        self.m1=monsters[0]
        self.m2=monsters[1]

    def start_fight(self):
        m1=self.m1
        m2=self.m2
        self.events.print(f"{m1.name} vs. {m2.name}")

        self.fight_order=roll_for_initiative(m1,m2)
        i=1
        for m in self.fight_order:
            self.events.print(f"{m.name} goes {order_text(i)}")
            i=i+1

        m1.hp=roll_the_dice(m1.hit_dice, False)
        m1.max_hp=m1.hp
        self.events.print(f"{m1.name} has {m1.hp} HP.")
        m2.hp=roll_the_dice(m2.hit_dice, False)
        m2.max_hp=m2.hp
        self.events.print(f"{m2.name} has {m2.hp} HP.")
        self.round_number=1

    def cancel_fight(self, monsters:List[Monster]):
        self.round_number=-1
        self.fight_order=[]

    def next_action(self):
        m_opponent=find_opponent(self.fight_order, self.m_active)
        self.events.print(f"{self.m_active.name} attacks {m_opponent.name}")
        attacks= self.m_active.get_attacks()
        a=attacks[self.attack_number]
        self.events.print(f"{self.m_active.name} uses {a.attack_name}")
        hit, crit= a.does_attack_hit(m_opponent.ac)
        if hit:
            dmg1,dt1=a.compute_damage(m_opponent.ivr,crit)
            dmg2,dt2,s_f=a.apply_effects()
            if not s_f:
                if dt2.strip() in m_opponent.conditions:
                    self.events.print(f"{m_opponent.name} was{dt2}ed!")
                m_opponent.conditions[dt2.strip()]=10
            m_opponent.hp=m_opponent.hp-dmg1-dmg2
            if dmg1+dmg2== 0: dmgtxt="no"
            elif dmg2==0: dmgtxt=f"{dmg1}{dt1}" 
            else: dmgtxt =f"{dmg1}{dt1} and {dmg2}{dt2}"
            self.events.print(f"{m_opponent.name} takes {dmgtxt} damage. {m_opponent.name} has {m_opponent.hp} HP left.")
            if crit==True: self.events.print("Boom!")
            if m_opponent.hp<=0:
                return False
        else:
            self.events.print(f"{self.m_active.name} misses!")
        return True

    def is_fight_over(self)->bool:
        n_alive=0
        for m in self.fight_order:
            if m.hp>0:
                n_alive+=1
        return n_alive<=1
    
    def get_winner(self)->Union[Monster, None]:
        for m in self.fight_order:
            if m.hp>0:
                return m
        return None

def advance_game_state(engine:GameEngine):
    print("advance", engine.state)
    if engine.state==GameStateEnum.NEW_GAME:
       engine.start_fight()
       engine.state=GameStateEnum.NEW_ROUND 
       return True
    if engine.state==GameStateEnum.NEW_ROUND:
        if not engine.is_fight_over():
            engine.events.signal_start_of_round(engine.round_number)
            engine.events.print(f"=== Round {engine.round_number} ===")
            engine.state=GameStateEnum.TAKE_TURN
            return True
        else:
            engine.state=GameStateEnum.GAME_OVER
            return False
    if engine.state==GameStateEnum.TAKE_TURN:
        
        m_active = engine.fight_order[engine.monster_number]
        engine.m_active=m_active
        m_active.update_conditions()
        c=engine.next_action()
        if c==False:
            engine.state=GameStateEnum.GAME_OVER
            return False
        elif engine.monster_number+1<len(engine.fight_order):
            engine.monster_number+=1
        else:
            engine.monster_number=0
            engine.state=GameStateEnum.NEW_ROUND
            engine.round_number+=1
            engine.events.print()
        return True    
    if engine.state==GameStateEnum.GAME_OVER: 
        return False
    raise Exception(f"unexpected state{engine.state}")

def run_a_fight(monsters:List[Monster], engine:GameEngine):
    "runs a fight between the first two monsters in the list until one is dead."

    
    engine.start_fight(monsters)
    
    while not engine.is_fight_over():
        engine.events.signal_start_of_round(engine.round_number)
        engine.events.print(f"=== Round {engine.round_number} ===")
        run_a_round(engine)
        engine.round_number+=1
        engine.events.print()

    engine.events.print()

    winner=engine.get_winner()
    if winner != None:
        engine.events.print(f"{winner.name} wins with {winner.hp} HP left!")
    else:
        engine.events.print("Both die.")
    engine.events.print()

def run_a_round(engine:GameEngine):
    "fight a single round"
    for m_active in engine.fight_order:
        engine.m_active=m_active
        m_active.update_conditions()
        c=engine.next_action()
        if c==False:
            break

    
def roll_the_dice(dice:str,crit:bool):
    #To do: make it read any kind of dice combination
    "rolls dice based on json discription"

    parts=dice.split("d")
    parts2=parts[1].split("+")
    dmgmod=parts2[1] if len(parts2)==2 else 0
    dmgdice=parts2[0]
    rollamount=parts[0]
    totaldmg=int(dmgmod)
    for idx in range(int(rollamount)):
        totaldmg=totaldmg+random.randint(1,int(dmgdice))
    if crit:
        totaldmg=totaldmg+(int(rollamount)*int(dmgdice))
    return totaldmg

def find_opponent(monsters: list,current_monster:dict)->Monster:
    for m in monsters:
        if m ==current_monster: continue
        return m
    raise Exception("No one to fight")

def roll_for_initiative(monster_1:dict,monster_2:dict):    
    "calculates who goes first"
    while True:
        monster_1.initiative=random.randint(1,20)
        monster_2.initiative=random.randint(1,20)

        if monster_1.initiative>monster_2.initiative:
            return [monster_1,monster_2]
        elif monster_1.initiative<monster_2.initiative:
            return [monster_2,monster_1]

def order_text(n:int)->str:
    "converts fight order into english"
    if n == 1:return "1st"
    if n == 2:return "2nd"
    raise Exception("unexpected number")

#the main program:
def main():

    engine=GameEngine()
    run_a_fight(engine.monsters, engine)

    #run_a_fight(monsters)

if __name__=="__main__":
    main()