
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
BULLET_STEP = 7
MAX_BULLET = 5 # section 1.6

# Keyboard Keys
blue_keys = {'left': pygame.K_a, 'right': pygame.K_d,
              'up': pygame.K_w, 'down': pygame.K_s}
red_keys = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
           'up': pygame.K_UP, 'down': pygame.K_DOWN}

# Create objects
window = Window(WIDTH, HEIGHT, 'space.png', 60)
blue_spaceship = Spaceship(75, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT,
                             'blue_spaceship.png', 90, blue_keys, 10, MAX_BULLET, 1, 'blue')
red_spaceship = Spaceship(window.width-100, 300, SPACESHIP_WIDTH,
                          SPACESHIP_HEIGHT, 'new_red_spaceship.png', 270, red_keys, 10, MAX_BULLET, 1, 'red')

def handle_objects(blue_stack, red_stack, stones):
    for stone in stones: # section 1.10
        stone.move(BULLET_STEP)
        if window.checkBorders(stone, 'left') or window.checkBorders(stone, 'right') or window.checkCollide(blue_spaceship, stone) or window.checkCollide(red_spaceship, stone):
            stones.remove(stone)
            if window.checkCollide(blue_spaceship, stone):
                blue_spaceship.life -= 1
            if window.checkCollide(red_spaceship, stone):
                red_spaceship.life -= 1
            print()
    for blue_bullet in blue_stack:
        blue_bullet.move(1, BULLET_STEP)
        if window.checkCollide(blue_bullet, red_spaceship) or window.checkBorders(blue_bullet, 'right'):
            blue_stack.remove(blue_bullet)
            if window.checkCollide(blue_bullet, red_spaceship):
                if type(blue_bullet) == BigBullet:
                    red_spaceship.life -= 2
                else:
                    red_spaceship.life -= 1
    for red_bullet in red_stack:
        red_bullet.move(-1, BULLET_STEP)
        if window.checkCollide(red_bullet, blue_spaceship) or window.checkBorders(red_bullet, 'left'):
            red_stack.remove(red_bullet)
            if window.checkCollide(red_bullet, blue_spaceship):
                if type(red_bullet) == BigBullet:
                    blue_spaceship.life -= 2
                else:
                    blue_spaceship.life -= 1
        for blue_bullet in blue_stack:
            if window.checkCollide(red_bullet, blue_bullet): # section 1.7
                red_stack.remove(red_bullet)
                blue_stack.remove(blue_bullet)
                


def end_game(spaceship1, spaceship2):
    if spaceship1.explode():
        window.writeToWindow(f'Game over - Winner is {str(spaceship2)}', 40, (250,300)) # section 1.4
        pygame.time.delay(5000)
        return True
    elif spaceship2.explode():
        window.writeToWindow(f'Game over - Winner is {str(spaceship1)}', 40, (250,300)) # section 1.4
        pygame.time.delay(5000)
        return True
    else:
        return False

def restart_game():
    pass

def main():
    window.createTitle('SpaceShip Game')
    clock = pygame.time.Clock()
    run = True
    stones = []
    while run:
        clock.tick(window.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run - False
                    pygame.quit()
                if event.key == pygame.K_LCTRL:
                    bullet = Bullet(50, 25, blue_spaceship, 'blue_bullets.png')
                    blue_spaceship.shoot(bullet)
                if event.key == pygame.K_RCTRL:
                    bullet = Bullet(50, 25, red_spaceship, 'red_bullets.png')
                    red_spaceship.shoot(bullet)
                if event.key == pygame.K_RSHIFT: # section 1.9
                    big_bullet = BigBullet(100, 50, red_spaceship, 'red_bullets.png')
                    red_spaceship.shoot(big_bullet)
                if event.key == pygame.K_LSHIFT: # section 1.9
                    big_bullet = BigBullet(100, 50, blue_spaceship, 'blue_bullets.png')
                    blue_spaceship.shoot(big_bullet)
                if event.key == pygame.K_SPACE: # section 1.10
                    stone = Stone(random.choice([0,window.width-50]), random.randint(0, window.height-50), 50, 50, 'stone.png')
                    stones.append(stone)
                if event.key == pygame.K_TAB: # section 1.11 bonus
                    pass
       
        if end_game(red_spaceship, blue_spaceship): # section 1.4
            red_spaceship.life = 10
            blue_spaceship.life = 10
            red_spaceship.max_big_bullets = 1
            blue_spaceship.max_big_bullets = 1
        
        blue_spaceship.move(SPACESHIP_STEP, window)
        red_spaceship.move(SPACESHIP_STEP, window)
        handle_objects(blue_spaceship._stack, red_spaceship._stack, stones)
        window.drawWindow([red_spaceship, blue_spaceship], {'red_stack': red_spaceship._stack, 'blue_stack': blue_spaceship._stack}, stones)

if __name__ == "__main__":
    main()
