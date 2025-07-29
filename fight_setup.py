# 
# Ruby -- Make the simplest possible fight setup
#  
#  To run a fight, we want to:
#     1. print the monster list.
#     2. have player 1 pick a monster
#     2. have player 2 pick a monster
#     3. if the monsters are the same, refuse to fight and ask them both to pick new monsters
#     4. call Sam's game engine
#     5. print the winner
#
#  For initial development, use the 'mock' run_a_fight functio below so you don't need
#  to access Sam or Amelia's code.
#
#                           Josh
#

def load_monster_names():
    
    # read and parse the json file
    import json
    with open("MonsterStats.json") as f:
        monsters = json.load(f)

    # get the name for each monster
    name_list = []
    for m in monsters:
        name_list.append(m["Name"])
    return name_list

def run_a_fight(monster_1: str, monster_2: str) -> str:
    "mock right engine"
    import random
    flip = random.randint(0, 1)
    return monster_1 if flip == 0 else monster_2 

def main():

    # get the monster list
    monsters = load_monster_names()
    print(monsters)

    # read a string entered by the user
    n = input("Type Something: ")
    print(n)

main()
