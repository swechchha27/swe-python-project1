class World:

    def __init__(self):
        self.places = ['Home','School','Hospital','Work']
        self.characters = []

    def add_character(self, character):
        self.characters.append(character)