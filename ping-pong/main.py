import pygame
import sys
# Import GameEngine from the 'game' package
from game.game_engine import GameEngine

# --- Initialization ---
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BLACK = (0, 0, 0)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping Pong Game")
clock = pygame.time.Clock()

# Setup game engine
game = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT)

# --- Game Loop ---
running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle game over events (e.g., reset/exit)
        game.handle_game_over_event(event)


    # 2. Input and Update
    if not game.game_over:
        game.handle_input()
        game.update()


    # 3. Rendering
    screen.fill(BLACK)
    game.render(screen)
    
    # Player control text at the bottom
    font_small = pygame.font.SysFont(None, 24)
    controls_text = font_small.render("Player: W (Up) / S (Down)", True, (150, 150, 150))
    screen.blit(controls_text, (20, SCREEN_HEIGHT - 30))

    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# --- Cleanup ---
pygame.quit()
sys.exit()
