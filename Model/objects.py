import pygame
import os

class Bullet(pygame.Rect):

    def __init__(self, width: int, height: int, spaceship, image_file: str, step: int, direction: int, power=1):
        self._width = width
        self._height = height
        self._power = power
        self._step = step
        self._direction = direction
        super().__init__(spaceship.x + spaceship.width, spaceship.y + spaceship.height / 2 - self._height, self._width, self._height)
        self._image_file = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', image_file)), (self.height, self.width)), 0)

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, new_width):
        if type(new_width) is not int:
            raise Exception('Width must be int')
        else:
            self._width = new_width

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, new_height):
        if type(new_height) is not int:
            raise Exception('Height must be int')
        else:
            self._height = new_height
    
    @property
    def power(self):
        return self._power
    
    @power.setter
    def power(self, new_power):
        if type(new_power) is not int:
            raise Exception('Power must be int')
        else:
            self._power = new_power

    @property
    def step(self):
        return self._step
    
    @step.setter
    def step(self, new_step):
        if type(new_step) is not int:
            raise Exception('Step must be int')
        else:
            self._step = new_step

    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, new_direction):
        if new_direction not in [1,-1] :
            raise Exception('Direction must be 1 or -1')
        else:
            self._direction = new_direction

    @property
    def image_file(self):
        return self._image_file
    
    @image_file.setter
    def image_file(self, new_image):
        if 'png' not in new_image:
            raise Exception('image must be in png format')
        else:
            self._image_file = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', new_image)), (self.height, self.width)), 0)
    
    def blit_bullet(self, window) -> None:
        window.blit(self._image_file, (self.x, self.y))
    
    def move(self, step: int) -> None:
        self.x += (self._direction*step)


class BigBullet(Bullet): # section 1.9

    def __init__(self, width: int, height: int, spaceship, image_file: str, step: int, direction: int):
        super().__init__(width, height, spaceship, image_file, step, direction, power=2)


class Stone(pygame.Rect): # section 1.10

    def __init__(self, x: int, y: int, width: int, height: int, image_file: str, step: int, power=1) -> None:
        self._height = height
        self._width = width
        self._power = power
        self._step = step
        if x == 0:
            self._direction = 1
        else:
            self._direction = -1
        super().__init__(x, y, width, height)
        self._image_file = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', image_file)), (self.height, self.width)), 0)

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, new_width):
        if type(new_width) is not int:
            raise Exception('Width must be int')
        else:
            self._color = new_width

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, new_height):
        if type(new_height) is not int:
            raise Exception('Height must be int')
        else:
            self._color = new_height

    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, new_direction):
        if new_direction not in [1, -1]:
            raise Exception('Direction must be 1 or -1')
        else:
            self._direction = new_direction

    @property
    def step(self):
        return self._step
    
    @step.setter
    def step(self, new_step):
        if type(new_step) is not int:
            raise Exception('Step must be int')
        else:
            self._step = new_step

    @property
    def image_file(self):
        return self._image_file
    
    @image_file.setter
    def image_file(self, new_image):
        if 'png' not in new_image:
            raise Exception('image must be in png format')
        else:
            self._image_file = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', new_image)), (self.height, self.width)), 0)

    @property
    def power(self):
        return self._power
    
    @power.setter
    def power(self, new_power):
        if type(new_power) is not int:
            raise Exception('Power must be int')
        else:
            self._power = new_power

    def blit_stone(self, window) -> None:
        window.blit(self.image_file, (self.x, self.y))
    
    def move(self, step: int) -> None:
        self.x += (self._direction*step)
    
    def explode(self, object_stack, sound=True) -> None:
        if sound:
            explode = pygame.mixer.Sound('Assets\Grenade+1.mp3')
            explode.play(fade_ms= 1000)
        object_stack.remove(self)


    
        
