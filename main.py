import sys
import pygame
from src.actor.asteroid.asteroid import Asteroid
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TEXT_COLOR
from src.utils.logger import log_state, log_event
from src.actor.player.player import Player
from src.actor.asteroid.asteroidfield import AsteroidField
from src.actor.player.shot import Shot
from src.components.menu.menu import Menu
    
def main():
    pygame.init()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0)
    pygame.display.set_caption("Asteroids")
    
    # Game variables
    game_loop = True
    game_pause = True
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

    menu = Menu(screen)
    
    # Start game_loop
    while game_loop:
        
        # Check if game is paused
#         if game_pause:
#            print("STARTING GAME")
# +          game_pause = False
#         else:
#             pass

        log_state()
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("PAUSE AND MENU")
                    game_pause = True
                if event.key==pygame.K_RETURN:
                    print("STARTING GAME")
                    game_pause = False
            if event.type == pygame.QUIT:
                game_loop = False

        pygame.display.update()
        if game_pause:
            menu.draw()
            pygame.display.flip()
            dt = clock.tick(60) / 1000
            continue
        
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
