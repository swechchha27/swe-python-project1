from characters.character import Character
from worlds.world import World
from events.event import user_choice_event, generate_random_event
from utilities.display import display_dict
from utilities.utility import save_game, load_game
import random

class Game:
    def __init__(self):
        self.character = None
        self.world = World()

    def create_character(self, name, gender, birth_origin, birth_year=2000):
        self.character = Character(name, gender, birth_year, birth_origin)

    def create_random_character(self, birth_year=2000):
        character_menu = [
            Character("Lina Rodríguez", "Female", birth_year, "Colombia"),
            Character("Akira Sato", "Female", birth_year, "Japan"),
            Character("Aisha Hassan", "Female", birth_year, "Egypt"),
            Character("Freya Svensson", "Female", birth_year, "Sweden"),
            Character("Nia Johnson", "Female", birth_year, "USA"),
            Character("Dmitri Petrov", "Male", birth_year, "Russia"),
            Character("Mateo Silva", "Male", birth_year, "Brazil"),
            Character("Ravi Sharma", "Male", birth_year, "India"),
            Character("Luca Bianchi", "Male", birth_year, "Italy"),
            Character("Kofi Mensah", "Male", birth_year, "Ghana"),
            Character("Alex Kim", "Non-Binary", birth_year, "South Korea")
        ]
        self.character = random.choice(character_menu)
        age_display = 'newborn' if self.character.age==0 else str(self.character.age)+' year old'
        return (f"You are {self.character.name} , {age_display} {self.character.gender} from {self.character.birth_origin}")

    def run_year(self):
        if self.character:
            self.character.age_one_year()
            if self.character.isAlive:
                if random.random() < 0.5:  # 50% chance of an event occurring
                    generate_random_event(self.character)
                else:
                    user_choice_event(self.character)
            

    def save_game(self, slot):
        save_game(self.character, slot)

    def load_game(self, slot):
        self.character = load_game(slot)
        if self.character:
            print(f"Game loaded from slot {slot}.")
