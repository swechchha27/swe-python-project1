

class Item:
    def __init__(self, name, effects) -> None:
        self.name = name
        self.effects = effects
        
    def use(self, character):
        # Apply item effects to character
        pass