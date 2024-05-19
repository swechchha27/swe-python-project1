from colorama import Fore, Back, Style
from game_engine import GameEngine

RED = Fore.RED
YELLOW = Fore.YELLOW
GREEN = Fore.GREEN
BLUE = Fore.BLUE
RESET = Fore.RESET
BRIGHT = Style.BRIGHT
RESET_ALL = Style.RESET_ALL

def start_game():
    print(f"****************************************************")
    print(GREEN + f"Welcome to the Game of Life." + RESET_ALL)
    print(f"****************************************************")
    print(Back.BLACK)
    s_continue = input("Would you like to Begin(y/n)? ")
    print(RESET_ALL)
    match s_continue.upper().strip():
        case "Y" : 
            print(f"****************************************************")
            print(Back.GREEN + f"Starting THE GAME OF LIFE." + RESET_ALL)
            print(f"****************************************************")
            game_engine = GameEngine()
            print(BLUE + Back.BLACK)
            game_engine.start()
            print(RESET_ALL)
        case "N" : 
            print(f"****************************************************")
            print(RED + "THE END." + RESET)
            print(f"****************************************************")
        case _ : 
            print(RED + f"Invalid argument '{s_continue}'. Please type 'y' or 'n'." + RESET)
        

if __name__ == '__main__':
    start_game()
    