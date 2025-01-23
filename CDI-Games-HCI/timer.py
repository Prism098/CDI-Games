import pygame
import math


class Timer:
    def __init__(self, total_seconds, x, y, font, radius=50):
        self.total_time = total_seconds  # Total time for the timer in seconds
        self.time_left = total_seconds  # Time remaining in seconds
        self.font = font  # Font for rendering the timer text
        self.x = x  # X position of the timer text
        self.y = y  # Y position of the timer text
        self.radius = radius  # Radius of the circular timer
        self.start_time = pygame.time.get_ticks()  # Start time in milliseconds

    def update(self):
        # Calculate the elapsed time in seconds
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Convert to seconds
        self.time_left = max(0, self.total_time - elapsed_time)  # Update the time left in seconds

    def draw(self, screen):
        # Render the remaining time as text
        timer_text = str(int(self.time_left))  # Convert time_left to an integer (seconds)
        text_surface = self.font.render(timer_text, True, (255, 0, 0))  # Red color for the timer text
        screen.blit(text_surface, (self.x-1540, self.y+850))

         # Draw the circular countdown timer
        angle = 360 * (self.time_left / self.total_time)  # Calculate the angle for the arc
        end_angle = math.radians(angle)
        pygame.draw.arc(screen, (255, 255, 255), (self.x - 1650, self.y+750, self.radius * 5, self.radius * 5), 0, end_angle, 5)

    def is_time_up(self):
        # Check if the timer has finished (i.e., time_left is 0)
        return self.time_left <= 0
    
    def stop(self):
        """Stop the timer from counting down"""
        self.running = False
        self.time_left = 0