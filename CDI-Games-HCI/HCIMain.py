import pygame
import sys

# Initialize Pygame and the font module
pygame.init()
pygame.font.init()

from game import GameState

# Screen dimensions
ORANGE = (255, 98, 40)
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Website Interface Builder Game")

def calculate_score(game_state):
    """Calculate total score based on all correct choices"""
    score = 0
    
    # Check for orange color
    if game_state.grey_color == ORANGE and not game_state.color_condition_met:
        score += 1000
        game_state.color_condition_met = True  # Mark that we've met the color condition
    
    # Check for happy sticker
    if game_state.sticker_placed and game_state.ui_stickers[0].placed and not game_state.sticker_condition_met:
        score += 1000
        game_state.sticker_condition_met = True  # Mark that we've met the sticker condition
    
    # Check for Comic Sans
    if game_state.font_name == "comicsansms" and not game_state.font_condition_met:
        score += 1000
        game_state.font_condition_met = True  # Mark that we've met the font condition
    
    return score

def main():
    game_state = GameState()
    clock = pygame.time.Clock()
    running = True
    total_score = 0
    previous_score = total_score  # Initialize previous_score
    
    # Print the initial score when the app starts
    print(f"Score: {total_score}")
    
    while running:
        dt = clock.tick(60) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle the event
            game_state.handle_event(event)
            
            # Calculate score if conditions are met
            score_change = calculate_score(game_state)
            total_score += score_change
            
            # Ensure the score does not exceed 3000
            total_score = min(total_score, 3000)
            
            # Update the score in game state
            game_state.score = total_score
            
            # Print the score only if it has changed
            if total_score != previous_score:
                print(f"Score: {total_score}")
                previous_score = total_score
        
        # Update timer and check for time-based scoring
        game_state.update_timer(dt)
        
        # Draw everything
        game_state.draw(screen)
        pygame.display.flip()
        
    pygame.quit()
    print(f"Score: {total_score}")
    sys.exit()

if __name__ == "__main__":
    main()