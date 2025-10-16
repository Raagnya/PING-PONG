import pygame

class Paddle:
    def __init__(self, x, y, width, height, screen_height, speed=6):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_height = screen_height
        self.speed = speed

    def move(self, up=True):
        """Move paddle up or down within screen bounds"""
        if up:
            self.y -= self.speed
        else:
            self.y += self.speed

        # Keep paddle within screen bounds
        # Clamps the self.y value between 0 (top) and screen_height - self.height (bottom)
        self.y = max(0, min(self.y, self.screen_height - self.height))

    def auto_move(self, ball):
        """AI movement to track the ball"""
        ball_center_y = ball.y + ball.height / 2
        paddle_center_y = self.y + self.height / 2

        # Add a small deadzone to make AI less perfect
        deadzone = 10

        if ball_center_y < paddle_center_y - deadzone:
            self.move(up=True)
        elif ball_center_y > paddle_center_y + deadzone:
            self.move(up=False)

    def rect(self):
        """Return pygame Rect for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
