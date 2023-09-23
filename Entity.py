
import pygame
import random
pygame.init()




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
        self.WIDTH, self.HEIGHT = 1536, 800
        self.FPS = 30
        self.WHITE = (255, 255, 255)
        self.GREY = (192, 192, 192)  # Grey color
        self.COLLISION_RADIUS = 10
        self.NUM_ENTITIES = 100  # Number of entities
        self.FONT = pygame.font.Font("resources/LiSu.ttf",20)
    
    def detect_bounce(self):
        # Bounce off the edges of the screen
        # Bounce off the edges of the screen
        if self.rect.left < 0:
            self.speed_x = abs(self.speed_x)  # Reverse horizontal speed
        elif self.rect.right > self.WIDTH:
            self.speed_x = -abs(self.speed_x)  # Reverse horizontal speed
        if self.rect.top < 0:
            self.speed_y = abs(self.speed_y)  # Reverse vertical speed
        elif self.rect.bottom > self.HEIGHT:
            self.speed_y = -abs(self.speed_y)  # Reverse vertical speed

    
    def handle_collisions(self, entities_group, leaderboard):
        for entity in entities_group:
            if entity != self:  
                distance = pygame.math.Vector2(entity.rect.centerx - self.rect.centerx,
                                            entity.rect.centery - self.rect.centery).length()

                # Check for collision only if the entities are within the collision radius
                if distance <= self.COLLISION_RADIUS:
                    collisions = pygame.sprite.collide_rect(self, entity)
                    if collisions:
                        r = random.randint(1, 2)
                        if r == 1:
                            entities_group.remove(entity)
                        else:
                            entities_group.remove(self)
                       
                        leaderboard[entity.id] += 1
                            

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
