
#To do: Crits, Saving throws, Additional effects

import random
import json
from typing import List, Union


class GameEvents:
    def __init__(self):
        pass
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
        
    def compute_damage(self,ivr:dict, crit:bool)->int:
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
        return x
    
    def apply_effects(self):
        if self.attack_name=="Sting":
            save=self.effects["save"]
            damage=self.effects["damage"]
            #print(save, damage)
            parts=save.split(",")
            #print(parts[0])
            parts=parts[0].split(" ")
            DC=int(parts[1])
            x=roll_the_dice(damage, False)
            if DC>random.randint(1,20):
                self.events.print("Success against poison!")
                x=x//2
            else:
                self.events.print("Failure against poison.")
            self.events.print(f"Took {x} poison damage.")
            return x
        return 0

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
        self.hp = 0
        self.actions = data["Actions"]
        self.ac = data["AC"]
        self.multiattack = False
        self.events=events

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

class GameEngine:

    def __init__(self):
        self.round_number=-1
        self.fight_order:List[Monster]=[]
        self.m_active:Monster=None
        self.events=GameEvents()

    def get_monster_list(self)->List[Monster]:
        return []
    
    def start_fight(self, monsters:List[Monster]):
        m1=monsters[0]
        m2=monsters[1]
        self.events.print(f"{m1.name} vs. {m2.name}")

        self.fight_order=roll_for_initiative(m1,m2)
        i=1
        for m in self.fight_order:
            self.events.print(f"{m.name} goes {order_text(i)}")
            i=i+1

        m1.hp=roll_the_dice(m1.hit_dice, False)
        self.events.print(f"{m1.name} has {m1.hp} HP.")
        m2.hp=roll_the_dice(m2.hit_dice, False)
        self.events.print(f"{m2.name} has {m2.hp} HP.")
        self.round_number=1

    def cancel_fight(self, monsters:List[Monster]):
        self.round_number=-1
        self.fight_order=[]

    def next_action(self):
        m_opponent=find_opponent(self.fight_order, self.m_active)
        self.events.print(f"{self.m_active.name} attacks {m_opponent.name}")
        attacks= self.m_active.get_attacks()
        for a in attacks:
            self.events.print(f"{self.m_active.name} uses {a.attack_name}")
            hit, crit= a.does_attack_hit(m_opponent.ac)
            if hit:
                dmg=a.compute_damage(m_opponent.ivr,crit)
                dmg+=a.apply_effects()
                m_opponent.hp=m_opponent.hp-dmg
                if dmg== 0:dmg="no"
                dt = "" if a.damage_type==None else " "+a.damage_type
                self.events.print(f"{m_opponent.name} takes {dmg}{dt} damage. {m_opponent.name} has {m_opponent.hp} HP left.")
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

def find_opponent(monsters: list,current_monster:dict):
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
    f=open("MonsterStats.json")
    text=f.read()
    monsters=json.loads(text)
    #print(monsters)
    monsters = [Monster(m,engine.events) for m in monsters]
    #print(monsters[2].name)

    run_a_fight(monsters, engine)

    #run_a_fight(monsters)

if __name__=="__main__":
    main()