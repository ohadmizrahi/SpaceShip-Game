import pygame
import os

# TODO make getter setter to mid_border

class Window:

    COLLIDE = pygame.USEREVENT + 1

    def __init__(self, width, height, bg_img, fps):
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
    def borders(self):
        return self._borders

    @borders.setter
    def borders(self, new_borders):
        if type(new_borders) is not dict:
            raise Exception('borders property must be dict of (direction: value)')
        else:
            self._borders = new_borders

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


    def createTitle(self, title):
        pygame.display.set_caption(title)
    
    def writeToWindow(self, messege, size, location, font='comicsans'):
        FONT = pygame.font.SysFont(font, size)
        text = FONT.render(messege, 1, 'white')
        self._screen.blit(text, location)
        pygame.display.update()
    
    def newScoreBoard(self, spaceships, font: str, size: int, color: tuple):
        FONT = pygame.font.SysFont(font, size)
        right = FONT.render("LIFE " + str(spaceships[0].life), 1, color)
        self._screen.blit(right,(self.width - right.get_width() - 10, 10))
        left = FONT.render("LIFE " + str(spaceships[1].life), 1, color)
        self._screen.blit(left, (10, 10))

    def checkBorders(self, entity, border) -> bool:
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

    def checkCollide(self, object1, object2) -> bool:
        if object1.colliderect(object2):
            pygame.event.post(pygame.event.Event(__class__.COLLIDE))
            return True
        else:
            return False

    def drawWindow(self, spaceships: list, stacks: dict, stones ):
        self._screen.blit(self.background, (0,0))
        pygame.draw.rect(self._screen, 'black', self._mid_border)
        for spaceship in spaceships:
            spaceship.blitSpachship(self._screen)
        self.newScoreBoard(spaceships, 'comicsans', 40, (255, 255, 255))
        all_bullets = stacks['red_stack'] + stacks['blue_stack']
        for bullet in all_bullets:
            bullet.blitBullet(self._screen)
        for stone in stones:
            stone.blitStone(self._screen)
        self.writeToWindow('Ohad Mizrahi|Or Solomon|Bar Siboni', 18, (300, self.height-40)) # section 1.5
        pygame.display.update()

