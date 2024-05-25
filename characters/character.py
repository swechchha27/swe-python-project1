from utilities.display import display_dict


class Character:
    
    def __init__(self, name, gender, birth_location, birth_year=2000):  
        self.name = name 
        self.birth_year = birth_year
        self.birth_location = birth_location
        self.gender = gender
        self.age = 0
        self.life_events = []
        self.necessities = {"thirst":10, "hunger":10, "energy":10, "health":10}
        self.emotions = {"anger":0, "sadness":0, "happiness":10, "fear":0}
        self.traits = {"strength":5, "intelligence":5, "charm":5, "confidence":5
                       , "creativity":5, "discipline":5}
        self.skills = {"cooking":0, "reading":0, "writing":0, "music":0, "sports":0
                       , "painting":0, "crafting":0, "persuasion":0, "combat":0
                       , "crime":0, "programming":0, "public_speaking":0}
        
    def create_character(self):
        self.name = input("Enter your character's name: ")
        
    def born(self):  
        print(f"""You are born on {self.birthdate} as a {self.gender}.
              Your parents named you {self.name}.""")
        
    def customize_character(character):
        # Add customization options for the character
        pass

    def age_one_year(self):
        self.age += 1
        self.decrease_needs()
        print(f"{self.name} is now {self.age} years old.")
        self.check_health()

    def decrease_needs(self):
        for need in self.necessities:
            if need != "health":
                self.necessities[need] = max(0, self.necessities[need] - 1)
        display_dict("Necessities", self.necessities)

    def check_health(self):
        if self.necessities['thirst'] == 0 or self.necessities['hunger'] == 0 or self.necessities['energy'] == 0:
            self.necessities['health'] = max(0, self.necessities['health'] - 1)
            print(f"{self.name} is feeling worse. health: {self.necessities['health']}")
        if self.necessities['health'] == 0:
            print(f"{self.name} has died.")
            exit()

    def add_life_event(self, event):
        self.life_events.append(event)

    def display_status(self):
        print(f"Necessities: {self.necessities}")
        print(f"Emotions: {self.emotions}")
        print(f"Traits: {self.traits}")
        print(f"Skills: {self.skills}") 

    def display_life_summary(self):
        print(f"Name: {self.name}")
        print(f"Gender: {self.gender}")
        print(f"Birth Location: (self.birth_location)")
        print(f"Age: {self.age}")
        print("Life Events:")
        for event in self.life_events:
            print(f"  - {event}")
        display_dict("Necessities", self.necessities)
        display_dict("Emotions", self.emotions)
        display_dict("Traits", self.traits)
        display_dict("Skills", self.skills)

    def to_dict(self):
        return {
            "name": self.name,
            "gender": self.gender,
            "birth_location": self.birth_location,
            "age": self.age,
            "life_events": self.life_events,
            "necessities": self.necessities,
            "emotions": self.emotions,
            "traits": self.traits,
            "skills": self.skills
        }
    
    @classmethod
    def from_dict(cls, data):
        character = cls(data["name"], data["gender"], data["birth_location"])
        character.age = data["age"]
        character.life_events = data["life_events"]
        character.necessities = data["necessities"]
        character.emotions = data["emotions"]
        character.traits = data["traits"]
        character.skills = data["skills"]
        return character

  
if __name__ == "__main__":
    c1 = Character()
    c1.create_character()
    c1.born()