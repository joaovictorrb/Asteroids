import sys
import pygame
import button
from asteroid import Asteroid
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TEXT_COLOR
from logger import log_state, log_event
from player import Player
from asteroidfield import AsteroidField
from shot import Shot
# Define font
font = pygame.font.SysFont("Arial", 32)

# Load button images
resume_img = pygame.image.load("assets/btn_resume.png").convert_alpha()

# Create button instances
resume_button = button.Button(SCREEN_WIDTH / 2 - resume_img.get_width() / 2, SCREEN_HEIGHT / 2 - resume_img.get_height() / 2, resume_img, 1)


def draw_text(text, font, x, y, screen):
    img = font.render(text, True, TEXT_COLOR)
    screen.blit(img, (x, y))
    

def main():
    pygame.init()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0)
    pygame.display.set_caption("Asteroids")
    
    # Game variables
    game_loop = True
    game_pause = False
    clock = pygame.time.Clock()
    dt = 0
    
    # Group class is a container that holds and manages multiple game objects.
    # You can think of them as a sort of Venn diagram. 
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroid = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroid)
    AsteroidField.containers = (updatable,)
    Shot.containers = (updatable, drawable, shots)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    AsteroidField()

    # Start game_loop
    while game_loop:
        
        # Check if game is paused
        if game_pause:
            resume_button.draw(screen)
            # Display menu
        else:
            draw_text("Asteroids", font, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, screen)

        log_state()
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("PAUSE AND MENU")
                    game_pause = True
                if event.key==pygame.K_RETURN:
                    print("STARTING GAME")
            if event.type == pygame.QUIT:
                game_loop = False

        pygame.display.update()
        
        # first update all the game objects
        for sprite in updatable:
            sprite.update(dt)
        
        for sprite in asteroid:
            # log if there is a collision between the player and any asteroid
            # if there is a collision, kill the player and end the game
            if sprite.collides_with(player):
               log_event("player_hit")
               print("Game Over!")
               sys.exit()
            # log if there is a collision between any asteroid and any shot
            # if there is a collision, kill the asteroid and the shot
            for shot in shots:
                if sprite.collides_with(shot):
                    log_event("asteroid_shot")
                    sprite.split()

        # Fill the screen
        screen.fill("black")
        
        # Draw all sprites
        for sprite in drawable:
            sprite.draw(screen)
        
        
        # player.draw(screen)
        # player.update(dt)
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
