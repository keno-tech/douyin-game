import pygame
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
FPS = 30
WHITE = (255, 255, 255)
GREY = (192, 192, 192)  # Grey color
COLLISION_RADIUS = 100
NUM_ENTITIES = 100  # Number of entities

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulator")
clock = pygame.time.Clock()

# Define game state variables
running = True
paused = False
enemies = {"one":"three", "two":"one", "three":"two"}
entity_counts = {"one": 0, "two": 0, "three": 0}



class Entity(pygame.sprite.Sprite):
    def __init__(self, id, image, x, y, width, height, speed_x, speed_y):
        super().__init__()
        self.id = id
        
        self.name = image.split(".")[0][10:]
        self.image_file = image
        self.enemy = enemies[self.name]
        self.original_image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.state = "wandering"
        self.width = width
        self.height = height
    
    def detect_bounce(self):
        # Bounce off the edges of the screen
        if entity.rect.left < 0 or entity.rect.right > WIDTH:
            entity.speed_x *= -1
        if entity.rect.top < 0 or entity.rect.bottom > HEIGHT:
            entity.speed_y *= -1
    
    def handle_collisions(self, entities_group):
        for entity in entities_group:
            if entity != self:  # Exclude self from consideration
                # Calculate the distance between self and the other entity
                distance = pygame.math.Vector2(entity.rect.centerx - self.rect.centerx,
                                               entity.rect.centery - self.rect.centery).length()

                # Check for collision only if the entities are within the collision radius
                if distance <= COLLISION_RADIUS:
                    collisions = pygame.sprite.collide_rect(self, entity)
                    if collisions:
                        if self.name != entity.name:
                            if enemies[self.name] == entity.name:
                                winner = self
                                loser = entity
                            elif enemies[entity.name] == self.name:
                                winner = entity
                                loser = self
                            else:
                                continue

                            # entities_group.remove(loser)
                            loser.image = winner.image
                            loser.name = winner.name
                            loser.enemy = winner.enemy

    def move(self, entities_group):
        closest_enemy = None
        closest_distance = float('inf')
        speed_x = 0
        speed_y = 0

        for entity in entities_group:
            if entity.name == self.enemy and entity != self:  # Exclude self from consideration
                delta_x = entity.rect.centerx - self.rect.centerx
                delta_y = entity.rect.centery - self.rect.centery
                distance = delta_x**2 + delta_y**2

                if distance < closest_distance:
                    closest_distance = distance
                    closest_enemy = entity

        if closest_enemy is not None:
            delta_x = closest_enemy.rect.centerx - self.rect.centerx
            delta_y = closest_enemy.rect.centery - self.rect.centery

            length = max(abs(delta_x), abs(delta_y))
            if length > 0:
                speed_x = (delta_x / length)
                speed_y = (delta_y / length)

            # Update speed_x and speed_y
            self.speed_x = speed_x
            self.speed_y = speed_y
      

        self.rect.x += self.speed_x 
        self.rect.y += self.speed_y 
            

        

    

# Create a list to store all the entities
entities = []

# Create and initialize the entities with random positions and movements
for i in range(100):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    id = i
    width = 50
    height = 50
    image_filename = random.choice(["resources/one.png", "resources/two.png", "resources/three.png"])  # Randomly choose an image
      # Random initial speed in x direction
    entity = Entity(id, image_filename, x, y, width, height, 0, 0)
    entities.append(entity)

# Create a sprite group and add all entities to it
entity_group = pygame.sprite.Group(entities)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  
                paused = not paused

    if not paused:
        entity_counts = {"one": 0, "two": 0, "three": 0}

        for entity in entity_group:
            if entity.state == "wandering":
                entity.detect_bounce()
                entity.move(entity_group)
                entity.handle_collisions(entity_group)
                entity_counts[entity.name] += 1
        
        for i in entity_counts.values():
            if i == 100:
                paused = not paused
    
    font = pygame.font.Font(None, 36)

        
    screen.fill(GREY)
    for entity in entity_group:
        pygame.draw.rect(screen, (0, 0, 0), entity.rect, 2)  # Draw red rectangles
        text = font.render(entity.name, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.midtop = entity.rect.midbottom  # Position the name below the sprite
        screen.blit(text, text_rect)

    entity_group.draw(screen)
    leaderboard_text = "Entities:"
    
    text = font.render(leaderboard_text, True, (0, 0, 0))
    location = 10
    screen.blit(text, (location, location))
    
    for entity_name, count in entity_counts.items():
        location += 30
        text = font.render(f"{entity_name}: {count}", True, (0, 0, 0))
        screen.blit(text, (10, location))

    
    pygame.display.flip()
    clock.tick(FPS)
    

pygame.quit()
