#!/usr/bin/env python3
"""
Quick test to verify the display layout works correctly
"""
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants from the main game
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
GAME_WIDTH = 640
GAME_HEIGHT = 480
GAME_X_OFFSET = (WINDOW_WIDTH - GAME_WIDTH) // 2
GAME_Y_OFFSET = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Planetoids Display Test")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    # Load keyboard image
    try:
        keyboard_image = pygame.image.load("ZX81_keyboard.jpg")
        keyboard_width = WINDOW_WIDTH - 100
        keyboard_height = int(keyboard_width * keyboard_image.get_height() / keyboard_image.get_width())
        keyboard_image = pygame.transform.scale(keyboard_image, (keyboard_width, keyboard_height))
        print(f"Keyboard image loaded: {keyboard_image.get_size()}")
    except pygame.error as e:
        print(f"Could not load keyboard image: {e}")
        keyboard_image = None
    
    # Create game surface
    game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Fill background
        screen.fill((30, 30, 30))
        
        # Draw TV frame
        tv_frame_color = (40, 40, 40)
        tv_inner_color = (20, 20, 20)
        
        # Outer TV case
        pygame.draw.rect(screen, tv_frame_color, 
                        (GAME_X_OFFSET - 40, GAME_Y_OFFSET - 40, 
                         GAME_WIDTH + 80, GAME_HEIGHT + 80))
        
        # Inner bezel
        pygame.draw.rect(screen, tv_inner_color, 
                        (GAME_X_OFFSET - 20, GAME_Y_OFFSET - 20, 
                         GAME_WIDTH + 40, GAME_HEIGHT + 40))
        
        # Screen bezel
        bezel_color = (60, 60, 60)
        for i in range(5):
            pygame.draw.rect(screen, bezel_color, 
                            (GAME_X_OFFSET - 15 + i, GAME_Y_OFFSET - 15 + i, 
                             GAME_WIDTH + 30 - 2*i, GAME_HEIGHT + 30 - 2*i), 1)
        
        # TV brand label
        brand_text = small_font.render("SINCLAIR", True, (200, 200, 200))
        brand_rect = brand_text.get_rect(center=(WINDOW_WIDTH // 2, GAME_Y_OFFSET - 25))
        screen.blit(brand_text, brand_rect)
        
        # Fill game surface with test content
        game_surface.fill(BLACK)
        
        # Test content on game surface
        title_text = font.render("PLANETOIDS", True, WHITE)
        title_rect = title_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 50))
        game_surface.blit(title_text, title_rect)
        
        subtitle_text = small_font.render("ZX81 Classic Recreation", True, GREEN)
        subtitle_rect = subtitle_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2))
        game_surface.blit(subtitle_text, subtitle_rect)
        
        info_text = small_font.render("Display Test - Press ESC to exit", True, WHITE)
        info_rect = info_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 50))
        game_surface.blit(info_text, info_rect)
        
        # Blit game surface to main screen
        screen.blit(game_surface, (GAME_X_OFFSET, GAME_Y_OFFSET))
        
        # Draw keyboard
        if keyboard_image:
            keyboard_y = GAME_Y_OFFSET + GAME_HEIGHT + 60
            keyboard_x = (WINDOW_WIDTH - keyboard_image.get_width()) // 2
            screen.blit(keyboard_image, (keyboard_x, keyboard_y))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
