import pygame
import os
from .paddle import Paddle 
from .ball import Ball     

class GameEngine:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height

        # Entities
        self.player = Paddle(30, screen_height // 2 - 50, 20, 100, screen_height, speed=6)
        self.ai = Paddle(screen_width - 30, screen_height // 2 - 50, 20, 100, screen_height, speed=6)
        self.ball = Ball(screen_width // 2 - 10, screen_height // 2 - 10, 20, 20, screen_width, screen_height)

        # Scores and state
        self.score_player = 0
        self.score_ai = 0
        self.winning_score = 5 
        self.game_over = False

        # Fonts
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 40)
        self.bigfont = pygame.font.SysFont(None, 72)
        self.smallfont = pygame.font.SysFont(None, 28)

        # Task 4: Add Sound Feedback
        # 1. Determine the absolute path to the directory containing THIS file (game_engine.py)
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        # 2. Construct the full path to the 'sounds' folder
        sounds_dir = os.path.join(base_dir, "sounds") 

        # Load sounds. This will print a warning if files are missing.
        self.sound_paddle = self._load_sound(os.path.join(sounds_dir, "paddle_hit.wav"))
        self.sound_wall = self._load_sound(os.path.join(sounds_dir, "wall_bounce.wav"))
        self.sound_score = self._load_sound(os.path.join(sounds_dir, "score.wav"))

    def _load_sound(self, path):
        """Safely load sound file and check if it exists"""
        try:
            if os.path.isfile(path):
                return pygame.mixer.Sound(path)
            else:
                # <-- IMPORTANT: This warning helps you debug file location!
                print(f"Warning: Sound file not found. Check if the file exists at: {path}") 
        except pygame.error as e:
            # Handle potential Pygame-specific loading errors
            print(f"Warning: Could not load sound {path} due to Pygame error: {e}") 
        except Exception as e:
            # Handle other general exceptions
            print(f"Warning: Could not load sound {path}: {e}")
        return None

    def play_sound(self, sound):
        """Play sound if available"""
        if sound:
            try:
                sound.play()
            except Exception:
                pass # Ignore errors if sound device is unavailable

    # --- INPUT, UPDATE, RENDER, and GAME OVER methods follow... ---

    def handle_input(self):
        """Handle player input (W and S keys). Player controls LEFT paddle"""
        keys = pygame.key.get_pressed()

        # Player controls (W=up, S=down)
        if keys[pygame.K_w]:
            self.player.move(up=True)
        elif keys[pygame.K_s]:
            self.player.move(up=False)

    def update(self):
        """Update game state, called every frame"""
        if self.game_over:
            return

        # Move ball and check for wall collision
        wall_hit = self.ball.move()
        if wall_hit == "wall":
            self.play_sound(self.sound_wall)

        # Check paddle collisions
        paddle_hit = self.ball.check_collision(self.player, self.ai)
        if paddle_hit == "paddle":
            self.play_sound(self.sound_paddle)

        # AI auto movement (RIGHT paddle)
        self.ai.auto_move(self.ball)

        # Scoring logic
        score_updated = False
        
        # Ball goes past LEFT side (AI scores)
        if self.ball.x < 0:
            self.score_ai += 1
            self.play_sound(self.sound_score)
            self.ball.reset()
            score_updated = True
            
        # Ball goes past RIGHT side (Player scores)
        elif self.ball.x + self.ball.width > self.width:
            self.score_player += 1
            self.play_sound(self.sound_score)
            self.ball.reset()
            score_updated = True

        # Task 2: Check game-over condition
        if score_updated and (self.score_player >= self.winning_score or self.score_ai >= self.winning_score):
            self.game_over = True

    def render(self, screen):
        """Render all game elements"""
        # Colors
        WHITE = (255, 255, 255)
        BLUE = (100, 150, 255)
        RED = (255, 100, 100)
        GRAY = (200, 200, 200)

        # Draw center line (dashed)
        for y in range(0, self.height, 20):
            pygame.draw.rect(screen, WHITE, (self.width // 2 - 2, y, 4, 10))

        # Draw paddles
        # Player paddle (LEFT) - Blue tint
        pygame.draw.rect(screen, BLUE, self.player.rect())
        # AI paddle (RIGHT) - Red tint
        pygame.draw.rect(screen, RED, self.ai.rect())

        # Draw ball
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())

        # Draw scores with labels
        # LEFT side (Player score)
        player_label = self.smallfont.render("PLAYER", True, BLUE)
        screen.blit(player_label, (self.width // 4 - player_label.get_width() // 2, 20))

        score_player_text = self.font.render(str(self.score_player), True, WHITE)
        screen.blit(score_player_text, (self.width // 4 - score_player_text.get_width() // 2, 50))

        # RIGHT side (AI score)
        ai_label = self.smallfont.render("AI", True, RED)
        screen.blit(ai_label, (self.width * 3 // 4 - ai_label.get_width() // 2, 20))

        score_ai_text = self.font.render(str(self.score_ai), True, WHITE)
        screen.blit(score_ai_text, (self.width * 3 // 4 - score_ai_text.get_width() // 2, 50))

        # Task 2: Game over overlay with winner display
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            # Display winner
            winner = "YOU WIN!" if self.score_player >= self.winning_score else "AI WINS!"
            winner_color = BLUE if self.score_player >= self.winning_score else RED

            winner_text = self.bigfont.render(winner, True, winner_color)
            screen.blit(winner_text, (self.width // 2 - winner_text.get_width() // 2, self.height // 2 - 120))

            # Task 3: Display replay options
            replay_text = self.font.render("Press 3, 5, or 7 for Best of...", True, GRAY)
            screen.blit(replay_text, (self.width // 2 - replay_text.get_width() // 2, self.height // 2 - 20))

            exit_text = self.smallfont.render("Press ESC to Exit", True, GRAY)
            screen.blit(exit_text, (self.width // 2 - exit_text.get_width() // 2, self.height // 2 + 20))

            # Display final score
            final_score = self.font.render(f"Final Score You: {self.score_player} AI: {self.score_ai}", True, GRAY)
            screen.blit(final_score, (self.width // 2 - final_score.get_width() // 2, self.height // 2 + 70))

    def handle_game_over_event(self, event):
        """Task 3: Handle replay option after game over"""
        if not self.game_over:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                self.reset_game(3)
                print("Starting Best of 3")
            elif event.key == pygame.K_5:
                self.reset_game(5)
                print("Starting Best of 5")
            elif event.key == pygame.K_7:
                self.reset_game(7)
                print("Starting Best of 7")
            elif event.key == pygame.K_ESCAPE:
                print("Exiting game...")
                pygame.quit()
                raise SystemExit

    def reset_game(self, best_of):
        """Task 3: Reset game with new winning score"""
        self.score_player = 0
        self.score_ai = 0
        self.winning_score = best_of
        self.ball.reset()
        self.game_over = False

        # Reset paddle positions
        self.player.y = self.height // 2 - 50
        self.ai.y = self.height // 2 - 50
