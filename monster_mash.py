from screen_welcome import ViewWelcome
from screen_monsterselect import ViewMonsterSelect
from screen_fight import ViewFight
from screen_result import ViewResult
from ui import UI_Host

def main():
    host = UI_Host()
    host.register_view(ViewWelcome())
    host.register_view(ViewMonsterSelect())
    host.register_view(ViewFight())
    host.register_view(ViewResult())
    host.run_game()
    
if __name__=="__main__":
    main()