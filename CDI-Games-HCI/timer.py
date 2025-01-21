import pygame

class Timer:
    def __init__(self, total_seconds, x, y, font):
        self.total_time = total_seconds  # Total time for the timer in seconds
        self.time_left = total_seconds  # Time remaining in seconds
        self.font = font  # Font for rendering the timer text
        self.x = x  # X position of the timer text
        self.y = y  # Y position of the timer text
        self.start_time = pygame.time.get_ticks()  # Start time in milliseconds

    def update(self):
        # Calculate the elapsed time in seconds
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Convert to seconds
        self.time_left = max(0, self.total_time - elapsed_time)  # Update the time left in seconds

    def draw(self, screen):
        # Render the remaining time as text
        timer_text = str(int(self.time_left))  # Convert time_left to an integer (seconds)
        text_surface = self.font.render(timer_text, True, (255, 0, 0))  # Red color for the timer text
        screen.blit(text_surface, (self.x, self.y))

    def is_time_up(self):
        # Check if the timer has finished (i.e., time_left is 0)
        return self.time_left <= 0
    def stop(self):
        """Stop the timer from counting down"""
        self.running = False
        self.time_left = 0