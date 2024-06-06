import time
import sys
import pygame
from pygame.locals import *
from functools import wraps


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = pygame.Color("royalblue2")
YELLOW = pygame.Color("yellow")

# Set standard colors
TEXT_COLOR = pygame.Color("darkgray")
BUTTON_COLOR = (0, 0, 255)
HOVER_COLOR = (150, 150, 255)
SELECTED_COLOR = (0, 150, 255)
BACKGROUND_COLOR = BLACK
TEXTBOX_INACTIVE = pygame.Color('lightskyblue3')
TEXTBOX_ACTIVE = pygame.Color('dodgerblue2')
ERROR_COLOR = RED

# Set standard sizes
button_size = (100, 40)
textbox_size = (140, 32)

# Initialize Pygame font and set standard fonts
pygame.font.init()
h1_font = pygame.font.SysFont('arialblack', 36)
h2_font = pygame.font.Font(None, 30)
h3_font = pygame.font.Font(None, 26)
text_font = pygame.font.SysFont('Helvetica', 18)
small_font = pygame.font.Font(None, 10)
dialogue_font = pygame.font.SysFont('arial', 15)
button_font = pygame.font.SysFont('calibri', 15)

def initialize_display(width=800, height=600, caption="Life Simulator"):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return screen

def clear_screen(screen, color=WHITE):
    screen.fill(color)

def display_text(screen, text, position, font=text_font, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def update_display():
    pygame.display.flip()

def get_events():
    return pygame.event.get()

def quit_display():
    pygame.quit()

def create_rect(x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    return rect

def color_value(value):
    if value >= 8:
        return GREEN
    elif value >= 4:
        return YELLOW
    else:
        return RED

def display_dict(screen, title, data, position, font=text_font):
    display_text(screen, title, position, h3_font) # Render title
    x, y = position
    y_offset = 10
    y += h3_font.get_height() + y_offset
    y_offset = 5
    for key, value in data.items():
        display_text(screen, f"{key}: ",  (x, y), font) # Render keys
        value_color = color_value(value) # Select color based on range of value
        display_text(screen, f"{value}", (x + 100, y), font, value_color) # Render values
        y += font.get_height()//2 + y_offset
    
def get_text_input(screen, prompt, position, font=text_font):
    input_box = create_rect(position[0], position[1], textbox_size[0], textbox_size[1])
    color = TEXTBOX_INACTIVE
    active = False
    text = ''
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_display()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = TEXTBOX_ACTIVE if active else TEXTBOX_INACTIVE
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        
        screen.fill((255, 255, 255), input_box)  # clear rect area
        # display_text(screen, text, (input_box.x+5, input_box.y+5), font, color)
        txt_surface = font.render(text, True, TEXT_COLOR)
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))  # offset text position from rect
        pygame.draw.rect(screen, color, input_box, 2)  # 2 is for border width
        display_text(screen, prompt, (position[0], position[1] - 30), font)
        # above displays prompt above input box
        update_display()
    return text


def add_asterisks(func):
    @wraps(func)
    def wrapper(message, *args, **kwargs):
        # Create a line of asterisks based on the length of the message
        border = '*' * (len(message) + 4)
        # Format the message with asterisks around it
        decorated_message = f"{border}\n* {message} *\n{border}"
        return func(decorated_message, *args, **kwargs)
    return wrapper

def typewriter_effect(message, delay=0.1):
    """
    Prints the given message to the terminal with a typewriter effect.

    Parameters:
    message (str): The message to display.
    delay (float): The delay between each character in seconds.
    """
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def slow_scroll(message, delay=0.2):
    """
    Prints the given message to the terminal with a slow scrolling effect.

    Parameters:
    message (str): The message to display.
    delay (float): The delay between each line in seconds.
    """
    for line in message.split('\n'):
        print(line)
        time.sleep(delay)

def flash_effect(message, times=3, delay=0.5):
    """
    Prints the given message to the terminal with a flashing effect.

    Parameters:
    message (str): The message to display.
    times (int): Number of times to flash the message.
    delay (float): The delay between flashes in seconds.
    """
    for _ in range(times):
        sys.stdout.write(f'\r{message}')
        sys.stdout.flush()
        time.sleep(delay)
        sys.stdout.write('\r' + ' ' * len(message))
        sys.stdout.flush()
        time.sleep(delay)
    print(message)

@add_asterisks
def display_with_asterisks(message, delay=0.1):
    typewriter_effect(message, delay)


class Button:
    def __init__(self, text, pos, size=button_size, color=BUTTON_COLOR, text_color=WHITE):
        self.text = text
        self.width, self.height = size
        self.position = pos
        self.color = color
        self.text_color = text_color
        self.font = button_font
        self.rect = create_rect(pos[0], pos[1], self.width, self.height)
        self.hover_color = HOVER_COLOR

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        display_text(screen, self.text
                     , [self.position[0] + 10, self.position[1] + 5], self.font, self.text_color)
        # screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def is_selected(self, event):
        if ((event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) 
            or (event.type == pygame.MOUSEBUTTONUP and event.button == 1)):
            return True
        return False
    
    def is_hovered(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False





# Example usage
if __name__ == "__main__":
    # typewriter_effect("This is a typewriter effect.", 0.05)
    # slow_scroll("This is a slow scrolling effect.\nLine 2.\nLine 3.", 0.5)
    # flash_effect("This is a flashing effect.", 3, 0.5)
    # display_with_asterisks("This is a heading with asterisks.", 0.1)
    test_display = input("Type y|Y if you want to test pygame display:")
    if test_display.lower() == 'y':
        screen = initialize_display()
        running = True
        while running:
            clear_screen(screen)
            display_text(screen, "Welcome to the Life Simulator Game!", (50, 50), h1_font)
            for event in get_events():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    display_text(screen, "Some event occurred!", (50, 100), text_font, RED)
                    display_dict(screen, "Necessities"
                                , {"reading":10, "writing":20,
                                    "art":10, "crafting":5,
                                    "cooking":1, "fighting":20}
                                , (50, 150))
            update_display()
        quit_display()
    print([f for f in pygame.font.get_fonts() if 'lucida' in f])
    print([(c, v) for c, v in pygame.color.THECOLORS.items() if 'blue' in c])
    sys.exit()

