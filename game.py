import pygame
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
FPS = 30
WHITE = (255, 255, 255)
GREY = (192, 192, 192)  # Grey color
COLLISION_RADIUS = 10
NUM_ENTITIES = 100  # Number of entities
FONT = pygame.font.Font(None, 24)


# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulator")
clock = pygame.time.Clock()

# Define game state variables
running = True
paused = False

class Entity(pygame.sprite.Sprite):
    def __init__(self, id, color, x, y, width, height, speed_x, speed_y):
        super().__init__()
        self.id = id
        self.color = color
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.state = "wandering"
        self.width = width
        self.height = height
    
    def detect_bounce(self):
        # Bounce off the edges of the screen
        # Bounce off the edges of the screen
        if self.rect.left < 0:
            self.speed_x = abs(self.speed_x)  # Reverse horizontal speed
        elif self.rect.right > WIDTH:
            self.speed_x = -abs(self.speed_x)  # Reverse horizontal speed
        if self.rect.top < 0:
            self.speed_y = abs(self.speed_y)  # Reverse vertical speed
        elif self.rect.bottom > HEIGHT:
            self.speed_y = -abs(self.speed_y)  # Reverse vertical speed

    
    def handle_collisions(self, entities_group):
        for entity in entities_group:
            if entity != self:  
                distance = pygame.math.Vector2(entity.rect.centerx - self.rect.centerx,
                                               entity.rect.centery - self.rect.centery).length()

                # Check for collision only if the entities are within the collision radius
                if distance <= COLLISION_RADIUS:
                    collisions = pygame.sprite.collide_rect(self, entity)
                    if collisions:
                            loser = random.choice([entity, self])
                            entities_group.remove(loser)

    def move(self, entities_group):
        closest_enemy = None
        closest_distance = float('inf')
   
        for entity in entities_group:
            if entity != self:  # Exclude self from consideration
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
                self.speed_x = speed_x 
                self.speed_y = speed_y 
      
        self.rect.x += self.speed_x 
        self.rect.y += self.speed_y 

# Create a list to store all the entities
entities = []

# Create and initialize the entities with random positions and movements
for i in range(NUM_ENTITIES):
    x = random.randint(0, WIDTH - 10)
    y = random.randint(0, HEIGHT- 10)
    id = i
    width = 20
    height = 20
    color = (random.randint(0, 255), random.randint(0,255), random.randint(0,255))  # Randomly choose a color
    speed_x = random.uniform(-1, 1)
    speed_y = random.uniform(-1, 1)
    entity = Entity(id, color, x, y, width, height, speed_x, speed_y)
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
        screen.fill(GREY)
        for entity in entity_group:
            pygame.draw.rect(screen, entity.color, entity.rect)
            text = FONT.render(str(entity.id), True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.midtop = entity.rect.midbottom 
            screen.blit(text, text_rect)
            
            if entity.state == "wandering":
                entity.detect_bounce()
                entity.move(entity_group)
                entity.handle_collisions(entity_group)        
     
        entity_group.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
