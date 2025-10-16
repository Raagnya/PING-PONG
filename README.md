This project is a terminal-based ping pong game using **Pygame**. It introduces students to interactive game design using object-oriented principles and real-time graphical rendering.Task 1: Refine Ball Collision (Requires External Check)
 Problem: At higher ball speeds, the ball was passing through the paddles instead of bouncing off them properly.
WHAT THINGS WE ADDED:
Enhance Collision Accuracy
The actual collision check logic (self.ball.check_collision) resides in the separate ball.py file (which is imported). The GameEngine simply calls this method. The high-speed pass-through issue cannot be fixed here; it must be addressed in the Ball class.
TASK 2:Implement Game Over Condition
Problem: The game lacked a proper ending condition — it ran indefinitely without showing a winner
WHAT THINGS WE ADDED:
The update() method checks the boolean score_updated and sets self.game_over = True if self.score_player or self.score_ai meets or exceeds self.winning_score (default is 5). 
The render() method checks if self.game_over: and draws a semi-transparent overlay, displays the "YOU WIN!" or "AI WINS!" message, and shows the final score.
TASK 3: Add Replay Option
Problem: After Game Over, players couldn’t restart or choose new game settings.
WHAT THINGS WE ADDED:
The handle_game_over_event() method listens for pygame.KEYDOWN events for keys K_3, K_5, K_7, and K_ESCAPE.
The reset_game(self, best_of) method successfully resets scores to zero, sets the new self.winning_score, resets the ball, and sets self.game_over = False, making the game playable again.
Task 4: Add Sound Feedback 
 Problem: The original version lacked sound, making the gameplay feel less dynamic and engaging.
WHAT THINGS WE ADDED:
The __init__ method correctly loads the three required files (paddle_hit.wav, wall_bounce.wav, score.wav) using pygame.mixer.Sound().
The code correctly uses os.path.join(base_dir, "sounds") to locate the sounds directory relative to the game_engine.py file.
The update() method plays the correct sound for the corresponding event: self.sound_wall after a wall bounce, self.sound_paddle after a paddle hit, and self.sound_score after a point is scored
