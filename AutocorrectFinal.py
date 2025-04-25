import pygame
import sys
import textwrap

# Load dictionary
def load_words(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def find_matches(words, prefix):
    return [word for word in words if word.startswith(prefix)]

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def render_multiline_text(surface, lines, font, pos, color):
    x, y = pos
    for line in lines:
        rendered = font.render(line, True, color)
        surface.blit(rendered, (x, y))
        y += font.get_height()

def render_cursor_and_fade(last_line, current_word, suggestion, cursor_visible, x, y):
    offset = FONT.size(last_line)[0]
    if suggestion and len(current_word) < len(suggestion):
        faded = suggestion[len(current_word):]
        faded_surface = FADE_FONT.render(faded, True, FADE_COLOR)
        screen.blit(faded_surface, (x + offset, y))

    if cursor_visible:
        pygame.draw.line(screen, TEXT_COLOR, (x + offset, y), (x + offset, y + FONT.get_height()), 2)

# Setup
pygame.init()
WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vertical Expanding Autocomplete")

FONT = pygame.font.SysFont("Arial", 32)
FADE_FONT = pygame.font.SysFont("Arial", 32)
FADE_COLOR = (180, 180, 180)
TEXT_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
BOX_COLOR = (230, 230, 230)
BUTTON_COLOR = (255, 100, 100)
BUTTON_HOVER = (255, 80, 80)

word_list = load_words("words.txt")
input_text = ''

clock = pygame.time.Clock()
cursor_timer = 0
cursor_visible = True

backspace_held = False
backspace_timer = 0
BACKSPACE_DELAY = 500
BACKSPACE_REPEAT = 50

box_margin = 50
input_box_width = WIDTH - 2 * box_margin

running = True
while running:
    screen.fill(BG_COLOR)
    dt = clock.tick(60)
    cursor_timer += dt

    if cursor_timer >= 500:
        cursor_visible = not cursor_visible
        cursor_timer = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_BACKSPACE]:
        if not backspace_held:
            backspace_held = True
            backspace_timer = BACKSPACE_DELAY
        else:
            backspace_timer -= dt
            if backspace_timer <= 0:
                input_text = input_text[:-1]
                backspace_timer = BACKSPACE_REPEAT
    else:
        backspace_held = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_RETURN:
                words = input_text.split(' ')
                if words:
                    last_word = words[-1]
                    matches = find_matches(word_list, last_word)
                    if matches:
                        words[-1] = matches[0]
                        input_text = ' '.join(words)
            elif event.key == pygame.K_SPACE:
                words = input_text.split(' ')
                if words:
                    last_word = words[-1]
                    if len(last_word) > 1:  # Need at least 2 chars to get prior suggestion
                        prior_prefix = last_word[:-1]  # Prefix before last letter
                        matches = find_matches(word_list, prior_prefix)
                        if matches:
                            words[-1] = matches[0]  # Use suggestion for prior prefix
                            input_text = ' '.join(words) + ' '
                        else:
                            input_text += ' '
                    else:
                        matches = find_matches(word_list, last_word)
                        if matches:
                            words[-1] = matches[0]
                            input_text = ' '.join(words) + ' '
                        else:
                            input_text += ' '
                else:
                    input_text += ' '
            elif event.unicode.isprintable():
                input_text += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if clear_rect.collidepoint(event.pos):
                input_text = ""

    words = input_text.split(' ')
    last_word = words[-1] if words else ''
    matches = find_matches(word_list, last_word)
    suggestion = matches[0] if matches else ''

    # Wrap text and compute height
    wrapped_lines = wrap_text(input_text, FONT, input_box_width - 20)
    input_box_height = max(60, FONT.get_height() * len(wrapped_lines) + 20)
    input_box_rect = pygame.Rect(box_margin, 80, input_box_width, input_box_height)

    # Draw input box
    pygame.draw.rect(screen, BOX_COLOR, input_box_rect, border_radius=12)
    pygame.draw.rect(screen, (180, 180, 180), input_box_rect, 2, border_radius=12)

    render_multiline_text(screen, wrapped_lines, FONT, (input_box_rect.x + 10, input_box_rect.y + 10), TEXT_COLOR)

    if wrapped_lines:
        render_cursor_and_fade(
            wrapped_lines[-1],
            last_word,
            suggestion,
            cursor_visible,
            input_box_rect.x + 10,
            input_box_rect.y + 10 + FONT.get_height() * (len(wrapped_lines) - 1)
        )

    # Draw Clear Button
    clear_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 60, 120, 40)
    is_hover = clear_rect.collidepoint(pygame.mouse.get_pos())
    pygame.draw.rect(screen, BUTTON_HOVER if is_hover else BUTTON_COLOR, clear_rect, border_radius=20)
    pygame.draw.rect(screen, (200, 50, 50), clear_rect, 2, border_radius=20)

    clear_label = FONT.render("Clear", True, (255, 255, 255))
    text_rect = clear_label.get_rect(center=clear_rect.center)
    screen.blit(clear_label, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()