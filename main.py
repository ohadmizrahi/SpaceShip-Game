
import pygame
from Model.spaceship import Spaceship
from Model.window import Window
from Model.objects import Bullet, BigBullet, Stone
import random

pygame.font.init()
pygame.mixer.init()

# TODO sections: 1.2, 1.11, 1.1 

# Global Variables
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 44
WIDTH, HEIGHT = 1200, 700 # section 1.8 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0) 
SPACESHIP_STEP = 5 
OBJECTS_STEP = 7
MAX_BULLET = 5 # section 1.6
STONES = []

# Keyboard Keys
blue_keys = {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s}
red_keys = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}

# Create objects
def create_game_objects():
    window = Window(WIDTH, HEIGHT, 'space.png', 60)
    blue_spaceship = Spaceship(75, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT,
                                'blue_spaceship.png', 90, blue_keys, 10, MAX_BULLET, 1, 'blue')
    red_spaceship = Spaceship(window.width-100, 300, SPACESHIP_WIDTH,
                            SPACESHIP_HEIGHT, 'new_red_spaceship.png', 270, red_keys, 10, MAX_BULLET, 1, 'red')                
    return blue_spaceship, red_spaceship, window

def listen_events(blue_spaceship, red_spaceship, window):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run - False
                    pygame.quit()
                if event.key == pygame.K_LCTRL:
                    bullet = Bullet(50, 25, blue_spaceship, 'blue_bullets.png', OBJECTS_STEP, 1)
                    blue_spaceship.shoot(bullet)
                if event.key == pygame.K_RCTRL:
                    bullet = Bullet(50, 25, red_spaceship, 'red_bullets.png', OBJECTS_STEP, -1)
                    red_spaceship.shoot(bullet)
                if event.key == pygame.K_RSHIFT: # section 1.9
                    big_bullet = BigBullet(100, 50, red_spaceship, 'red_bullets.png', OBJECTS_STEP, -1)
                    red_spaceship.shoot(big_bullet)
                if event.key == pygame.K_LSHIFT: # section 1.9
                    big_bullet = BigBullet(100, 50, blue_spaceship, 'blue_bullets.png', OBJECTS_STEP, 1)
                    blue_spaceship.shoot(big_bullet)
                if event.key == pygame.K_SPACE: # section 1.10
                    stone = Stone(random.choice([0,window.width-50]), random.randint(0, window.height-50), 50, 50, 'stone.png', OBJECTS_STEP)
                    STONES.append(stone)
                if event.key == pygame.K_TAB: # section 1.11 bonus
                    pass
                if event.key == pygame.K_KP_ENTER:
                    restart_game()


def end_game(spaceship1, spaceship2, window):
    if spaceship1.explode():
        window.write_to_window(f'Game over - Winner is {str(spaceship2)}', 40, (250,300)) # section 1.4
        pygame.time.delay(5000)
        return True
    elif spaceship2.explode():
        window.write_to_window(f'Game over - Winner is {str(spaceship1)}', 40, (250,300)) # section 1.4
        pygame.time.delay(5000)
        return True
    else:
        return False

def restart_game():
    main()

def main():
    blue_spaceship, red_spaceship, window = create_game_objects()
    window.create_title('SpaceShip Game')
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(window.fps)
        listen_events(blue_spaceship, red_spaceship, window)
        if end_game(red_spaceship, blue_spaceship, window): # section 1.4
            restart_game() # section 1.4

        blue_spaceship.move(SPACESHIP_STEP, window)
        red_spaceship.move(SPACESHIP_STEP, window)
        window.handle_objects_movement(red_spaceship.stack)
        window.handle_objects_movement(blue_spaceship.stack)
        window.handle_objects_movement(STONES)
        window.handle_objects_events(blue_spaceship, red_spaceship, STONES)
        window.draw_window([red_spaceship, blue_spaceship], {'red_stack': red_spaceship._stack, 'blue_stack': blue_spaceship._stack}, STONES)

if __name__ == "__main__":
    main()
