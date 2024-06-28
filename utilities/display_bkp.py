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
CAPTION_COLOR = WHITE
TEXT_COLOR = (242, 242, 242)
BUTTON_COLOR = (77, 255, 255)
HOVER_COLOR = (204, 204, 255)
SELECTED_COLOR = (0, 150, 255)
SHADOW_COLOR = (100, 100, 100)
BACKGROUND_COLOR = pygame.Color("darkgray")
TEXTBOX_INACTIVE = pygame.Color('lightskyblue3')
TEXTBOX_ACTIVE = pygame.Color('dodgerblue2')
ERROR_COLOR = RED

# Set standard sizes
screen_size = (800, 600)
button_size = (200, 40)
textbox_size = (140, 32)

# Initialize Pygame font and set standard fonts
pygame.font.init()
h1_font = pygame.font.SysFont('arialblack', 36)
h2_font = pygame.font.Font(None, 30)
h3_font = pygame.font.Font(None, 26)
text_font = pygame.font.SysFont('centuryschoolbook', 18)
small_font = pygame.font.SysFont('brittanic', 10)
dialogue_font = pygame.font.SysFont('cambria', 15)
button_font = pygame.font.SysFont('stencil', 15)

def initialize_display(screen_size=screen_size, caption="Life Simulator"):
    width, height = screen_size
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return screen

def clear_screen(screen, color=BACKGROUND_COLOR):
    screen.fill(color)

def update_display():
    pygame.display.flip()

def delay_event(delay=0.1):
    pygame.time.wait(int(delay * 1000))

def get_events():
    return pygame.event.get()

def quit_display():
    pygame.quit()

def display_text(screen, text, position, font=text_font, color=TEXT_COLOR):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def display_multiline_text(screen, text, position, font=text_font, color=TEXT_COLOR):
    x, y = position
    for line in text.split('\n'):
        # Render each line
        display_text(screen, line, (x, y), font, color)
        y += font.get_height() + 5  # Adjust the line height with an extra margin

def display_aligned_text(screen, text, position, alignment='left', font=text_font, color=TEXT_COLOR):
    lines = text.split('\n')
    line_height = font.get_linesize()
    y = position[1]
    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect()
        if alignment == 'center':
            text_rect.midtop = (position[0], y)
        elif alignment == 'right':
            text_rect.topright = (position[0], y)
        elif alignment == 'left':
            text_rect.topleft = (position[0], y)
        screen.blit(text_surface, text_rect)
        y += line_height

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
    
def center_position(index, total_buttons):
    screen_width , screen_height = screen_size
    button_width, button_height = button_size
    x = (screen_width - button_width) // 2
    y = (screen_height - (total_buttons * (button_height + 10))) // 2 + index * (button_height + 10)
    return (x, y)

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
        
        screen.fill(WHITE, input_box)  # clear rect area
        # display_text(screen, text, (input_box.x+5, input_box.y+5), font, color)
        txt_surface = font.render(text, True, TEXT_COLOR)
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))  # offset text position from rect
        pygame.draw.rect(screen, color, input_box, 2)  # 2 is for border width
        display_text(screen, prompt, (position[0], position[1] - 30), font)
        # above displays prompt above input box
        update_display()
    return text

def typewriter_effect(screen, message, position, font=text_font, delay=0.1):
    x, y = position
    for char in message:
        if char == '\n':  # Handle newline character explicitly
            x = position[0]
            y += font.get_height() + 5  # Move to the next line with an extra margin
        else:
            char_surface = font.render(char, True, TEXT_COLOR)
            screen.blit(char_surface, (x, y))
            x += char_surface.get_width()
        update_display()
        delay_event(delay)
    update_display()

def add_asterisks(func):
    @wraps(func)
    def wrapper(screen, message, position, font=text_font, *args, **kwargs):
        ratio = 10 / 9
        len_max = len(max(message.split('\n'), key=len))
        len_max = int(len_max * ratio)   # adjusting difference between width of asterisk and character
        border = '*' * len_max
        decorated_message = f"{border}\n"
        for line in message.split('\n'):
            len_line = int(len(line) * ratio)
            prefix = '*' * ((len(border) - len_line)//2)
            postfix = '*' * (len(border) - (len_line + len(prefix)))
            decorated_message += f"{prefix}{line}{postfix}\n"
        decorated_message += f"{border}"
        return func(screen, decorated_message, position, font, *args, **kwargs)
    return wrapper

@add_asterisks
def display_with_asterisks(screen, message, position, font=text_font, color=TEXT_COLOR):
    display_multiline_text(screen, message, position, font, color)

def slow_scroll(screen, message, position, font=text_font, delay=0.2):
    x, y = position
    for line in message.split('\n'):
        line_surface = font.render(line, True, TEXT_COLOR)
        screen.blit(line_surface, (x, y))
        y += line_surface.get_height()
        update_display()
        delay_event(delay)
    update_display()

def flash_effect(screen, message, position, font=text_font, times=3, delay=0.5):
    x, y = position
    message_surface = font.render(message, True, TEXT_COLOR)
    blank_surface = pygame.Surface(message_surface.get_size())
    blank_surface.fill(BACKGROUND_COLOR)
    for _ in range(times):
        screen.blit(message_surface, (x, y))
        update_display()
        delay_event(delay)
        screen.blit(blank_surface, (x, y))
        update_display()
        delay_event(delay)
    screen.blit(message_surface, (x, y))
    update_display()


class Button:
    def __init__(self, text, pos, size=button_size):
        self.text = text
        self.width, self.height = button_size
        self.position = pos
        self.color = BUTTON_COLOR
        self.hover_color = HOVER_COLOR
        self.text_color = WHITE
        self.font = button_font
        self.rect = create_rect(pos[0], pos[1], self.width, self.height)
        self.shadow_color = SHADOW_COLOR
        self.shadow_offset = 3
        self.border_radius = 0  # Rounded corners
        self.gradient = True  # Add a gradient fill if desired

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        # Draw shadow
        shadow_rect = self.rect.move(self.shadow_offset, self.shadow_offset)
        pygame.draw.rect(screen, self.shadow_color, shadow_rect, border_radius=self.border_radius)

        # Draw button with hover effect
        if is_hovered:
            color = self.hover_color
        else:
            color = self.color

        # Draw gradient if enabled
        if self.gradient:
            self.draw_gradient(screen, color)
        else:
            pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)

        # Render wrapped text
        self.draw_text(screen)

    def draw_gradient(self, screen, color):
        # Draw a vertical gradient
        for i in range(self.height):
            gradient_color = (
                color[0] + (self.shadow_color[0] - color[0]) * i // self.height,
                color[1] + (self.shadow_color[1] - color[1]) * i // self.height,
                color[2] + (self.shadow_color[2] - color[2]) * i // self.height
            )
            pygame.draw.line(screen, gradient_color, (self.rect.x, self.rect.y + i), (self.rect.x + self.width, self.rect.y + i))

    def draw_text(self, screen):
        words = self.text.split(' ')
        lines = []
        current_line = ""

        # Wrap text
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= self.width - 20:  # 20 for padding
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        # Center text vertically
        y_offset = (self.height - (len(lines) * self.font.get_height())) // 2

        for line in lines:
            text_surface = self.font.render(line.strip(), True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.y + y_offset + text_surface.get_height() // 2))
            screen.blit(text_surface, text_rect.topleft)
            y_offset += self.font.get_height()
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)


class Hyperlink:
    def __init__(self, text, pos):
        """
        Initialize the hyperlink.
        
        Parameters:
        text (str): The text to display as a hyperlink.
        pos (tuple): The (x, y) position to display the hyperlink.
        link_color (tuple): RGB color of the hyperlink text.
        hover_color (tuple): RGB color of the hyperlink text when hovered.
        """
        self.text = text
        self.position = pos
        self.link_color = BUTTON_COLOR
        self.hover_color = HOVER_COLOR
        self.font = text_font
        self.rect = self.font.render(self.text, True, self.link_color).get_rect(topleft=self.position)

    def draw(self, screen):
        """
        Draw the hyperlink on the screen.
        
        Parameters:
        screen (pygame.Surface): The screen to draw the hyperlink on.
        """
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Change color if hovered
        color = self.hover_color if is_hovered else self.link_color
        display_text(screen, self.text, self.position, self.font, color)

    def is_clicked(self, event):
        """
        Check if the hyperlink is clicked.
        
        Parameters:
        event (pygame.event.Event): The event to check for clicks.
        
        Returns:
        bool: True if the hyperlink is clicked, False otherwise.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False




# Example usage
if __name__ == "__main__":
    # typewriter_effect("This is a typewriter effect.", 0.05)
    # slow_scroll("This is a slow scrolling effect.\nLine 2.\nLine 3.", 0.5)
    # flash_effect("This is a flashing effect.", 3, 0.5)
    # display_with_asterisks("This is a heading with asterisks.", 0.1)
    # test_display = input("Type y|Y if you want to test pygame display: ")
    # if test_display.lower() == 'y':
    if True:
        screen = initialize_display()
        # button = Button("Click Me", (100, 400))
        button = Button("Go to previous one", (100, 100))
        hyperlink1 = Hyperlink("Go to Screen 1", (100, 200))
        hyperlink2 = Hyperlink("Go to Screen 2", (100, 300))
        running = True
        while running:
            clear_screen(screen)
            display_text(screen, "Welcome to the Game!", (50, 50), h1_font)
            hyperlink1.draw(screen)
            hyperlink2.draw(screen)
            button.draw(screen)
            update_display()
            # typewriter_effect(screen, "This is a typewriter effect!", (50, 100), delay=0.1)
            # slow_scroll(screen, "This is a slow scroll effect!\nLine 2\nLine 3", (50, 150), delay=0.2)
            # flash_effect(screen, "Flashing message!", (50, 250), times=3, delay=0.5)
            # display_with_asterisks(screen, "Asterisk bordered message!\nSwe", (50, 300))
            
            for event in get_events():
                if event.type == pygame.QUIT:
                    running = False
                elif button.is_clicked(event):
                    print("Button clicked!")
                    # Do something when button is clicked
                    display_text(screen, "Button was clicked!", (250, 250), text_font)
                    update_display()
                    delay_event(1)  # Optional: wait for 1 second to show the message
                elif hyperlink1.is_clicked(event):
                    print("Hyperlink 1 clicked!")
                    # Do something when button is clicked
                    display_text(screen, "Hyperlink 1 was clicked!", (250, 250), text_font)
                    update_display()
                    delay_event(1)  # Optional: wait for 1 second to show the message
                elif hyperlink2.is_clicked(event):
                    print("Hyperlink 2 clicked!")
                    # Do something when button is clicked
                    display_text(screen, "Hyperlink 2 was clicked!", (250, 250), text_font)
                    update_display()
                    delay_event(1)  # Optional: wait for 1 second to show the message
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # display_text(screen, "Some event occurred!", (50, 100), text_font, RED)
                    # display_dict(screen, "Necessities"
                    #             , {"reading":10, "writing":20,
                    #                 "art":10, "crafting":5,
                    #                 "cooking":1, "fighting":20}
                    #             , (50, 150))
                    print("Mouse button down event!")
                    display_text(screen, "Mouse button down!", (250, 250), text_font)
                    update_display()
                    delay_event(0.5)  # Optional: wait for 0.5 seconds to show the message
        quit_display()
        sys.exit()
    # print([f for f in pygame.font.get_fonts() if 'lucida' in f])
    # print([(c, v) for c, v in pygame.color.THECOLORS.items() if 'blue' in c])
    sys.exit()

