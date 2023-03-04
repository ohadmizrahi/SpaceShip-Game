import pygame
import os

class Window:

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
        '''
        Description:
        -------------
            create title for the game window

        Parameters:
        -----------
            title: str
                the text to show in the title
        '''
        pygame.display.set_caption(title)
    
    def write_to_window(self, messege: str, size: int, font='comicsans', location='middle') -> None:
        '''
        Description:
        -------------
            method to write text into the game window

        Parameters:
        -----------
            messege: str
                text messege to display
            size: int
                the size of the text
            font: default - 'comicsans'
            location: default - 'middle'
                where to display the text (y axis)
                option: lower, middle, upper
        '''
        FONT = pygame.font.SysFont(font, size)
        text = FONT.render(messege, 1, 'white')
        if location == 'middle':
            location = (self.width//2 - text.get_width()//2, self.height//2 - text.get_height()//2)
        if location == 'lower':
            location = (self.width//2 - text.get_width()//2, self.height - text.get_height())
        if location == 'upper':
            location = (self.width//2 - text.get_width()//2, 10)
        self.screen.blit(text, location)
    
    def new_score_board(self, spaceships: list, font: str, size: int, color: tuple) -> None:
        '''
        Description:
        -------------
            create new scoreboard

        Parameters:
        -----------
            spaceships: list of Spaceship objects
            font: str
                the font to write with
            size: int
                size of the text
            color: tuple
                RGB color 
        '''
        FONT = pygame.font.SysFont(font, size)
        red = FONT.render("RED LIFE " + str(spaceships[0].life), 1, color)
        blue = FONT.render("BLUE LIFE " + str(spaceships[1].life), 1, color)
        red_loc = (self.width - red.get_width() - 30, 10)
        blue_loc = (10,10)
        if spaceships[0].score_board_side == 'right':
            red_loc = (self.width - red.get_width() - 30, 10)
            blue_loc = (10,10)
        else:
            blue_loc = (self.width - red.get_width() - 30, 10)
            red_loc = (10,10)

        self.screen.blit(red,red_loc)
        self.screen.blit(blue, blue_loc)


    def check_borders(self, entity, border: str) -> bool:
        '''
        Description:
        -------------
            check if any object cross the window borders

        Parameters:
        -----------
            entity: ADT object of the game
                the checked object
            border: str
                the checked border crossed
        
        Return:
        --------
            bool value represent if cross border occur
        '''
        cross_border = False
        if border == 'left' and entity.x < self.borders[border]:
            cross_border = True
        if border == 'right' and entity.x > self.borders[border] - entity.width:
            cross_border = True
        if border == 'up' and entity.y < self.borders[border]:
            cross_border = True
        if border == 'down' and entity.y > self.borders[border] - entity.height:
            cross_border = True
        if border == 'mid_left' and entity.x == self.borders[border] + (entity.width-30):
            cross_border = True
        if border == 'mid_right' and entity.x == self.borders[border] - entity.width:
            cross_border = True
        
        return cross_border

    def check_collide(self, object1, object2) -> bool:
        '''
        Description:
        -------------
            check collide of two ADT objects

        Parameters:
        -----------
            object1: ADT object of the game
            object2: ADT object of the game
        
        Return:
        --------
            bool value represent if collide occur
        '''
        if object1.colliderect(object2):
            return True
        else:
            return False
    
    def handle_objects_movement(self, *args) -> None:
        '''
        Description:
        -------------
            move the all the objects given on the game window

        Parameters:
        -----------
            *args:
                every list of objects need to be moved on the window 
        '''
        for objects in args:
            if type(objects) is not list:
                raise Exception('Window can move objects collect in a list only')
            for object in objects:
                object.move(object.step)

    
    def handle_objects_events(self, blue_spaceship, red_spaceship, stones: list) -> None:
        '''
        Description:
        -------------
            handle the objects collide, cross borders, hit, miss and got hit

        Parameters:
        -----------
            blue_spaceship: Spaceship object in left side
            red_spaceship: Spaceship object in right side
            stones: list
                the list of stones in the window
        '''
        for stone in stones: # section 1.10
            if self.check_borders(stone, 'left') or self.check_borders(stone, 'right'):
                stone.explode(stones, sound=False)
            if self.check_collide(blue_spaceship, stone):
                blue_spaceship.got_hit(stone)
                stone.explode(stones, sound=True)
            if self.check_collide(red_spaceship, stone):
                red_spaceship.got_hit(stone)
                stone.explode(stones, sound=True)
            stone.check_got_hit(blue_spaceship, self, stones)
            stone.check_got_hit(red_spaceship, self, stones)

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


    def draw_window(self, spaceships: list, stones: list) -> None:
        '''
        Description:
        -------------
            draw the window objects current state and update the surface

        Parameters:
        -----------
            spaceships: list of Spaceship objects
            stones: list of all Stones objects
        '''
        self.screen.blit(self.background, (0,0))
        pygame.draw.rect(self.screen, 'black', self._mid_border)
        for spaceship in spaceships:
            spaceship.blit_spachship(self.screen)
            for bullet in spaceship.stack:
                bullet.blit_bullet(self.screen)
        self.new_score_board(spaceships, 'comicsans', 40, (255, 255, 255))
        for stone in stones:
            stone.blit_stone(self.screen)
        self.write_to_window('Ohad Mizrahi|Or Solomon|Bar Siboni', 18, location='lower') # section 1.5
        self.write_to_window('Press Enter to Restart',18, location='upper')
        pygame.display.update()
    

