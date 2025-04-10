import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slot Machine")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)
# Load an emoji-compatible font
emoji_font = pygame.font.Font("NotoColorEmoji.ttf", 1)  # Replace with your emoji font file

# Slot symbols
symbols = ["🍒", "🍋", "🔔", "⭐", "🍉"]
symbol_colors = [RED, GREEN, BLUE, WHITE, RED]

# Reel positions
reel_positions = [WIDTH // 4, WIDTH // 2, 3 * WIDTH // 4]
reel_results = ["", "", ""]

# Spin button
button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 80, 100, 50)

# Counters
wins = 0
spins = 0

def draw_reels(reel_offsets=None):
    if reel_offsets is None:
        reel_offsets = [0, 0, 0]
    for i, pos in enumerate(reel_positions):
        # Draw larger reel borders
        pygame.draw.rect(screen, WHITE, (pos - 75, HEIGHT // 2 - 75, 150, 150), 2)
        if reel_results[i]:
            # Render the emoji or question mark using the emoji-compatible font
            text = emoji_font.render(reel_results[i], True, WHITE)
            screen.blit(text, (pos - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + reel_offsets[i]))

def drawText(message, color, x, y, size):
    """Draw text on the screen."""
    text_font = pygame.font.Font(None, size)
    text = text_font.render(message, True, color)
    screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

def spin_reels():
    global reel_results, wins, spins

    # Increment the spin counter
    spins += 1

    # Step 1: Replace emojis with question marks
    reel_results = ["?", "?", "?"]
    draw_reels()
    pygame.display.flip()
    pygame.time.delay(1000)  # Display question marks for 1 second

    # Step 2: Final results for each reel
    reel_results = [random.choice(symbols) for _ in range(3)]
    draw_reels()
    pygame.display.flip()

    # Step 3: Check for a win
    if reel_results[0] == reel_results[1] == reel_results[2]:
        wins += 1  # Increment the win counter
        drawText("You Win!", GREEN, WIDTH // 2, HEIGHT // 2 + 100, 50)
        pygame.display.flip()
        pygame.time.delay(2000)  # Pause for 2 seconds

def main():
    # Initialize the clock
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        # Draw reels
        draw_reels()

        # Draw spin button
        pygame.draw.rect(screen, WHITE, button_rect)
        button_text = font.render("SPIN", True, BLACK)
        screen.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2,
                                  button_rect.y + button_rect.height // 2 - button_text.get_height() // 2))

        # Display the number of wins and spins
        drawText(f"Wins: {wins}", WHITE, WIDTH // 2, HEIGHT - 350, 36)
        drawText(f"Spins: {spins}", WHITE, WIDTH // 2, HEIGHT - 320, 36)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    spin_reels()

        pygame.display.flip()
        clock.tick(30)  # Limit the frame rate to 30 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit()