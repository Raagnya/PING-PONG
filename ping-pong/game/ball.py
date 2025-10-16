import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        # Store original position for reset
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Initial velocity values, set randomly upon initialization/reset
        self.velocity_x = random.choice([-6, 6])
        self.velocity_y = random.choice([-4, 4])


    def move(self):
        """
        Move ball with sub-stepping to prevent passing through paddles.
        This handles Task 2: Refine Ball Collision
        """
        # Determine number of steps based on max velocity component
        steps = max(int(abs(self.velocity_x)), int(abs(self.velocity_y)), 1)

        # Calculate delta movement per step
        dx = self.velocity_x / steps
        dy = self.velocity_y / steps

        # Iterate in steps (original code structure)
        # Note: In the final game engine loop, this only moves one step per frame for smooth collision checks.
        for _ in range(steps):
            self.x += dx
            self.y += dy

        # Bounce off top/bottom walls
        if self.y <= 0:
            self.y = 0  # Reposition to the edge
            self.velocity_y = abs(self.velocity_y) # Reverse direction
            return "wall"

        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height # Reposition to the edge
            self.velocity_y = -abs(self.velocity_y) # Reverse direction
            return "wall"

        return None

    def check_collision(self, player, ai):
        """Check collision with player and AI paddles."""
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()

        # Handle player paddle collision (left side, only if moving left)
        if ball_rect.colliderect(player_rect) and self.velocity_x < 0:
            # Position ball at right edge of player paddle
            self.x = player_rect.right
            self.velocity_x = abs(self.velocity_x) # Reverse direction

            # Add slight angle variation based on where ball hits paddle
            relative_intersect = (player.y + player.height / 2) - (self.y + self.height / 2)
            normalized_intersect = relative_intersect / (player.height / 2)
            # Increase/decrease vertical speed based on hit point
            self.velocity_y += normalized_intersect * 2 

            return "paddle"

        # Handle AI paddle collision (right side, only if moving right)
        elif ball_rect.colliderect(ai_rect) and self.velocity_x > 0:
            # Position ball at left edge of AI paddle
            self.x = ai_rect.left - self.width
            self.velocity_x = -abs(self.velocity_x) # Reverse direction

            # Add slight angle variation based on where ball hits paddle
            relative_intersect = (ai.y + ai.height / 2) - (self.y + self.height / 2)
            normalized_intersect = relative_intersect / (ai.height / 2)
            # Increase/decrease vertical speed based on hit point
            self.velocity_y += normalized_intersect * 2

            return "paddle"

        return None

    def reset(self):
        """Reset ball to center with random velocity"""
        self.x = self.original_x
        self.y = self.original_y

        # Always set fresh velocity values
        self.velocity_x = random.choice([-6, 6])
        # Randomize initial vertical direction and speed slightly
        self.velocity_y = random.choice([-4, -3, -2, 2, 3, 4])

    def rect(self):
        """Return pygame Rect for drawing and collision detection"""
        # Convert to int for pygame.Rect
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
