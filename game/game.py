from characters.character import Character
from events.event import user_choice_event, generate_random_event
from utilities.display import display_dict
from utilities.utility import save_game, load_game
import random

class Game:
    def __init__(self):
        self.character = None

    def create_character(self, name, gender, birth_location, birth_year=2000):
        self.character = Character(name, gender, birth_year, birth_location)

    def run_year(self):
        if self.character:
            self.character.age_one_year()
            if random.random() < 0.5:  # 50% chance of an event occurring
                event = generate_random_event()
                self.character.add_life_event(event)
                print(f"Event: {event}")
                event.trigger(self.character)
            else:
                user_choice_event(self.character)
        display_dict("Necessities", self.character.necessities)
        display_dict("Emotions", self.character.emotions)
        display_dict("Traits", self.character.traits)
        display_dict("Skills", self.character.skills)

    def save_game(self, slot):
        save_game(self.character, slot)

    def load_game(self, slot):
        self.character = load_game(slot)
        if self.character:
            print(f"Game loaded from slot {slot}.")
