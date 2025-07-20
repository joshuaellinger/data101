#To do: Crits, Saving throws, Additional effects

import random

def run_a_fight(monsters:list):
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
    for m in fight_order:
        m_opponent=find_opponent(fight_order, m)
        print(m["Name"], "attacks", m_opponent["Name"])
        attacks= get_attacks(m)
        for a in attacks:
            print(m["Name"], "uses", a["attack name"])
            if does_attack_hit(a,m_opponent["AC"]):

                dmg=compute_damage(a)
                m_opponent["HP"]=m_opponent["HP"]-dmg
                print(m_opponent["Name"], "takes", dmg, "damage.", m_opponent["Name"], "has", m_opponent["HP"], "HP left.")
                if m_opponent["HP"]<=0:
                    return
            else:
                print(m["Name"], "misses!")

def does_attack_hit(attack:dict,AC:int):
    to_hit=attack["to hit"]
    x=random.randint(1,20)
    if x==1:
        return False
    if x==20:
        return True
    if x+to_hit>=AC:
        return True
    else:
        return False

def get_attacks(m:dict):
    result=[]
    has_multiattack= m["Actions"]["Multiattack"]
    for action in m["Actions"]:
        if action=="Multiattack":
            continue
        dice=(m["Actions"][action]["base damage"])
        to_hit=(m["Actions"][action]["to hit"])
        attack ={"attack name":action, "dice":dice, "to hit":to_hit}
        result.append(attack)
    return result

def roll_the_dice(dice:str):
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
    
def compute_damage(a:dict):
    dice=a["dice"]
    return roll_the_dice(dice)

    raise Exception("No attacks.")

def find_opponent(monsters: list,me:dict):
    for m in monsters:
        if m ==me: continue
        return m
    raise Exception("No one to fight")

def roll_for_initiative(m1:dict,m2:dict):    
    while True:
        m1["initiative"]=random.randint(1,20)
        m2["initiative"]=random.randint(1,20)

        if m1["initiative"]>m2["initiative"]:
            return [m1,m2]
        elif m1["initiative"]<m2["initiative"]:
            return [m2,m1]

def order_text(n:int)->str:
    if n == 1:return "1st"
    if n == 2:return "2nd"
    raise Exception("unexpected number")

f=open("MonsterStats.json")
text=f.read()
import json
monsters=json.loads(text)
#print(monsters)

run_a_fight(monsters)

#run_a_fight(monsters)