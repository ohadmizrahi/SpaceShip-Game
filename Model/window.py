import pygame
import os
from typing import Tuple

class Window:

    COLLIDE = pygame.USEREVENT + 1

    def __init__(self, width: int, height: int, bg_img: str, fps: int):
        self._width = width
        self._height = height
        self._background = pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', bg_img)),
             (self.width, self.height))
        self._screen = pygame.display.set_mode((self.width, self.height))
        self._fps = fps
        self._borders = {'left': 0, 'right': self.width, 'up': 0, 'down': self.height, 'mid_left': self.width/2, 'mid_right': self.width/2}
        self._mid_border = pygame.Rect(self.width / 2 - 5, 0, 30, self.height)

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, new_size):
        if type(new_size) is not tuple:
            raise Exception('size for screen must be tuple of (width, height)')
        else:
            self._screen = pygame.display.set_mode((new_size[0], new_size[1]))

    @property
    def borders(self):
        return self._borders

    @borders.setter
    def borders(self, new_borders):
        if type(new_borders) is not dict:
            raise Exception('borders property must be dict of (direction: value)')
        else:
            self._borders = new_borders

    @property
    def mid_border(self):
        return self._mid_border

    @borders.setter
    def mid_border(self, new_mid_border):
        if type(new_mid_border) is not pygame.Rect:
            raise Exception('Mid border property must be pygame.Rect')
        else:
            self._mid_border = new_mid_border

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, new_width):
        if type(new_width) is not int:
            raise Exception('width property must be int')
        else:
            self._width = new_width

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, new_height):
        if type(new_height) is not int:
            raise Exception('height property must be int')
        else:
            self._height = new_height

    @property
    def background(self):
        return self._background
    
    @background.setter
    def background(self, new_bg_img):
        self._background = pygame.transform.scale(pygame.image.load(
        os.path.join('Assets', new_bg_img)),
            (self.width, self.height))

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, new_fps):
        if type(new_fps) is not int:
            raise Exception('fpx property must be int')
        else:
            self._fps = new_fps


    def create_title(self, title: str) -> None:
        pygame.display.set_caption(title)
    
    def write_to_window(self, messege: str, size: int, location: Tuple[int, int], font='comicsans') -> None:
        FONT = pygame.font.SysFont(font, size)
        text = FONT.render(messege, 1, 'white')
        self.screen.blit(text, location)
        pygame.display.update()
    
    def new_score_board(self, spaceships, font: str, size: int, color: tuple) -> None:
        FONT = pygame.font.SysFont(font, size)
        right = FONT.render("LIFE " + str(spaceships[0].life), 1, color)
        self.screen.blit(right,(self.width - right.get_width() - 10, 10))
        left = FONT.render("LIFE " + str(spaceships[1].life), 1, color)
        self.screen.blit(left, (10, 10))

    def check_borders(self, entity, border: str) -> bool:
        cross_border = False
        if border is 'left' and entity.x < self.borders[border]:
            cross_border = True
        if border is 'right' and entity.x > self.borders[border] - entity.width:
            cross_border = True
        if border is 'up' and entity.y < self.borders[border]:
            cross_border = True
        if border is 'down' and entity.y > self.borders[border] - entity.height:
            cross_border = True
        if border is 'mid_left' and entity.x == self.borders[border] + (entity.width-30):
            cross_border = True
        if border is 'mid_right' and entity.x == self.borders[border] - entity.width:
            cross_border = True
        
        return cross_border

    def check_collide(self, object1, object2) -> bool:
        if object1.colliderect(object2):
            pygame.event.post(pygame.event.Event(__class__.COLLIDE))
            return True
        else:
            return False
    
    def handle_objects_movement(self, *args) -> None:
        for objects in args:
            if type(objects) is not list:
                raise Exception('Window can move objects collect in a list only')
            for object in objects:
                object.move(object.step)

    
    def handle_objects_events(self, blue_spaceship, red_spaceship, stones: list) -> None:
        for stone in stones: # section 1.10
            if self.check_borders(stone, 'left') or self.check_borders(stone, 'right'):
                stone.explode(stones, sound=False)
            if self.check_collide(blue_spaceship, stone):
                blue_spaceship.got_hit(stone)
                stone.explode(stones, sound=True)
            if self.check_collide(red_spaceship, stone):
                red_spaceship.got_hit(stone)
                stone.explode(stones, sound=True)

        for blue_bullet in blue_spaceship.stack:
            if self.check_borders(blue_bullet, 'right'):
                blue_spaceship.miss_shoot(blue_bullet)
            if self.check_collide(blue_bullet, red_spaceship):
                blue_spaceship.hit(blue_bullet)
                red_spaceship.got_hit(blue_bullet)

        for red_bullet in red_spaceship.stack:
            if self.check_borders(red_bullet, 'left'):
                red_spaceship.miss_shoot(red_bullet)
            if self.check_collide(red_bullet, blue_spaceship):
                red_spaceship.hit(red_bullet)
                blue_spaceship.got_hit(red_bullet)

            for blue_bullet in blue_spaceship.stack:
                if self.check_collide(red_bullet, blue_bullet): # section 1.7
                    red_spaceship.miss_shoot(red_bullet)
                    blue_spaceship.miss_shoot(blue_bullet)


    def draw_window(self, spaceships: list, stacks: dict, stones: list) -> None:
        self.screen.blit(self.background, (0,0))
        pygame.draw.rect(self.screen, 'black', self._mid_border)
        for spaceship in spaceships:
            spaceship.blitSpachship(self.screen)
        self.new_score_board(spaceships, 'comicsans', 40, (255, 255, 255))
        all_bullets = stacks['red_stack'] + stacks['blue_stack']
        for bullet in all_bullets:
            bullet.blitBullet(self.screen)
        for stone in stones:
            stone.blitStone(self.screen)
        self.write_to_window('Ohad Mizrahi|Or Solomon|Bar Siboni', 18, (300, self.height-40)) # section 1.5
        pygame.display.update()

