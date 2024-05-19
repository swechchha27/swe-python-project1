class Character:
    
    def __init__(self):  
        self.name = ""  
        self.birthdate = ""
        self.birthcity = ""
        self.gender = ""
        self.necessities = {"Thirst":10, "Hunger":10, "Energy":10, "Health":10}
        self.emotions = {"Anger":0, "Sadness":0, "Happiness":0, "Fear":0}
        self.traits = {"Strength":0, "Intelligence":0, "Charm":0, "Confidence":0}
        self.skills = {"Cooking":0, "Reading":0, "Writing":0, "Music":0, "Sports":0
                       , "Painting":0, "Crafting":0, "Persuasion":0, "Combat":0
                       , "Crime":0}
        
    def create_character(self):
        self.name = input("Enter your character's name: ")
        
    def born(self):  
        print(f"""You are born on {self.birthdate} as a {self.gender}.
              Your parents named you {self.name}.""")
    
    def display_status(self):
        print(f"Necessities: {self.necessities}")
        print(f"Emotions: {self.emotions}")
        print(f"Traits: {self.traits}")
        print(f"Skills: {self.skills}") 
        
    def customize_character(character):
        # Add customization options for the character
        pass
  
if __name__ == "__main__":
    c1 = Character()
    c1.create_character()
    c1.born()