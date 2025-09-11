from screen_welcome import screen_welcome
from screen_monsterselect import screen_monsterselect
from screen_fight import screen_fight
from screen_result import screen_result

def main():
    screen_welcome()

    screen_monsterselect(True)

    
    screen_fight(True)
    
    screen_result()

if __name__=="__main__":
    main()