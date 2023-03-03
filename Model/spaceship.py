import pygame
import os
from Model.objects import Bullet, BigBullet
from typing import Dict

# TODO fix the stack property

class Spaceship(pygame.Rect):

    def __init__(self, x: int, y: int, width: int, height: int, image_file: str,
                  imageRotate: int, keys: Dict[str, int], life: int, max_bullets: int,
                    max_big_bullets: int, color: str, score_board_side) -> None:

        super().__init__(x, y, width, height)
        self._direction = imageRotate
        self._image_file = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', image_file)), (self.height, self.width)), imageRotate)
        self._keys = keys
        self._life = life
        self._max_bullets = max_bullets
        self._stack = []
        self._color = color
        self._max_big_bullets = max_big_bullets
        self._score_board_side = score_board_side 
    
    def __str__(self) -> str:
        return f'{self._color} spaceship'

    @property
    def score_board_side(self):
        return self._score_board_side
    
    @score_board_side.setter
    def score_board_side(self, new_side):
        if type(new_side) is not str:
            raise Exception('side property must be str')
        else:
            self._score_board_side = new_side

    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, new_direction):
        if type(new_direction) is not int:
            raise Exception('direction property must be int')
        else:
            self._direction = new_direction

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, new_color):
        if new_color not in ['red', 'blue']:
            raise Exception('color property must be (red or blue)')
        else:
            self._color = new_color
    
    @property
    def stack(self):
        return self._stack
    
    @stack.setter
    def stack(self, bullet):
        if type(bullet) in [Bullet, BigBullet]:
            self._stack.append(bullet) 
        else:
            raise Exception('Spaceship can shoot bullet type objects only')


    @property
    def image_file(self):
        return self._image_file
    
    @image_file.setter
    def image_file(self, new_image):
        if 'png' not in new_image:
            raise Exception('image must be in png format')
        else:
            self._image_file = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', new_image)), (self.height, self.width)), self.direction)

    @property
    def keys(self):
        return self._keys
    
    @keys.setter
    def keys(self, new_keys):
        expected_keys = ['left', 'right', 'up', 'down', 'shoot', 'shoot_big']
        if type(new_keys) is not dict or sorted(expected_keys) != sorted([*new_keys]) :
            raise Exception('The new keys must be in dict when keys are (left, right, up, down, shoot, shoot_big)')
        else:
            self._keys = new_keys
    
    @property
    def life(self):
        return self._life
    
    @life.setter
    def life(self, new_life):
        if type(new_life) is not int:
            raise Exception('Life property must be int')
        elif new_life < 0:
            raise Exception('Life must be positive')
        else:
            self._life = new_life

    @property
    def max_bullets(self):
        return self._max_bullets
    
    @max_bullets.setter
    def max_bullets(self, new_max_bullets):
        if type(new_max_bullets) is not int:
            raise Exception('Max Bullets property must be int')
        elif new_max_bullets < 0:
            raise Exception('Max Bullets must be positive')
        else:
            self._max_bullets = new_max_bullets

    @property
    def max_big_bullets(self):
        return self._max_big_bullets
    
    @max_big_bullets.setter
    def max_big_bullets(self, new_max_big_bullets):
        if type(new_max_big_bullets) is not int:
            raise Exception('Max Big Bullets property must be int')
        elif new_max_big_bullets < 0:
            raise Exception('Max Big Bullets must be positive')
        else:
            self._max_big_bullets = new_max_big_bullets

    def move(self, STEP, window):
        '''
        Description:
        -------------
            move the spaceship on the window by the steps
            the keys are provide when init the spaceship (keys)

        Parameters:
        -----------
            STEP: int
                the pace the spaceship is move by
            window: Window object
                the surface the spaceship moving in
        '''
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[self.keys['left']] and not window.check_borders(self, 'left') and not window.check_borders(self, 'mid_left'):
            self.x -= STEP
        if keys_pressed[self.keys['right']] and not window.check_borders(self, 'right') and not window.check_borders(self, 'mid_right'):
            self.x += STEP
        if keys_pressed[self.keys['up']] and not window.check_borders(self, 'up'):
            self.y -= STEP
        if keys_pressed[self.keys['down']] and not window.check_borders(self, 'down'):
            self.y += STEP
    
    def blit_spachship(self, window) -> None:
        '''
        Description:
        -------------
            Blit the spaceship into the screen

        Parameters:
        -----------
            window: Window object
            the surface the spaceship is blit into
        '''
        window.blit(self.image_file, (self.x, self.y))
    
    def shoot(self, bullet) -> None:
        '''
        Description:
        -------------
            spaceship shoot the bullet when the stack is not full

        Parameters:
        -----------
            bullet: Bullet/BigBullet
                object that been shooting by the spaceship
        '''
        if len(self.stack) < self.max_bullets:
            if type(bullet) is BigBullet and self.max_big_bullets == 0: # section 1.9
                print('Special bullet already been shooted')
            elif type(bullet) is BigBullet:
                self.max_big_bullets-=1 
                self.stack.append(bullet)
                shoot = pygame.mixer.Sound('Assets\Grenade+1.mp3')
                shoot.play(fade_ms= 1000)
            else:
                self.stack.append(bullet)
                shoot = pygame.mixer.Sound('Assets\Gun+Silencer.mp3')
                shoot.play(fade_ms= 1000)

        else:
            print('The stack is full')

    def hit(self, bullet) -> None:
        '''
        Description:
        -------------
            remove bullet from spaceship stack when hit enemy

        Parameters:
        -----------
            bullet: Bullet or BigBullet
                the bullet to remove from stack
        '''
        self.stack.remove(bullet)
    
    def miss_shoot(self, bullet) -> None:
        '''
        Description:
        -------------
            remove bullet from spaceship stack when cross window borders

        Parameters:
        -----------
            bullet: Bullet or BigBullet
                the bullet to remove from stack
        '''
        self.stack.remove(bullet)

    def got_hit(self, object) -> None:
        '''
        Description:
        -------------
            alerts when spaceship is hitten by enemy and reduce life by object power

        Parameters:
        -----------
            object: Bullet/BigBullet or Stone
                the object that hit the spaceship
        '''
        self.life -= object.power

    def explode(self) -> bool:
        '''
        Description:
        -------------
            Alert for explodition of the spaceship 

        Parameters:
        -----------
            None
        
        Return:
        --------
            bool value represent if the spaceship explode
        '''
        if self.life is 0:
            return True
        return False
            



