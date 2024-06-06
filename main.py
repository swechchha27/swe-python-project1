from game.game import Game
from utilities.display import (
    initialize_display, clear_screen, display_text,
    update_display, get_events, quit_display, display_dict,
    get_text_input,
    create_rect, Button,
    h1_font, h2_font, h3_font, text_font, small_font,
    BACKGROUND_COLOR, ERROR_COLOR
)
from utilities.constants import GENDERS
import pygame
import sys


def main():
    game = Game()

    # Initialize main screen
    screen = initialize_display()

    # Create buttons
    buttons = {
        "create_character": Button("Create Character", (100, 100)),
        "start_random_game": Button("Start New Game \n[Random Character]", (100, 150)),
        "load_game": Button("Load Game from a Slot", (100, 200)),
        "quit": Button("Quit", (100, 250)),
        "run_year": Button("Run a Year", (100, 100)),
        "view_stats": Button("View Character Stats", (100, 150)),
        "save_game": Button("Save Game", (100, 200)),
        "save_exit": Button("Save and Exit", (100, 250)),
        "exit_without_saving": Button("Exit without saving", (100, 300))
    }

    # Create text links
    links = {
        # "head": Button("Head", (100, 100), (50, 25), BACKGROUND_COLOR)
    }

    clock = pygame.time.Clock()

    # Main game loop
    running = True
    menu_active = True
    character_creation_active = False
    game_active = False

    while running:
        clear_screen(screen)

        if menu_active:
            display_text(screen, "Welcome to the Game!", (50, 50), h1_font)
            buttons["create_character"].draw(screen)
            buttons["start_random_game"].draw(screen)
            buttons["load_game"].draw(screen)
            buttons["quit"].draw(screen)

        elif character_creation_active:
            display_text(screen, "Character Creation", (50, 50), h2_font)
            name = get_text_input(screen, "Enter name:", (100, 200), text_font)
            gender = get_text_input(screen, "Enter gender:", (100, 300), text_font)
            birth_origin = get_text_input(screen, "Enter birth origin:", (100, 400), text_font)
            game.create_character(name, gender, birth_origin)
            game_active = True
            character_creation_active = False

        elif game_active:
            display_text(screen, "Game Menu", (50, 50), h3_font)
            buttons["run_year"].draw(screen)
            buttons["view_stats"].draw(screen)
            buttons["save_game"].draw(screen)
            buttons["save_exit"].draw(screen)
            buttons["exit_without_saving"].draw(screen)

        # Input event handling
        for event in get_events():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_active:
                    if buttons["create_character"].is_clicked(event):
                        character_creation_active = True
                        menu_active = False
                    elif buttons["start_random_game"].is_clicked(event):
                        display_text(screen, "Creating Random character..", (250, 200), h3_font)
                        update_display()
                        pygame.time.wait(2000)  # Wait for 2 seconds to display the message
                        character_info = game.create_random_character()
                        display_text(screen, character_info, (250, 250), h3_font)
                        update_display()
                        pygame.time.wait(3000)  # Wait for 3 seconds to display the character info
                        game_active = True
                        menu_active = False
                    elif buttons["load_game"].is_clicked(event):
                        display_text(screen, "Load Game!", (250, 100), text_font)
                        game.load_game(get_slot_input(screen))
                        game_active = True
                        menu_active = False
                    elif buttons["quit"].is_clicked(event):
                        running = False
                
                elif game_active:
                    if buttons["run_year"].is_clicked(event):
                        game.run_year()
                    elif buttons["view_stats"].is_clicked(event):
                        display_stats(screen, game)
                    elif buttons["save_game"].is_clicked(event):
                        game.save_game(get_slot_input(screen))
                    elif buttons["save_exit"].is_clicked(event):
                        game.save_game(get_slot_input(screen))
                        running = False
                    elif buttons["exit_without_saving"].is_clicked(event):
                        running = False

        # Refresh the Pygame display with new content
        update_display()
        clock.tick(60)

    game.character.display_life_summary()
    display_text(screen, "GAME OVER!", (50, 50), h1_font, ERROR_COLOR)
    quit_display()
    sys.exit()

def get_slot_input(screen):
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
    clear_screen(screen)
    display_dict(screen, "Necessities", game.character.necessities, (50, 100))
    display_dict(screen, "Emotions", game.character.emotions, (250, 100))
    display_dict(screen, "Traits", game.character.traits, (50, 300))
    display_dict(screen, "Skills", game.character.skills, (250, 300))
    pygame.display.flip()
    pygame.time.wait(10000)


if __name__ == "__main__":
    main()