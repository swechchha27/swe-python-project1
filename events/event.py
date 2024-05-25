import random

class Event:
    def __init__(self, description, effects):
        self.description = description
        self.effects = effects

    def __str__(self):
        return self.description
    
    def to_dict(self):
        return {
            "description": self.description,
            "effects": self.effects
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["description"], data["effects"])

    def trigger(self, character):
        for attribute, change in self.effects.items():
            if attribute in character.necessities:
                self.modify_attribute(character.necessities, attribute, change)
            elif attribute in character.emotions:
                self.modify_attribute(character.emotions, attribute, change)
            elif attribute in character.traits:
                self.modify_attribute(character.traits, attribute, change)
            elif attribute in character.skills:
                self.modify_attribute(character.skills, attribute, change)

    def modify_attribute(self, attributes, attribute, change):
        attributes[attribute] = max(0, min(10, attributes[attribute] + change))
        print(f"{attribute.capitalize()} changed by {change}. New value: {attributes[attribute]}")

    # def learn_skill(self, character):
    #     skill = random.choice(list(character.skills.keys()))
    #     character.skills[skill] += 1
    #     print(f"Learned a new skill: {skill}. Skill level: {character.skills[skill]}")

    # def modify_emotions(self, character):
    #     character.emotions['anger'] = min(10, character.emotions['anger'] + 1)
    #     character.emotions['happiness'] = max(0, character.emotions['happiness'] - 1)
    #     print(f"Had an argument. Anger: {character.emotions['anger']}, Happiness: {character.emotions['happiness']}")

def generate_random_event():
    events = [
        Event("Got sick", {"health": -2}),
        Event("Went on a trip", {"energy": -1, "happiness": 1}),
        Event("Had a big meal", {"hunger": 3}),
        Event("Went to bed early", {"energy": 2}),
        Event("Learned a new skill", {"intelligence": 1}),
        Event("Had an argument", {"anger": 1, "happiness": -1}),
        Event("Won a prize", {"confidence": 2}),
        Event("Started a new hobby", {"crafting": 1, "happiness": 1}),
        Event("Got a promotion", {"confidence": 2, "income": 1})
    ]
    return random.choice(events)

def user_choice_event(character):
    print("You have an important decision to make:")
    choices = {
        "1": ("Go to the gym", {"strength": 1, "energy": -1}),
        "2": ("Read a book", {"intelligence": 1, "happiness": 1}),
        "3": ("Work extra hours", {"income": 1, "energy": -2}),
        "4": ("Take a nap", {"energy": 2, "time_management": 0})
    }
    for key, (description, _) in choices.items():
        print(f"{key}: {description}")

    choice = input("Enter the number of your choice: ")
    if choice in choices:
        description, effects = choices[choice]
        event = Event(description, effects)
        event.trigger(character)
    else:
        print("Invalid choice, no changes made.")
