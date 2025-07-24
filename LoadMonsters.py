#To do: Crits, Saving throws, Additional effects

import random
import json

def run_a_fight(monsters:list):
    "runs a fight between the first two monsters in the list until one is dead."

    m1=monsters[0]
    m2=monsters[1]
    print(m1["Name"], "vs.", m2["Name"])

    fight_order=roll_for_initiative(m1,m2)
    i=1
    for m in fight_order:
        print(m["Name"], "goes", order_text(i))
        i=i+1

    m1["HP"]=roll_the_dice(m1["Hit Dice"])
    print(m1["Name"], "has", m1["HP"], "HP.")
    m2["HP"]=roll_the_dice(m2["Hit Dice"])
    print(m2["Name"], "has", m2["HP"], "HP.")
    Round_number=1
    while m1["HP"]>0 and m2["HP"]>0:
        print("=== Round",Round_number)
        run_a_round(fight_order)
        Round_number=Round_number+1
        print()

    print()

    if m1["HP"]>0:
        print(m1["Name"], "wins with", m1["HP"], "HP left!")
    if m2["HP"]>0:
        print(m2["Name"], "wins with", m2["HP"], "HP left!")
    if m1["HP"]<=0 and m2["HP"]<=0:
        print("Both die.")
    print()

def run_a_round(fight_order:list):
    "fight a single round"
    for m_active in fight_order:
        m_opponent=find_opponent(fight_order, m_active)
        print(m_active["Name"], "attacks", m_opponent["Name"])
        attacks= get_attacks(m_active)
        for a in attacks:
            print(m_active["Name"], "uses", a["attack name"])
            if does_attack_hit(a,m_opponent["AC"]):

                dmg=compute_damage(a)
                m_opponent["HP"]=m_opponent["HP"]-dmg
                print(m_opponent["Name"], "takes", dmg, "damage.", m_opponent["Name"], "has", m_opponent["HP"], "HP left.")
                if m_opponent["HP"]<=0:
                    return
            else:
                print(m_active["Name"], "misses!")

def does_attack_hit(attack:dict,AC:int):
    "attacks hit or miss (rolling a d20)"
    to_hit=attack["to hit"]
    x=random.randint(1,20)
    if x==1: #fumble
        return False
    if x==20: #crit
        return True
    if x+to_hit>=AC:
        return True
    else:
        return False

def get_attacks(monster:dict):
    "get attacks for the monsters"
    result=[]
    has_multiattack= monster["Actions"]["Multiattack"]
    for action in monster["Actions"]:
        if action=="Multiattack":
            continue
        dice=(monster["Actions"][action]["base damage"])
        to_hit=(monster["Actions"][action]["to hit"])
        attack ={"attack name":action, "dice":dice, "to hit":to_hit}
        result.append(attack)
    return result

def roll_the_dice(dice:str):
    #To do: make it read any kind of dice combination
    "rolls dice based on json discription"
    if dice=="1d8+2":
        return random.randint(1,8)+2
    elif dice=="2d8+3":
        return random.randint(1,8)+random.randint(1,8)+3
    elif dice=="2d10":
        return random.randint(1,10)+random.randint(1,10)
    elif dice=="7d10+14":
        x=14
        for idx in range(7):
            x=x+random.randint(1,10)
        return x
    elif dice=="11d8+22":
        x=22
        for idx in range(11):
            x=x+random.randint(1,8)
        return x
    else:
        raise Exception("No dice for"+dice)
    
def compute_damage(attack:dict):
    dice=attack["dice"]
    return roll_the_dice(dice)

    raise Exception("No attacks.")

def find_opponent(monsters: list,current_monster:dict):
    for m in monsters:
        if m ==current_monster: continue
        return m
    raise Exception("No one to fight")

def roll_for_initiative(monster_1:dict,monster_2:dict):    
    "calculates who goes first"
    while True:
        monster_1["initiative"]=random.randint(1,20)
        monster_2["initiative"]=random.randint(1,20)

        if monster_1["initiative"]>monster_2["initiative"]:
            return [monster_1,monster_2]
        elif monster_1["initiative"]<monster_2["initiative"]:
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

run_a_fight(monsters)

#run_a_fight(monsters)