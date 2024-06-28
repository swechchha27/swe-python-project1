from game.game import Game
from utilities.display import (
    initialize_display, clear_screen, display_text,
    update_display, get_events, quit_display, display_dict,
    center_position, display_text_with_effects, display_aligned_text,
    typewriter_effect, flash_effect, create_rect, Button, TextBox, Form,
    RadioButton, ScreenManager, TextManager,
    h1_font, h2_font, h3_font, text_font, small_font, input_font,
    BACKGROUND_COLOR, ERROR_COLOR, screen_size, button_size, INPUT_COLOR
)
from utilities.constants import GENDERS
import pygame
import sys


def main():
    game = Game()

    # Initialize main screen
    screen = initialize_display()
    if not screen:
        print("Failed to initialize display")
        return
    ScreenManager.set_screen(screen)

    # Create buttons
    buttons = {
        "create_character": Button("Create Character", center_position(0, 4)),
        "start_random_game": Button("Start New Game [Random Character]", center_position(1, 4)),
        "load_game": Button("Load Game from a Slot", center_position(2, 4)),
        "quit": Button("Quit", center_position(3, 4)),
        "run_year": Button("Run a Year", center_position(0, 5)),
        "view_stats": Button("View Character Stats", center_position(1, 5)),
        "save_game": Button("Save Game", center_position(2, 5)),
        "save_exit": Button("Save and Exit", center_position(3, 5)),
        "exit_without_saving": Button("Exit without saving", center_position(4, 5)),
        "back": Button("Back", (50, 500)),
        "continue": Button("Continue", (550, 500))
    }

    clock = pygame.time.Clock()
    running = True
    menu_active = True
    character_creation_active = False
    game_active = False
    form = None
    form_initialized = False
    print('starting game loop')
    while running:
        clear_screen(screen, BACKGROUND_COLOR)
        events = get_events()

        if menu_active:
            title_area = (50, 50, 700, 100)
            display_aligned_text(screen, "Welcome to the Game!", (screen_size[0] // 2 - 100, 50), alignment='center', font=h1_font, screen_area=title_area)
            for button in ["create_character", "start_random_game", "load_game", "quit"]:
                buttons[button].draw(screen)
                if any(buttons[button].is_clicked(event) for event in events):
                    if button == "create_character":
                        character_creation_active = True
                        menu_active = False
                        form = Form(screen)
                        form.add_element(TextBox(screen, "Enter name:", (screen_size[0] // 2 - 300, 150), (200, 30)))
                        form.add_element(RadioButton(screen, "Select gender:",options=GENDERS, position=(screen_size[0] // 2 - 300, 200)))
                        form.add_element(TextBox(screen, "Enter birth origin:", (screen_size[0] // 2 - 300, 300), (200, 30)))
                        form_initialized = True
                    elif button == "start_random_game":
                        display_text_with_effects(screen, "Creating Random character..", position=(100, 500), screen_area=(100, 400, 800, 100), effects=[flash_effect], alignment='left', font=h3_font)
                        update_display()
                        pygame.time.wait(2000)  # Wait for 2 seconds to display the message
                        character_info = game.create_random_character()
                        display_text_with_effects(screen, character_info, position=(100, 500), screen_area=(100, 500, 800, 100), effects=[typewriter_effect], alignment='left')
                        update_display()
                        pygame.time.wait(3000)  # Wait for 3 seconds to display the character info
                        game_active = True
                        menu_active = False
                    elif button == "load_game":
                        display_text(screen, "Load Game!", (screen_size[0] // 2 - 100, 100), text_font)
                        game.load_game(get_slot_input(screen))
                        game_active = True
                        menu_active = False
                    elif button == "quit":
                        running = False

        elif character_creation_active:
            title_area = (50, 50, 700, 100)
            display_aligned_text(screen, "Character Creation", (screen_size[0] // 2 - 100, 50), alignment='center', font=h2_font, screen_area=title_area)
            for button in ["back", "continue"]:
                buttons[button].draw(screen)
                if any(buttons[button].is_clicked(event) for event in events):
                    if button == "back":
                        character_creation_active = False
                        menu_active = True
                        form_initialized = False  # Reset form initialization
                    elif button == "continue" and form.is_complete():
                        data = form.get_data()
                        print(data)
                        game.create_character(data["Enter name:"], data["Select gender:"], data["Enter birth origin:"])
                        game_active = True
                        character_creation_active = False
                        form_initialized = False  # Reset form initialization
            form.handle_events(events)
            form.draw()

        elif game_active:
            title_area = (50, 50, 700, 100)
            display_aligned_text(screen, "Game Menu", (screen_size[0] // 2 - 100, 50), alignment='center', font=h2_font, screen_area=title_area)
            for button in ["run_year", "view_stats", "save_game", "save_exit", "exit_without_saving"]:
                buttons[button].draw(screen)
                if any(buttons[button].is_clicked(event) for event in events):
                    if button == "run_year":
                        game.run_year()
                    elif button == "view_stats":
                        display_stats(screen, game)
                        # pass
                    elif button == "save_game":
                        game.save_game(get_slot_input(screen))
                    elif button == "save_exit":
                        game.save_game(get_slot_input(screen))
                        running = False
                    elif button == "exit_without_saving":
                        running = False

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        update_display()
        clock.tick(60)

    game.character.display_life_summary()
    display_text(screen, "GAME OVER!", (screen_size[0] // 2 - 100, 50), h1_font, ERROR_COLOR)
    quit_display()
    sys.exit()

def get_slot_input(screen):
    return "Random"
    try:
        slot = int(get_text_input(screen, "Enter Slot Number <1|2|3>:", (250, 200), text_font))
    except (TypeError, ValueError):
        display_text(screen, "Invalid Input! Type 1 or 2 or 3", (250, 250), text_font, ERROR_COLOR)
        slot = int(get_text_input(screen, "Enter Slot Number <1|2|3>:", (250, 200), text_font))
    if slot<1 or slot>3:
        display_text(screen, "Invalid Input! Type 1 or 2 or 3", (250, 250), text_font, ERROR_COLOR)
        slot = int(get_text_input(screen, "Enter Slot Number <1|2|3>:", (250, 200), text_font))
    return slot  # Placeholder, replace with actual logic

def display_stats(screen, game):
    clear_screen(screen, BACKGROUND_COLOR)
    display_dict(screen, "Necessities", game.character.necessities, (50, 100))
    display_dict(screen, "Emotions", game.character.emotions, (250, 100))
    display_dict(screen, "Traits", game.character.traits, (50, 300))
    display_dict(screen, "Skills", game.character.skills, (250, 300))
    pygame.display.flip()
    pygame.time.wait(10000)

if __name__ == "__main__":
    main()
