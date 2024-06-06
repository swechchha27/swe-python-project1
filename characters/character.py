from utilities.display import display_dict, display_with_asterisks
from utilities.utility import get_simple_choice, create_enum
from utilities.constants import GENDERS
# from events.event import Event


class Character:
    
    def __init__(self, name, gender, birth_year=2000, birth_origin='Georgia'):  
        # personal identity
        self.name = name 
        self.birth_year = birth_year
        self.birth_origin = birth_origin
        if gender.lower() not in GENDERS:
            raise ValueError("Invalid gender"+str(GENDERS))
        else:
            self.gender = gender
        self.age = 0

       # Current Status
        self.current_location = ""
        self.house_location = ""
        self.study_location = ""
        self.work_location = ""
        self.credit_score = 100
        self.luck = 0
        self.popularity = 0
        self.notoriety = 0
        self.items_equipped = []  # glossy satin lipstick red, shiny platinum earrings rose-gold
        self.items_in_bag = []
        self.natural_talents = []
        self.special_abilities = []
        self.total_income = 0
        self.total_expenses = 0
        self.credit_card_balance = 0 
        self.isAlive = True
        self.isAttractive = False
        self.isStudent = False
        self.isEmployed = False
        self.hasBusiness = False

        # Physical Appearance
        self.head = []  # normal,round
        self.body = []  # tall, slim
        self.skin = []  # fair, oily
        self.hair = []  # shoulder-length ginger soft-waves
        self.eyes = []
        self.nose = []
        self.lips = []  # color: red, makeup:glossy satin lipstick red
        self.ears = []
        self.neck = []
        self.chest = []
        self.hips = []
        self.hands = []
        self.feet = []
        self.legs = []
        self.belly = []  # tattoo: butterfly

        # Closet
        self.closet = {
            "outer_wear": [], # subtype material type color
            "tops": [],
            "bottoms": [],
            "dresses": [],
            "footwear": [],
            "accessories": {
                "hats": [],
                "bags": [],
                "jewelry": [],
                "belts": [],
                "cosmetics": []
            }
        }

        # Other possessions
        self.pantry = []
        self.cleaning_supplies = []
        self.tools = []
        self.books = []
        self.invaluable_furniture = []

        # Assets
        self.cash = 100
        self.bank_balance = 0
        self.vehicles = {"bikes":[], "cars":[], "ships":[], "jets":[], "others":[]} # name,value
        self.properties = {"houses":[], "plots":[], "commercial":[]} # Name+Location Value
        self.valuables = {"jewellery":[], "paintings":[], "instruments":[], "furniture":[], "rare_items":[], "gear":[], "others":[]}
        self.stocks = []

        # Debts
        self.mortgage = {"bikes":[], "cars":[], "ships":[], "jets":[], "houses":[], "plots":[], "others":[]}
        self.student_loan = 0
        self.business_loan = 0
        self.credit_card_loan = 0

        # Inventory
        self.inventory = []

        # Memories
        self.life_events = []
        self.decisions_made = []

        # Physical and Pscychological Attributes
        self.necessities = {"thirst":10, "hunger":10, "energy":10, "health":10}
        self.emotions = {"anger":0, "sadness":0, "happiness":10, "fear":0}
        self.traits = {"strength":5, "intelligence":5, "charisma":5, "confidence":5
                       , "creativity":5, "discipline":5, "agility":0, "willpower":5}
        
        # Skills and Experiences
        self.skills = {"cooking":0, "reading":0, "writing":0, "music":0, "sports":0
                       , "painting":0, "crafting":0, "persuasion":0, "combat":0
                       , "crime":0, "programming":0, "public_speaking":0}
        
        # Relationships
        self.family = dict()  # Joanna Samson : 99 , Peter Brad : 32
        self.friends = dict()
        self.enemies = dict()
        self.acquaintances = dict()
        self.love_interests = dict()

        # Income Details
        self.monthly_salary = 0
        self.daily_wages = 0
        self.investment_income = 0
        self.pension = 0
        self.pocketmoney = 0

        # Expenditure Details
        self.property_rent = 0
        self.recurring_payments = 0
        self.food_expenses = 0
        self.household_expenses = 0
        self.travel_expenses = 0
        self.fashion_expenses = 0
        self.business_expenses = 0
        self.entertainment_expenses = 0
        self.loan_emis = 0

        # Career History
        self.education_history = {"playschool":{"institute":"", "grades":[], "admit_year":"", "passing_year":"", "subjects":[]}
                                  ,"school":{"institute":"", "grades":[], "admit_year":"", "passing_year":"", "subjects":[]}
                                  ,"highschool":{"institute":"", "grades":[], "admit_year":"", "passing_year":"", "subjects":[]}
                                  , "grad":{"institute":"", "grades":[], "admit_year":"", "passing_year":"", "subjects":[]}
                                  , "post-grad":{"institute":"", "grades":[], "admit_year":"", "passing_year":"", "subjects":[]}
                                  , "diploma":{"institute":"", "grades":[], "admit_year":"", "passing_year":"", "subjects":[]}
                                  , "online":{"institute":"", "grades":[], "admit_year":"", "passing_year":"", "subjects":[]}
                                  }
        self.job_history = dict()  # parttime, from_date, to_date, company, role, years
        self.business_history = dict()  # sidebusiness, from_date, to_date, business_category, role, years

        # Medical History
        self.cured_diseases = []
        self.dormant_diseases = []
        self.current_diseases = []

        # Personal Preferences
        self.likes = []
        self.dislikes = []
        self.hates = []
        self.career_goals = []
        self.financial_goals = []
        self.relationship_goals = []
        self.fitness_goals = []
        self.beauty_goals = []

        
    def born(self):  
        print(f"""You are born on {self.birth_year} as a {self.gender}.
              Your parents named you {self.name}.""")
        
    def customize_character(character):
        display_with_asterisks("Customize your character:")
        character.head=get_simple_choice(create_enum("Head Size", {'S':'Small', 'M':'Medium', 'L':'Large'}),"Head Size: ")
        +" "+get_simple_choice(create_enum("Head Shape", {'O':'Oval', 'D':'Diamond', 'R':'Round', 'S':'Square'}),"Head Shape: ")
        character.body=get_simple_choice(create_enum("Body Size", {'S':'Short', 'M':'Medium', 'T':'Tall'}),"Body Size: ")
        +" "+get_simple_choice(create_enum("Body Type", {'S':'Slim', 'N':'Normal', 'C':'Chubby', 'M':'Fat', 'O':'Overweight'}),"Body Type: ")
        character.skin=get_simple_choice(create_enum("Skin Color", {'F':'White', 'T':'Light', 'B':'Brown', 'D':'Dark'}),"Skin Color: ")
        +" "+get_simple_choice(create_enum("Skin UnderTone", {'Y':'Yellow', 'R':'Red'}),"Skin UnderTone: ")
        +" "+get_simple_choice(create_enum("Skin Type", {'O':'Oily', 'D':'Dry', 'N':'Normal', 'C':'Combination', 'S':'Sensitive'}),"Skin Type: ")
        character.hair=get_simple_choice(create_enum("Hair Length", {'BO':'Bob-cut', 'SH':'Shoulder-Length', 'W':'Waist-Length', 'L':'Long'}),"Hair Length: ")
        +" "+get_simple_choice(create_enum("Hair Color", {'BK':'Black', 'BR':'Brown', 'BL':'Blonde', 'GI':'Ginger'}),"Hair Color: ")
        +" "+get_simple_choice(create_enum("Hair Style", {'WAV':'Soft-Wavy', 'CUR':'Curly', 'AFR':'Afro', 'PON':'Ponytail', 'BRD':'Braided', 'STR':'Straight'}),"Hair Style: ")
        character.eyes=get_simple_choice(create_enum("Eyes Color", {'GR':'Green', 'BL':'Blue', 'BK':'Black', 'BR':'Brown'}),"Eyes Color: ")
        +" "+get_simple_choice(create_enum("Eyes Type", {'AL':'Almond-shaped', 'R':'Round','H':'Hooded','P':'Perfect','AS':'Asian'}),"Eyes Type: ")
        character.nose=get_simple_choice(create_enum("Nose Type", {'LO':'Long', 'BU':'Button', 'PA':'Parrot','P':'Perfect','UP':'Upturned'}),"Nose Type: ")
        character.lips=get_simple_choice(create_enum("Lips Type", {'TH':'Thin','FU':'Full','PO':'Pouty'}),"Lips Type: ")
        character.ears=get_simple_choice(create_enum("Ears Type", {'S':'Small','M':'Medium','L':'Large','E':'Elf-like'}),"Ears Type: ")
        character.neck=get_simple_choice(create_enum("Neck Type", {'L':'Long','S':'Short','SL':'Slim','TH':'Thick'}),"Neck Type: ")
        character.chest=(get_simple_choice(create_enum("Chest Type", {'F':'Flat','P':'Perky','S':'Small','F':'Full','H':'Heavy'}),"Chest Type: ") 
        if (character.gender in ['female'] and character.age > 12) 
        else get_simple_choice(create_enum("Chest Type", {'B':'Broad','N':'Narrow','M':'Muscular'}),"Chest Type: "))
        character.hips=(get_simple_choice(create_enum("Butt Type", {'C':'Curvy','N':'Narrow','A':'Athletic','W':'Wide'}),"Butt Type: ") if (character.age > 12)
        else get_simple_choice(create_enum("Butt Type", {'W':'Wide', 'S':'Small', 'P':'Plumpy'}),"Butt Type: "))
        character.hands=get_simple_choice(create_enum("Hands Type", {'L':'Long','SL':'Slender','SH':'Short','LA':'Large'}),"Hands Type: ")
        character.feet=get_simple_choice(create_enum("Feet Type", {'S':'Small','M':'Medium','L':'Large'}),"Feet Type: ")
        character.legs=get_simple_choice(create_enum("Legs Type", {'S':'Short','L':'Long','MU':'Muscular','SL':'Slim'}),"Legs Type: ")
        character.belly=get_simple_choice(create_enum("Belly Type", {'F':'Flat','R':'Round','P':'Plump','A':'Abs'}),"Belly Type: ")


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
            self.isAlive = False
            print(f"{self.name} has died.")

    def add_life_event(self, event):
        self.life_events.append(event)

    def display_status(self):
        print(f"Necessities: {self.necessities}")
        print(f"Emotions: {self.emotions}")
        print(f"Traits: {self.traits}")
        print(f"Skills: {self.skills}") 

    def display_life_summary(self):
        # print(f"Name: {self.name}")
        # print(f"Gender: {self.gender}")
        # print(f"Birth Location: (self.birth_origin)")
        # print(f"Age: {self.age}")
        # print("Life Events:")
        # for event in self.life_events:
        #     print(f"  - {event}")
        display_dict("Necessities", self.necessities)
        display_dict("Emotions", self.emotions)
        display_dict("Traits", self.traits)
        display_dict("Skills", self.skills)

    def to_dict(self):
        return {
            "name": self.name,
            "gender": self.gender,
            "birth_origin": self.birth_origin,
            "age": self.age,
            # "life_events": [event.to_dict() for event in self.life_events],
            "life_events": self.life_events,
            "necessities": self.necessities,
            "emotions": self.emotions,
            "traits": self.traits,
            "skills": self.skills,
            "cash": self.cash
        }
    
    @classmethod
    def from_dict(cls, data):
        character = cls(data["name"], data["gender"], data["birth_origin"])
        character.age = data["age"]
        # character.life_events = [Event.from_dict(event_data) for event_data in data["life_events"]],
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