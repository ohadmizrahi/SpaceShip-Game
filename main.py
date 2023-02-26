
import pygame
from Model.spaceship import Spaceship
from Model.window import Window
from Model.objects import Bullet, BigBullet, Stone
import random
from typing import Tuple

pygame.font.init()
pygame.mixer.init()

# TODO sections: 1.11 

# Global Variables
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 44
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 700 # section 1.8 
BULLET_WIDTH, BULLET_HEIGHT = 50, 25
WHITE = (255, 255, 255)
BLACK = (0, 0, 0) 
SPACESHIP_STEP = 5 
OBJECTS_STEP = 7
MAX_BULLET = 5 # section 1.6
STONES = []
BG_IMG = 'new_space.png' # section 1.2
BLUE_SPACESHIP_IMG, RED_SPACESHIP_IMG = 'blue_spaceship.png', 'new_red_spaceship.png'
BLUE_BULLET_IMG, RED_BULLET_IMG = 'blue_bullets.png', 'red_bullets.png'
STONE_IMG = 'stone.png'
FPS = 60
MX_LIFE = 10
END_GAME_DELAY = 5000


# Keyboard Keys
# section 1.1
blue_keys = {'left': pygame.K_1, 'right': pygame.K_4, 'up': pygame.K_3, 'down': pygame.K_2}
red_keys = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}

# Create objects
def create_game_objects() -> Tuple[Spaceship, Spaceship, Window]:
    '''
    Description:
    -------------
        create the basic objects for the game
        1) Two spaceships
        2) Window

    Parameters:
    -----------
        None
    
    Return:
    --------
        Tuple of the basic objects for the game
        e.g. (blue_spaceship, red_spaceship, window) 
    '''
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, BG_IMG, FPS)
    blue_spaceship = Spaceship(75, window.height//2 -55 , SPACESHIP_WIDTH, SPACESHIP_HEIGHT,
                                BLUE_SPACESHIP_IMG, 90, blue_keys, MX_LIFE, MAX_BULLET, 1, 'blue')
    red_spaceship = Spaceship(window.width-100, window.height//2 -55, SPACESHIP_WIDTH,
                            SPACESHIP_HEIGHT, RED_SPACESHIP_IMG, 270, red_keys, MX_LIFE, MAX_BULLET, 1, 'red')                
    return blue_spaceship, red_spaceship, window

# Listen to the game event
def listen_events(blue_spaceship: Spaceship, red_spaceship: Spaceship, window: Window):
    '''
    Description:
    -------------
        listen to game events 

    Parameters:
    -----------
        blue_spaceship: Spaceship object in the left side
        red_spaceship: Spaceship object in the right side
        window: Window object
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                return False
            if event.key == pygame.K_q: #section 1.1
                bullet = Bullet(BULLET_WIDTH, BULLET_HEIGHT, blue_spaceship, BLUE_BULLET_IMG, OBJECTS_STEP, 1)
                blue_spaceship.shoot(bullet)
            if event.key == pygame.K_RCTRL:
                bullet = Bullet(BULLET_WIDTH, BULLET_HEIGHT, red_spaceship, RED_BULLET_IMG, OBJECTS_STEP, -1)
                red_spaceship.shoot(bullet)
            if event.key == pygame.K_RSHIFT: # section 1.9
                big_bullet = BigBullet(BULLET_WIDTH*2, BULLET_HEIGHT*2, red_spaceship, RED_BULLET_IMG, OBJECTS_STEP, -1)
                red_spaceship.shoot(big_bullet)
            if event.key == pygame.K_LSHIFT: # section 1.9
                big_bullet = BigBullet(BULLET_WIDTH*2, BULLET_HEIGHT*2, blue_spaceship, BLUE_BULLET_IMG, OBJECTS_STEP, 1)
                blue_spaceship.shoot(big_bullet)
            if event.key == pygame.K_SPACE: # section 1.10
                stone = Stone(random.choice([0,window.width-50]), random.randint(0, window.height-50), 50, 50, STONE_IMG, OBJECTS_STEP)
                STONES.append(stone)
            if event.key == pygame.K_TAB: # section 1.11 bonus
                pass
            if event.key == pygame.K_KP_ENTER:
                restart_game()


def end_game(spaceship1: Spaceship, spaceship2: Spaceship, window: Window) -> bool:
    '''
    Description:
    -------------
        end the game when one of the spaceships explode

    Parameters:
    -----------
        spaceship1: Spaceship object 
        spaceship2: Spaceship object
        window: Window object
    Return:
    -------
        write end game messege on screen
        bool value represent if the game ends or not
    '''
    SIZE = 40
    if spaceship1.explode():
        window.write_to_window(f'Game over - Winner is {str(spaceship2)}', SIZE,) # section 1.4
        return True
    elif spaceship2.explode():
        window.write_to_window(f'Game over - Winner is {str(spaceship1)}', SIZE) # section 1.4
        return True
    else:
        return False

def restart_game() -> None:
    '''
    Description:
    -------------
        restart the game after delay of 5000 miliseconds
    '''
    pygame.time.delay(END_GAME_DELAY)
    main()

def main() -> None:
    blue_spaceship, red_spaceship, window = create_game_objects()
    window.create_title('SpaceShip Game')
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(window.fps)
        response = listen_events(blue_spaceship, red_spaceship, window)
        if response is False:
            run = False
        if end_game(red_spaceship, blue_spaceship, window): # section 1.4
            restart_game() # section 1.4

        blue_spaceship.move(SPACESHIP_STEP, window)
        red_spaceship.move(SPACESHIP_STEP, window)
        window.handle_objects_movement(red_spaceship.stack, blue_spaceship.stack, STONES)
        window.handle_objects_events(blue_spaceship, red_spaceship, STONES)
        window.draw_window([red_spaceship, blue_spaceship], STONES)

if __name__ == "__main__":
    main()
