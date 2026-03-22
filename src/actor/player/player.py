import pygame
from src.actor.circleshape import CircleShape
from src.utils.constants import LINE_WIDTH, PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN_SECONDS, PLAYER_SHOT_SPEED, PLAYER_TURN_SPEED, PLAYER_SPEED, SHOT_RADIUS
from src.actor.player.shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cdr = 0

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
        # draw the circle hitbox in red for comparison
        pygame.draw.circle(screen, "red", (int(self.position.x), int(self.position.y)), self.radius, 1)

    def rotate(self, dt):
        self.rotation += dt * PLAYER_TURN_SPEED
        
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shot_cdr -= dt
        
        if keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_DOWN]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.shot_cdr <= 0:
                self.shot_cdr = PLAYER_SHOOT_COOLDOWN_SECONDS
                self.shoot()
    
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
    
    # defining the exact collision detection between the player and the asteroids
    def collides_with(self, other):
        # get vertices
        verts = self.triangle()
        
        for i in range(len(verts)):
            # get two adjacent vertices to form one edge of the triangle
            edge = verts[(i + 1) % len(verts)] - verts[i]

            # the separating axis is perpendicular to the edge
            # rotating (x, y) by 90 degrees gives (-y, x)
            axis = pygame.Vector2(-edge.y, edge.x).normalize()

            # project each triangle vertex onto the axis (dot product = scalar position along axis)
            dots = [v.dot(axis) for v in verts]
            tri_min, tri_max = min(dots), max(dots)

            # project the circle onto the same axis
            # the circle's projection is its center +/- its radius
            center_proj = other.position.dot(axis)
            circle_min = center_proj - other.radius
            circle_max = center_proj + other.radius

            # if the two projections don't overlap, there's a gap — no collision possible
            if tri_max < circle_min or circle_max < tri_min:
                return False

            # extra axis: from the circle center toward the closest triangle vertex
            # this catches corner cases where edge normals alone miss a separation
            closest = min(verts, key=lambda v: v.distance_to(other.position))
            axis = (other.position - closest).normalize()

            dots = [v.dot(axis) for v in verts]
            tri_min, tri_max = min(dots), max(dots)

            center_proj = other.position.dot(axis)
            circle_min = center_proj - other.radius
            circle_max = center_proj + other.radius

            if tri_max < circle_min or circle_max < tri_min:
                return False

            # all axes tested, no separating axis found — shapes are colliding
            return True
        
    def shoot(self):
        # create a new shot at the player's position, moving in the direction the player is facing
        new_shot = Shot(self.position.x, self.position.y)
        # .rotate() the vector in the direction the player is facing.
        new_shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED