from screen_welcome import ViewWelcome
from screen_monsterselect import ViewMonsterSelect
from screen_fight import ViewFight
from screen_result import ViewResult
from ui import UI_Host
from game_engine import GameEngine

def main():
    host = UI_Host()
    engine=GameEngine()
    host.register_view(ViewWelcome())
    host.register_view(ViewMonsterSelect(engine))
    host.register_view(ViewFight(engine))
    host.register_view(ViewResult(engine))
    host.run_game()
    
if __name__=="__main__":
    main()