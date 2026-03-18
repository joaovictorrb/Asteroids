import random

import pygame
from logger import log_event
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
        
    def update(self, dt):
        self.position += self.velocity * dt
        
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        origin_asteroid = self.velocity
        asteroid_child_one = origin_asteroid.rotate(angle) # rotated clockwise
        asteroid_child_two = origin_asteroid.rotate(-angle) # rotated counter-clockwise
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        child_one = Asteroid(self.position.x, self.position.y, new_radius)
        child_one.velocity = asteroid_child_one * 1.2

        child_two = Asteroid(self.position.x, self.position.y, new_radius)
        child_two.velocity = asteroid_child_two * 1.2