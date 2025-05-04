from constant import *
import pygame
from highscore import *


def show_highscores(screen):
    # Initialize font
    font = pygame.font.Font(None, 50)

    # Read highscores
    highscores = read_highscores()

    # Highscore loop
    highscore_active = True
    while highscore_active:
        screen.fill((0, 0, 0))  # Black background

        # Render highscores
        title_text = font.render("Highscores", True, (255, 255, 255))
        screen.blit(title_text, (WINDOW_WIDTH // 2 -
                    title_text.get_width() // 2, 50))

        for i, score in enumerate(highscores):
            score_text = font.render(
                f"{i + 1}. {score}", True, (255, 255, 255))
            screen.blit(score_text, (WINDOW_WIDTH // 2 -
                        score_text.get_width() // 2, 100 + i * 50))

        # Adjust back button position to avoid collision
        back_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, 100 + len(highscores) * 50 + 50, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), back_button)
        back_text = font.render("Back", True, (255, 255, 255))
        screen.blit(back_text, (back_button.x + 100 - back_text.get_width() //
                    2, back_button.y + 25 - back_text.get_height() // 2))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    highscore_active = False  # Exit highscore screen

        pygame.display.update()


def show_menu(screen):
    # Initialize font
    font = pygame.font.Font(None, 50)  # Default font, size 50

    # Define button properties
    button_width, button_height = 200, 50
    start_button = pygame.Rect(
        WINDOW_WIDTH // 2 - button_width // 2, 200, button_width, button_height)
    highscore_button = pygame.Rect(
        WINDOW_WIDTH // 2 - button_width // 2, 300, button_width, button_height)
    exit_button = pygame.Rect(
        WINDOW_WIDTH // 2 - button_width // 2, 400, button_width, button_height)

    # Menu loop
    menu_active = True
    while menu_active:
        screen.fill((0, 0, 0))  # Black background

        # Draw buttons
        pygame.draw.rect(screen, (255, 0, 0), start_button)  # Red Start button
        # Green Highscore button
        pygame.draw.rect(screen, (0, 255, 0), highscore_button)
        pygame.draw.rect(screen, (0, 0, 255), exit_button)  # Blue Exit button

        # Render button text
        start_text = font.render("Start", True, (255, 255, 255))
        highscore_text = font.render("Highscores", True, (255, 255, 255))
        exit_text = font.render("Exit", True, (255, 255, 255))

        # Center text on buttons
        screen.blit(start_text, (start_button.x + button_width // 2 - start_text.get_width() //
                    2, start_button.y + button_height // 2 - start_text.get_height() // 2))
        screen.blit(highscore_text, (highscore_button.x + button_width // 2 - highscore_text.get_width() //
                    2, highscore_button.y + button_height // 2 - highscore_text.get_height() // 2))
        screen.blit(exit_text, (exit_button.x + button_width // 2 - exit_text.get_width() //
                    2, exit_button.y + button_height // 2 - exit_text.get_height() // 2))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return "start"
                if highscore_button.collidepoint(event.pos):
                    # Call a function to display highscores
                    show_highscores(screen)
                if exit_button.collidepoint(event.pos):
                    return "quit"

        pygame.display.update()
