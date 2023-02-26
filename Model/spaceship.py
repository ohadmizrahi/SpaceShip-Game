import pygame
import os
from Model.objects import Bullet, BigBullet

# TODO fix the stack property

class Spaceship(pygame.Rect):

    def __init__(self, x, y, width, height, image_file, imageRotate, keys, life, max_bullets, max_big_bullets, color):

        super().__init__(x, y, width, height)
        self._direction = imageRotate
        self._image_file = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', image_file)), (self.height, self.width)), imageRotate)
        self._left = keys['left']
        self._right = keys['right']
        self._up = keys['up']
        self._down = keys['down']
        self._life = life
        self.max_bullets = max_bullets
        self._stack = []
        self._color = color
        self._max_big_bullets = max_big_bullets
    
    def __str__(self) -> str:
        return f'{self._color} spaceship'
    
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
    def left(self):
        return self._left

    @left.setter
    def left(self, new_keys):
        expected_keys = ['left', 'right', 'up', 'down']
        if type(new_keys) is not dict or sorted(expected_keys) != sorted([*new_keys]) :
            raise Exception('The new keys must be in dict when keys are (left, right, up, down)')
        else:
            self._left = new_keys['left']

    @property
    def right(self):
        return self._right
    
    @right.setter
    def right(self, new_keys):
        expected_keys = ['left', 'right', 'up', 'down']
        if type(new_keys) is not dict or sorted(expected_keys) != sorted([*new_keys]) :
            raise Exception('The new keys must be in dict when keys are (left, right, up, down)')
        else:
            self._right = new_keys['right']

    @property
    def up(self):
        return self._up
    
    @up.setter
    def up(self, new_keys):
        expected_keys = ['left', 'right', 'up', 'down']
        if type(new_keys) is not dict or sorted(expected_keys) != sorted([*new_keys]) :
            raise Exception('The new keys must be in dict when keys are (left, right, up, down)')
        else:
            self._up = new_keys['up']

    @property
    def down(self):
        return self._down
    
    @down.setter
    def down(self, new_keys):
        expected_keys = ['left', 'right', 'up', 'down']
        if type(new_keys) is not dict or sorted(expected_keys) != sorted([*new_keys]) :
            raise Exception('The new keys must be in dict when keys are (left, right, up, down)')
        else:
            self._down = new_keys['down']
    
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
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[self.left] and not window.checkBorders(self, 'left') and not window.checkBorders(self, 'mid_left'):
            self.x -= STEP
        if keys_pressed[self.right] and not window.checkBorders(self, 'right') and not window.checkBorders(self, 'mid_right'):
            self.x += STEP
        if keys_pressed[self.up] and not window.checkBorders(self, 'up'):
            self.y -= STEP
        if keys_pressed[self.down] and not window.checkBorders(self, 'down'):
            self.y += STEP
    
    def blitSpachship(self, window):
        window.blit(self.image_file, (self.x, self.y))
    
    def shoot(self, bullet):
        if len(self.stack) < self.max_bullets:
            if type(bullet) is BigBullet and self._max_big_bullets is 0: # section 1.9
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
        
    def explode(self):
        if self.life is 0:
            return True
        else:
            return False
            



