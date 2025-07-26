#
# Sam:
#
#  Look at Amelia's GUI_Events.py implementation and then start changing the engine implementation
#  to use custom classes, instead of dict.
#
#  1. Create a Monster class
#        -- copy the data from the dict into the Monster class
#        -- make sure the rest of the code works on Monster class, not dict
#  2. Create a stub MonsterEvent class
#        -- it should have a single method called print that prints it arguments
#        -- all your print statements should route through this class 
#  3. Create a Fight Class
#        -- this should have the two monsters and an instance of the MonsterEvent class
#        -- this is the top level class that Ruby will call
#
#                             Josh

#To do: Crits, Saving throws, Additional effects

import random
import json
from typing import List

class Attack:
    def __init__(self,action: str,dice: str,to_hit: int, attack_name: str,damage_type:str):
        self.action = action
        self.dice = dice
        self.to_hit = to_hit
        self.attack_name = attack_name
        self.damage_type = damage_type

    def compute_damage(self,ivr:dict)->int:

        x=roll_the_dice(self.dice)
        if self.damage_type in ivr:
            val=ivr[self.damage_type]
            if val=="immune":
                print("*What?*")
                x=0
            elif val=="resists":
                print("*Shrug*")
                x=x//2
            elif val=="vulnerable":
                print("*Ouch*")
                x=x*2
            else:
                raise Exception("invalid value "+val)
        return x
    
    def does_attack_hit(self,AC:int):
        "attacks hit or miss (rolling a d20)"
        to_hit=self.to_hit
        x=random.randint(1,20)
        if x==1: #fumble
            return False
        if x==20: #crit
            return True
        if x+to_hit>=AC:
            return True
        else:
            return False
        
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
    def __init__(self,data:dict):
        self.name = data["Name"]
        self.initiative = 0
        self.hit_dice = data["Hit Dice"]
        self.hp = 0
        self.actions = data["Actions"]
        self.ac = data["AC"]
        self.multiattack = False

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
            attack =Attack(action_name,dice,to_hit, action_name,damage_type)
            result.append(attack)
        
        if self.multiattack:
            return result
        else:
            n=random.randint(0,len(result)-1)
            return [result[n]]


def run_a_fight(monsters:List[Monster]):
    "runs a fight between the first two monsters in the list until one is dead."

    m1=monsters[0]
    m2=monsters[1]
    print(m1.name, "vs.", m2.name)

    fight_order=roll_for_initiative(m1,m2)
    i=1
    for m in fight_order:
        print(m.name, "goes", order_text(i))
        i=i+1

    m1.hp=roll_the_dice(m1.hit_dice)
    print(m1.name, "has", m1.hp, "HP.")
    m2.hp=roll_the_dice(m2.hit_dice)
    print(m2.name, "has", m2.hp, "HP.")
    Round_number=1
    while m1.hp>0 and m2.hp>0:
        print("=== Round",Round_number)
        run_a_round(fight_order)
        Round_number=Round_number+1
        print()

    print()

    if m1.hp>0:
        print(m1.name, "wins with", m1.hp, "HP left!")
    if m2.hp>0:
        print(m2.name, "wins with", m2.hp, "HP left!")
    if m1.hp<=0 and m2.hp<=0:
        print("Both die.")
    print()

def run_a_round(fight_order:List[Monster]):
    "fight a single round"
    for m_active in fight_order:
        m_opponent=find_opponent(fight_order, m_active)
        print(m_active.name, "attacks", m_opponent.name)
        attacks= m_active.get_attacks()
        for a in attacks:
            print(m_active.name, "uses", a.attack_name)
            if a.does_attack_hit(m_opponent.ac):
                dmg=a.compute_damage(m_opponent.ivr)
                m_opponent.hp=m_opponent.hp-dmg
                if dmg== 0:dmg="no"
                print(m_opponent.name, "takes", dmg, a.damage_type, "damage.", m_opponent.name, "has", m_opponent.hp, "HP left.")
                if m_opponent.hp<=0:
                    return
            else:
                print(m_active.name, "misses!")

def roll_the_dice(dice:str):
    #To do: make it read any kind of dice combination
    "rolls dice based on json discription"
    dmgmod=dice.split("d")[1].split("+")[1]
    dmgdice=dice.split("d")[1].split("+")[0]
    rollamount=dice.split("d")[0]
    totaldmg=int(dmgmod)
    for idx in range(int(rollamount)):
        totaldmg=totaldmg+random.randint(1,int(dmgdice))
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

f=open("MonsterStats.json")
text=f.read()
monsters=json.loads(text)
#print(monsters)
monsters = [Monster(m) for m in monsters]
#print(monsters[2].name)

run_a_fight(monsters)

#run_a_fight(monsters)