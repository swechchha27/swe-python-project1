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
INPUT_COLOR = BLACK

# Set standard sizes
screen_size = (800, 600)
button_size = (200, 40)
textbox_size = (140, 32)

# Set standard screen areas
screen_area = (50, 50, 700, 500)  # leaving 50px margin on all sides

# Initialize Pygame font and set standard fonts
pygame.font.init()
h1_font = pygame.font.SysFont('arialblack', 36)
h2_font = pygame.font.SysFont('arialblack',30)
h3_font = pygame.font.SysFont('arialblack', 26)
text_font = pygame.font.SysFont('centuryschoolbook', 18)
small_font = pygame.font.SysFont('brittanic', 10)
dialogue_font = pygame.font.SysFont('cambria', 15)
button_font = pygame.font.SysFont('stencil', 15)
input_font = pygame.font.SysFont('arial', 15)
form_font = pygame.font.SysFont('serif', 16)


# Text Effect functions
def typewriter_effect(screen, message, position, font=text_font, delay=0.1, **kwargs):
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
    return message

def slow_scroll(screen, message, position, font=text_font, delay=0.2, **kwargs):
    x, y = position
    for line in message.split('\n'):
        line_surface = font.render(line, True, TEXT_COLOR)
        screen.blit(line_surface, (x, y))
        y += line_surface.get_height()
        update_display()
        delay_event(delay)
    return message

def flash_effect(screen, message, position, font=text_font, times=3, delay=0.5, **kwargs):
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
    return message


# to keep track of current screen
class ScreenManager:
    _screen = None
    @classmethod
    def set_screen(cls, screen):
        cls._screen = screen
    @classmethod
    def get_screen(cls):
        if cls._screen is None:
            raise ValueError("Screen has not been initialized. Call set_screen() first.")
        return cls._screen


# to keep track of current text position
class TextManager:
    _screen = None
    _start_position = (50, 50)
    _line_height = 30
    current_y = _start_position[1]
    @classmethod
    def add_text(cls, text, effects=[typewriter_effect], font=text_font, color=TEXT_COLOR, alignment='left', **kwargs):
        position = (cls._start_position[0], cls.current_y)
        display_text_with_effects(text, position, effects, font, color, alignment, **kwargs)
        cls.current_y += cls._line_height
        delay_event(2)


def initialize_display(screen_size=screen_size, caption="Life Simulator"):
    width, height = screen_size
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    current_screen = screen
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

# Helper functions
def center_position(index, total_buttons=1, button_size=button_size, screen_area=None):
    """
    Calculate the center position for a button based on the screen area.

    Args:
        index (int): The index of the button.
        total_buttons (int): The total number of buttons.
        button_size (tuple): The size of the button (width, height).
        screen_area (tuple): Optional. The screen area to consider for centering (x, y, width, height).
                             If not provided, the full screen size will be used.

    Returns:
        tuple: The calculated (x, y) position for the button.
    """
    if screen_area is None:
        screen_width, screen_height = screen_size
        x_offset, y_offset = 0, 0
    else:
        x_offset, y_offset, screen_width, screen_height = screen_area
    button_width, button_height = button_size
    x = x_offset + (screen_width - button_width) // 2
    y = y_offset + (screen_height - (total_buttons * (button_height + 10))) // 2 + index * (button_height + 10)
    return (x, y)

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

# Decorator to add multiple text effects
def add_effects(effect_functions):
    def decorator(func):
        def wrapper(screen, text, position, *args, **kwargs):
            for effect_function in effect_functions:
                text = effect_function(screen, text, position, *args, **kwargs)
            return func(screen, text, position, *args, **kwargs)
        return wrapper
    return decorator

# Text Display functions
def display_text(screen, text, position, font=text_font, color=TEXT_COLOR):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def display_multiline_text(screen, text, position, font=text_font, color=TEXT_COLOR):
    x, y = position
    for line in text.split('\n'):
        # Render each line
        display_text(screen, line, (x, y), font, color)
        y += font.get_height() + 5  # Adjust the line height with an extra margin

def calculate_aligned_position(text, alignment, font, screen_area=None):
    lines = text.split('\n')
    positions = []
    for line in lines:
        text_surface = font.render(line, True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        x, y = center_position(lines.index(line), total_buttons=len(lines), button_size=(text_rect.size), screen_area=screen_area)
        positions.append((x, y))
        y += font.get_linesize()
    return positions

def display_aligned_text(screen, text, position, alignment='left', font=text_font, color=TEXT_COLOR, screen_area=screen_area):
    positions = calculate_aligned_position(text, alignment, font, screen_area=screen_area)
    for line, (x, y) in zip(text.split('\n'), positions):
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (x, y))
        # print('ALIGNED: '+line)

# Unified function to display text with effects
def display_text_with_effects(text, position, effects=[], font=text_font, color=TEXT_COLOR, alignment='left', **kwargs):
    screen=ScreenManager.get_screen()
    screen_area = None if not kwargs.get('screen_area') else kwargs['screen_area']
    print(screen_area)
    positions = calculate_aligned_position(text, alignment, font, screen_area=screen_area)
    print(positions)
    for effect in effects:
        for line, (x, y) in zip(text.split('\n'), positions):
            print(line)
            text = effect(screen, line, (x, y), font=font, color=color, **kwargs)
    # display_aligned_text(screen, text, position, alignment=alignment, font=font, color=color)

@add_effects([typewriter_effect])
def display_typed_text(screen, text, position, font=text_font, color=TEXT_COLOR, **kwargs):
    display_text(screen, text, position, font, color)

@add_effects([typewriter_effect])
def display_typed_multiline_text(screen, text, position, font=text_font, color=TEXT_COLOR, **kwargs):
    display_multiline_text(screen, text, position, font, color)

def create_rect(x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    return rect

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
    

class TextBox:
    def __init__(self, screen, label, position, size=textbox_size, font=input_font):
        self.screen = screen
        self.label = label
        self.position = position
        self.size = size
        self.font = font
        self.input_box = create_rect(position[0]+200, position[1], size[0], size[1])
        self.active = False
        self.text = ''
    def draw(self):
        # Clear the text box area
        self.screen.fill(WHITE, self.input_box)
        # Render the text
        display_text(self.screen, self.text, (self.input_box.x + 5, self.input_box.y + 5), self.font, INPUT_COLOR)
        # Draw the input box
        pygame.draw.rect(self.screen, self.get_color(), self.input_box, 2)
        # Display the label
        display_text(self.screen, self.label, (self.position[0], self.position[1]), form_font)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN :
                    self.active = False   
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
    def get_active(self):
        return self.active
    def set_active(self, active):
        self.active = active
        print(f"Textbox {self.label} active set to {self.active}")
    def get_color(self):
        return TEXTBOX_ACTIVE if self.get_active() else TEXTBOX_INACTIVE
    def is_complete(self):
        return bool(self.text)
    @property
    def value(self):
        return self.text.strip()


class RadioButton:
    def __init__(self, screen, label, options, position, font=form_font):
        self.screen = screen
        self.label = label
        self.options = options
        self.position = position
        self.font = font
        self.active = False
        self.selected_option = None
        self.rects = []
        # Create rectangles for each radio button option
        self._create_radio_buttons()
    def _create_radio_buttons(self):
        x, y = (self.position[0], self.position[1] + 30)
        for option in self.options:
            option_text = self.font.render(option, True, TEXT_COLOR)
            option_rect = option_text.get_rect(topleft=(x + 20, y))
            radio_rect = create_rect(x, y + 5, 10, 10)
            self.rects.append((radio_rect, option_rect, option))
            x += 130 
    def draw(self):
        display_text(self.screen, self.label, self.position, self.font, TEXT_COLOR)
        for radio_rect, option_rect, option in self.rects:
            # print(self.selected_option)
            pygame.draw.circle(self.screen, self.get_color(option), radio_rect.center, 6)
            if self.selected_option == option:
                pygame.draw.circle(self.screen, BLACK, radio_rect.center, 4)
            display_text(self.screen, option, option_rect.topleft, self.font, TEXT_COLOR)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for radio_rect, option_rect, option in self.rects:
                if radio_rect.collidepoint(event.pos) or option_rect.collidepoint(event.pos):
                    # self.active = True  # not self.active
                    self.selected_option = option
                    print(f"{option} selected")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            # Select next option
            if (self.selected_option in self.options 
            and self.options.index(self.selected_option) + 1 < len(self.options)):
                    self.selected_option = self.options[self.options.index(self.selected_option) + 1]
            else:
                self.selected_option = self.options[0]
            print(f"{self.selected_option} selected")
    def get_active(self):
        return self.active
    def set_active(self, active):
        self.active = active
    def get_color(self, option):
        return TEXTBOX_ACTIVE if (self.get_active() and self.selected_option==option) else TEXTBOX_INACTIVE
    def is_complete(self):
        return bool(self.value)
    def is_last_radio_selected(self):
        if self.selected_option == self.options[len(self.options)-1]:
            return True
        else:
            return False
    @property
    def value(self):
        return self.selected_option

class Form:
    def __init__(self, screen):
        self.screen = screen
        self.elements = []
        self.active_element_index = 0
    def add_element(self, element):
        self.elements.append(element)
        if len(self.elements) == 1:  # If this is the first element, activate it
            self.elements[0].set_active(True)
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                if (isinstance(self.elements[self.active_element_index], RadioButton) 
                and (not self.elements[self.active_element_index].is_last_radio_selected())):
                        self.elements[self.active_element_index].set_active(True)
                        self.elements[self.active_element_index].handle_event(event)
                else:
                    # Deactivate current element
                    self.elements[self.active_element_index].set_active(False)
                    # Move to the next element, looping back to the start if necessary
                    self.active_element_index = (self.active_element_index + 1) % len(self.elements)
                    # Activate the new current element
                    self.elements[self.active_element_index].set_active(True)
                    if isinstance(self.elements[self.active_element_index], RadioButton):
                        self.elements[self.active_element_index].handle_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check which element was clicked and activate it
                for index, element in enumerate(self.elements):
                    if isinstance(element, RadioButton):
                        for radio_rect, option_rect, option in element.rects:
                            if radio_rect.collidepoint(event.pos) or option_rect.collidepoint(event.pos):
                                self.elements[self.active_element_index].set_active(False)
                                self.active_element_index = index
                                self.elements[self.active_element_index].set_active(True)
                                self.elements[self.active_element_index].handle_event(event)
                                break
                    elif isinstance(element, TextBox):
                        if element.input_box.collidepoint(event.pos):
                            self.elements[self.active_element_index].set_active(False)
                            self.active_element_index = index
                            element.handle_event(event)
                            break
            else:
                # Pass the event to the active element for handling
                self.elements[self.active_element_index].handle_event(event)
    def deactivate_all(self):
        for element in self.elements:
            element.set_active(False)
    def draw(self):
        for element in self.elements:
            element.draw()
    def is_complete(self):
        return all(element.is_complete() for element in self.elements)
    def get_data(self):
        return {element.label: element.value for element in self.elements}


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
                    display_text_with_effects(screen, "Welcome to the Game!", (250, 450), font=h1_font, color=TEXT_COLOR, effects=[typewriter_effect, flash_effect], alignment='left')
                    display_text_with_effects(screen, "This is a center aligned text with effects."
                                              + "\nLine 2 starts here."
                                              + "\nLine 3."
                                              + "\nThis is the last line."
                                              , (screen.get_width() // 2, screen.get_height() // 2)
                                              , font=h2_font, color=TEXT_COLOR
                                              , effects=[typewriter_effect], alignment='center'
                                              , screen_area=(400, 300, 400, 500))
                    update_display()
                    delay_event(0.5)  # Optional: wait for 0.5 seconds to show the message
        quit_display()
        sys.exit()
    # print([f for f in pygame.font.get_fonts() if 'lucida' in f])
    # print([(c, v) for c, v in pygame.color.THECOLORS.items() if 'blue' in c])
    sys.exit()

