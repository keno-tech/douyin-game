import logging
import config
from douyin import Douyin
import pygame
import random
from Entity import Entity
import threading
from collections import Counter

def run_pygame(entities):
    running = True
    paused = False
    e = Entity("test", (1, 1, 1), 1, 1, 1, 1, 1, 1)
    leaderboard = Counter()
    leaderboard_font = pygame.font.Font(None, 36)
    
    gold = pygame.image.load('resources/gold.png')
    aspect_ratio_gold = gold.get_width() / gold.get_height()
    gold = pygame.transform.scale(gold, (25, int(25 / aspect_ratio_gold)))
    
    silver = pygame.image.load('resources/silver.png')
    aspect_ratio_silver = silver.get_width() / silver.get_height()
    silver= pygame.transform.scale(silver, (25, int(25 / aspect_ratio_silver)))

    bronze = pygame.image.load('resources/bronze.png')
    aspect_ratio_bronze = bronze.get_width() / bronze.get_height()
    bronze = pygame.transform.scale(bronze, (25, int(25 / aspect_ratio_bronze)))


    pygame.init()
    screen = pygame.display.set_mode((e.WIDTH, e.HEIGHT))
    pygame.display.set_caption("Douyin Game")
    clock = pygame.time.Clock()

    # Create a sprite group and add all entities to it
    entity_group = pygame.sprite.Group()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop when the user closes the window
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

        if not paused:
            screen.fill(e.GREY)
            for entity in entities:
                pygame.draw.rect(screen, entity.color, entity.rect)
                text = e.FONT.render(str(entity.id), True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.midtop = entity.rect.midbottom 
                screen.blit(text, text_rect)
                
                if entity.state == "wandering":
                    entity.detect_bounce()
                    entity.move(entities)  # Pass 'entities' instead of 'entity_group'
                    entity.handle_collisions(entities, leaderboard)  # Pass 'entities' instead of 'entity_group'

            entity_group.draw(screen)
        
            leaderboard_text = "Leaderboard:"
        
            text = leaderboard_font.render(leaderboard_text, True, (0, 0, 0))
            location = 10
            screen.blit(text, (location, location))

            screen.blit(gold, (10, 40))
            screen.blit(silver, (10, 90))
            screen.blit(bronze, (10, 140))
            
            for i, (entity_name, count) in enumerate(leaderboard.most_common(3)):
                location += 48
                background_color = (255, 223, 0) if i == 0 else (169, 169, 169) if i == 1 else (205, 127, 50)
                
                # Render the text and get its width
                text = e.FONT.render(f"{entity_name}: {count}", True, (0, 0, 0))
                text_width = text.get_width()
                
                # Create a background rectangle with a width that fits the text
                pygame.draw.rect(screen, background_color, (40, location, text_width + 10, 36))
                
                screen.blit(text, (40, location))
                
        pygame.display.flip()
        clock.tick(e.FPS)

    pygame.quit()

def run_webscoket(entities):
    dy = Douyin(url, entities)
    dy.connect_web_socket()

if __name__ == '__main__':
    entities = []  # This is the shared list for entities

    url = config.content['url']
    logging.basicConfig(level=config.content['log']['level'], format=config.content['log']['format'])

    pygame_thread = threading.Thread(target=run_pygame, args=(entities,))
    websocket_thread = threading.Thread(target=run_webscoket, args=(entities,))

    pygame_thread.start()
    websocket_thread.start()

    # Wait for both threads to finish
    pygame_thread.join()
    websocket_thread.join()
