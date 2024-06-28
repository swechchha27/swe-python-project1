from characters.character import Character
import random

class Event:
    event_categories = {
        "health": 0.2,
        "social": 0.3,
        "educational": 0.2,
        "financial": 0.2,
        "miscellaneous": 0.1
    }
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
        return_text = ""
        for attribute, change in self.effects.items():
            if attribute in character.necessities:
                return_text += "\n" + self.modify_attribute(character.necessities, attribute, change)
            elif attribute in character.emotions:
                return_text += "\n" + self.modify_attribute(character.emotions, attribute, change)
            elif attribute in character.traits:
                return_text += "\n" + self.modify_attribute(character.traits, attribute, change)
            elif attribute in character.skills:
                return_text += "\n" + self.modify_attribute(character.skills, attribute, change)
            elif attribute == "cash":
                character.cash = character.cash + change
            # handle nested dictionaries for skills
            elif attribute == "skills":
                for skill, skill_change in change.items():
                    if skill in character.skills:
                        character.skills[skill] = max(0, character.skills[skill] + skill_change)
        return return_text

    def modify_attribute(self, attributes, attribute, change):
        attributes[attribute] = max(0, min(10, attributes[attribute] + change))
        return_text="\n" + f"{attribute.capitalize()} changed by {change}. New value: {attributes[attribute]}"
        return return_text

    # def learn_skill(self, character):
    #     skill = random.choice(list(character.skills.keys()))
    #     character.skills[skill] += 1
    #     print(f"Learned a new skill: {skill}. Skill level: {character.skills[skill]}")

    # def modify_emotions(self, character):
    #     character.emotions['anger'] = min(10, character.emotions['anger'] + 1)
    #     character.emotions['happiness'] = max(0, character.emotions['happiness'] - 1)
    #     print(f"Had an argument. Anger: {character.emotions['anger']}, Happiness: {character.emotions['happiness']}")

# def generate_random_event(character):
#     health_events = [
#         {"preconditions": {"": True, "": False}
#          , "description": "Caught a cold."
#          , "effects": {"health": -1, "energy": -1}},
#         {"preconditions": {"": True, "": False}
#          , "description": "Visited a doctor for a check-up."
#          , "effects": {"health": +1, "cash": -10}}
#     ]
#     social_events = [
#         {"preconditions": {"": True, "": False}, "description": "Made a new friend.", "effects": {"happiness": +2, "confidence": +1}},
#         {"preconditions": {"": True, "": False}, "description": "Had an argument with a friend.", "effects": {"happiness": -2, "anger": +2}}
#     ]
#     educational_events = [
#         {"preconditions": {"": True, "": False}, "description": "Attended a lecture on AI.", "effects": {"intelligence": +2}},
#         {"preconditions": {"": True, "": False}, "description": "Failed a test.", "effects": {"intelligence": -1, "confidence": -2}}
#     ]
#     financial_events = [
#         {"preconditions": {"": True, "": False}, "description": "Found a $20 bill on the ground.", "effects": {"cash": +20}},
#         {"preconditions": {"": True, "": False}, "description": "Lost your wallet.", "effects": {"cash": -50}}
#     ]
#     miscellaneous_events = [
#         {"preconditions": {"": True, "": False}, "description": "Went on a spontaneous trip.", "effects": {"happiness": +3, "cash": -30}},
#         {"preconditions": {"": True, "": False}, "description": "Learned a new hobby.", "effects": {"skills": {"crafting": +1}}}
#     ]
#     event_pool = {
#         "health": health_events,
#         "social": social_events,
#         "educational": educational_events,
#         "financial": financial_events,
#         "miscellaneous": miscellaneous_events
#     }
#     category = random.choices(
#         list(Event.event_categories.keys()), 
#         weights=list(Event.event_categories.values()), 
#         k=1
#     )[0]
#     available_events = event_pool[category]
#     event_data = random.choice(available_events)
#     random_event = Event(event_data["description"], event_data["effects"])
#     character.add_life_event(random_event)
#     print(f"Event: {random_event}")
#     random_event.trigger(character)


# def user_choice_event(character):
#     print("You have an important decision to make:")
#     choices = {
#         "1": ("Go to the gym", {"strength": 1, "energy": -1}),
#         "2": ("Read a book", {"intelligence": 1, "happiness": 1}),
#         "3": ("Work extra hours", {"income": 1, "energy": -2}),
#         "4": ("Take a nap", {"energy": 2, "time_management": 0})
#     }
#     for key, (description, _) in choices.items():
#         print(f"{key}: {description}")

#     choice = input("Enter the number of your choice: ")
#     if choice in choices:
#         description, effects = choices[choice]
#         event = Event(description, effects)
#         event.trigger(character)
#     else:
#         print("Invalid choice, no changes made.")
