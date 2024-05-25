from game.game import Game

def main():
    print("Welcome to the Life Simulator Game!")

    game = Game()

    while True:
        print("\n1. Create Character")
        print("2. Run Year")
        print("3. Save Game")
        print("4. Load Game")
        print("5. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name: ")
            gender = input("Enter gender: ")
            birth_location = input("Enter birth location: ")
            game.create_character(name, gender, birth_location)
        elif choice == "2":
            game.run_year()
        elif choice == "3":
            slot = int(input("Enter save slot (1-3): "))
            game.save_game(slot)
        elif choice == "4":
            slot = int(input("Enter load slot (1-3): "))
            game.load_game(slot)
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

    game.character.display_life_summary()

if __name__ == "__main__":
    main()
