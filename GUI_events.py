#
# Amelia -
#   
#    The next step is to figure out everything you need from the engine to update
#    the display.  I'm thinking the events are:
#         start fight
#         start round
#         start turn
#         attack hit
#         attack miss
#         end turn
#         end round
#         end fight
#
#    Each event should include eough information to show what happen. 
#  
#    You should write a little 'simulated/mock' engine that calls each event and,
#    inside of MonsterEvents, you should print out the message about what happened.
#
#                  Josh


class Monster:
    def __init__(self, name:str,hp:int):
        self.monster_name=name
        self.monster_type=""
        self.max_hp=hp
        self.current_hp=hp

class MonsterEvents:
    def __init__(self):
        pass
    def on_hit(self, m:Monster):
        print(f"{m.monster_name} was hit, {m.current_hp} HP left!!")

def main():
    m1=Monster("Sam",1)
   
    m2=Monster("Amelia",100)
    print (f"{m1.monster_name} vs {m2.monster_name}, FIGHT!!!!")
 
    gui=MonsterEvents()
    gui.on_hit(m1)

main()
   