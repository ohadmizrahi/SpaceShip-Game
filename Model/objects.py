import pygame
import os

# TODO create getter setter to direction in Stone class 

class Bullet(pygame.Rect):

    def __init__(self, width, height, spaceship, image_file):
        self._width = width
        self._height = height
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
    def image_file(self):
        return self._image_file
    
    @image_file.setter
    def image_file(self, new_image):
        if 'png' not in new_image:
            raise Exception('image must be in png format')
        else:
            self._image_file = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', new_image)), (self.height, self.width)), 0)
    
    def blitBullet(self, window):
        window.blit(self._image_file, (self.x, self.y))
    
    def move(self, direction: int, step: int):
        self.x += (direction*step)

class BigBullet(Bullet): # section 1.9
    def __init__(self, width, height, spaceship, image_file):
        super().__init__(width, height, spaceship, image_file)


class Stone(pygame.Rect): # section 1.10

    def __init__(self, x, y, width, height, image_file) -> None:
        self._height = height
        self._width = width
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
    def image_file(self):
        return self._image_file
    
    @image_file.setter
    def image_file(self, new_image):
        if 'png' not in new_image:
            raise Exception('image must be in png format')
        else:
            self._image_file = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', new_image)), (self.height, self.width)), 0)

    def blitStone(self, window):
        window.blit(self.image_file, (self.x, self.y))
    
    def move(self, step: int):
        self.x += (self._direction*step)


    
        
