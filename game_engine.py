from character import Character

class GameEngine:
    def __init__(self):
        self.is_running = True
        self.character = None
        
    def start(self):
        self.character = Character()
        self.character.create_character()
        while self.is_running:
            self.update()
            self.render()
            
    def update(self):
        # Update game state, handle, events, etc.
        pass
    
    def render(self):
        # Render the game state to console
        pass
    
    def stop(self):
        self.is_running = False