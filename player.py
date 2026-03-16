import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0

    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        # point
        a = self.position + forward * self.radius
        # base left
        b = self.position - forward * self.radius - right
        # base right
        c = self.position - forward * self.radius + right

        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += dt * PLAYER_TURN_SPEED
        
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_DOWN]:
            self.move(-dt)
    
    def move(self, dt):
        # a unit vector in a normed vector space is a vector 
        # (often a spatial vector) of length 1. A unit vector is 
        # often denoted by a lowercase letter with a circumflex, or "hat", as in 
        # ^v. The term normalized vector is sometimes used as a synonym for
        # unit vector.
        
        # So:
        # 1. Draw a vector from 0,0 to 0,1 (pointing up)
        # 2. Rotate Sideways by the player's rotation
        # 3. Adjust the speed
        # 4. Move the player
        unit_vector = pygame.Vector2(0,1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position+=rotated_with_speed_vector