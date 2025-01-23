import pygame
from screens.menu_screen import show_menu
from screens.game_screen import start_game

# Initialiseer pygame
pygame.init()

def main():
    while True:
        # Startscherm weergeven
        choice = show_menu()
        if choice == "start":
            start_game()
        elif choice == "quit":
            break

    pygame.quit()

if __name__ == "__main__":
    main()
