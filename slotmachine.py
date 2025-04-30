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
symbols = ["🍒", "🍋", "🥭", "🥑", "🍊", "💀", "🥩", "👑", "🥕", "🥪", "🐖", "🐢", "🏆", "🎈", "🚽", "🪑", "🍆", "🥚", "🥒", "🚗", "🛬", "🗼", "🥱", "🤔", "🤫", "🗣", "🔥", "🔮", "🎳", "🎁", "🌈", "🏳‍🌈", "📋", "🐑", "📳", "🌐"]
symbol_colors = [RED, GREEN, BLUE, WHITE, RED]

# Sounds
win = pygame.mixer.Sound("win.wav")  # Win sound
TDB = pygame.mixer.Sound("VBS.wav")  # Default spin sound
spin_sounds = [pygame.mixer.Sound("VBS.wav"), pygame.mixer.Sound("MPF.wav"), pygame.mixer.Sound("TBD.wav")] 

# Reel positions
reel_positions = [WIDTH // 4, WIDTH // 2, 3 * WIDTH // 4]
reel_results = ["", "", ""]

# Spin button
button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 80, 100, 50)

# Counters
wins = 0
spins = 0

# Initial balance
balance = 1000  # Starting money
spin_cost = 5  # Cost per spin
win_reward = 100  # Reward for a win

def draw_balance():
    """Display the player's balance on the screen."""
    drawText(f"Balance: ${balance}", WHITE, WIDTH // 2, HEIGHT - 290, 36)

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
    global reel_results, wins, spins, balance

    # Deduct the spin cost
    if balance < spin_cost:
        drawText("Not enough money!", RED, WIDTH // 2, HEIGHT // 2 + 150, 50)
        pygame.display.flip()
        pygame.time.delay(2000)
        return

    balance -= spin_cost  # Decrease balance
    spins += 1  # Increment the spin counter

    # Play a random spin sound
    random.choice(spin_sounds).play()

    # Step 1: Replace emojis with question marks
    draw_reels()
    pygame.display.flip()
    pygame.time.delay(50)

    # Step 2: Final results for each reel
    reel_results = [random.choice(symbols) for _ in range(3)]
    draw_reels()
    pygame.display.flip()

    # Step 3: Check for a win
    if reel_results[0] == reel_results[1] == reel_results[2]:
        pygame.mixer.Sound.play(win)  # Play the win sound
        for i, pos in enumerate(reel_positions):
            text = emoji_font.render(reel_results[i], True, symbol_colors[i])
            screen.blit(text, (pos - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        wins += 1
        balance += win_reward  # Add the win reward
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

        # Display the balance
        draw_balance()

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