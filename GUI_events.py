class Monster:
    def __init__(self, name:str,hp:int):
        self.monster_name=name
        self.monster_type="Deep One"
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
   