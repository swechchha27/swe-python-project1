from characters.character import Character
from worlds.world import World
# from events.event import user_choice_event, generate_random_event
from events.event import Event
from utilities.display import display_dict, TextManager
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
            return_text = self.character.age_one_year()
            print(return_text)
            TextManager.add_text(return_text)
            if self.character.isAlive:
                if random.random() < 0.5:  # 50% chance of an event occurring
                    generate_random_event(self.character)
                else:
                    user_choice_event(self.character)
            
def generate_random_event(character):
    health_events = [
        {"preconditions": {"": True, "": False}
         , "description": "Caught a cold."
         , "effects": {"health": -1, "energy": -1}},
        {"preconditions": {"": True, "": False}
         , "description": "Visited a doctor for a check-up."
         , "effects": {"health": +1, "cash": -10}}
    ]
    social_events = [
        {"preconditions": {"": True, "": False}, "description": "Made a new friend.", "effects": {"happiness": +2, "confidence": +1}},
        {"preconditions": {"": True, "": False}, "description": "Had an argument with a friend.", "effects": {"happiness": -2, "anger": +2}}
    ]
    educational_events = [
        {"preconditions": {"": True, "": False}, "description": "Attended a lecture on AI.", "effects": {"intelligence": +2}},
        {"preconditions": {"": True, "": False}, "description": "Failed a test.", "effects": {"intelligence": -1, "confidence": -2}}
    ]
    financial_events = [
        {"preconditions": {"": True, "": False}, "description": "Found a $20 bill on the ground.", "effects": {"cash": +20}},
        {"preconditions": {"": True, "": False}, "description": "Lost your wallet.", "effects": {"cash": -50}}
    ]
    miscellaneous_events = [
        {"preconditions": {"": True, "": False}, "description": "Went on a spontaneous trip.", "effects": {"happiness": +3, "cash": -30}},
        {"preconditions": {"": True, "": False}, "description": "Learned a new hobby.", "effects": {"skills": {"crafting": +1}}}
    ]
    event_pool = {
        "health": health_events,
        "social": social_events,
        "educational": educational_events,
        "financial": financial_events,
        "miscellaneous": miscellaneous_events
    }
    category = random.choices(
        list(Event.event_categories.keys()), 
        weights=list(Event.event_categories.values()), 
        k=1
    )[0]
    available_events = event_pool[category]
    event_data = random.choice(available_events)
    random_event = Event(event_data["description"], event_data["effects"])
    character.add_life_event(random_event)
    return_text="\n" + f"Event: {random_event}"
    print(return_text)
    TextManager.add_text(return_text)
    return_text = "\n" + random_event.trigger(character)
    print(return_text)
    TextManager.add_text(return_text)

def user_choice_event(character):
    print("You have an important decision to make:")
    choices = {
        "1": ("Go to the gym", {"strength": 1, "energy": -1}),
        "2": ("Read a book", {"intelligence": 1, "happiness": 1}),
        "3": ("Work extra hours", {"income": 1, "energy": -2}),
        "4": ("Take a nap", {"energy": 2, "time_management": 0})
    }
    for key, (description, _) in choices.items():
        return_text = "\n" + f"{key}: {description}"
        print(return_text)
        TextManager.add_text(return_text)
    choice = input("Enter the number of your choice: ")
    if choice in choices:
        description, effects = choices[choice]
        event = Event(description, effects)
        event.trigger(character)
    else:
        print("Invalid choice, no changes made.")
    
    def save_game(self, slot):
        save_game(self.character, slot)

    def load_game(self, slot):
        self.character = load_game(slot)
        if self.character:
            print(f"Game loaded from slot {slot}.")
