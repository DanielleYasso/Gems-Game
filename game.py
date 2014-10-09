import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import random

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 5
GAME_HEIGHT = 5

#### Put class definitions here ####
class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, zelda):
        if self.IMAGE != "OrangeGem":
            zelda.inventory.append(self)
            GAME_BOARD.draw_msg("You rich bitch! You so fancy. You have %d status symbols" % len(zelda.inventory))

    def __init__(self, gem_color="BlueGem"):
        self.IMAGE = gem_color

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True    

class Character(GameElement):
    IMAGE = "Princess"
    start_position = (2,2)
    # inventory = []

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

    def update_pos(self, next_x, next_y):
        self.board.del_el(self.x, self.y)
        self.board.set_el(next_x, next_y, self)

    def keyboard_handler(self, symbol, modifier):
        direction = None
        direction_message = "I'm a Princess!"

        if symbol == key.UP:
            direction_message = "Upsee dwaynzee"
            direction = "up"
        elif symbol == key.DOWN:
            direction_message = "we goin down we yellin timberrrr"
            direction = "down"
        elif symbol == key.LEFT:
            direction_message = "to the left to the left"
            direction = "left"
        elif symbol == key.RIGHT:
            direction_message = "you spin me right round baby rigghhhht round"
            direction = "right"
        elif symbol == key.SPACE:
            self.board.erase_msg()

        self.board.draw_msg('%s says: "%s"' % (self.IMAGE, direction_message))

        if direction:
            next_location = self.next_pos(direction)

            if next_location:
                next_x, next_y = next_location
                try:
                    existing_el = self.board.get_el(next_x, next_y)
                    if existing_el:
                        existing_el.interact(self)

                    if existing_el and existing_el.SOLID:
                        self.board.draw_msg("You got rock blocked")
                    if existing_el and existing_el.IMAGE == "OrangeGem":
                        next_x, next_y = self.start_position
                        self.update_pos(next_x, next_y)
                        GAME_BOARD.draw_msg("whoever said orange is the new pink was seriously disturbed! Back to start")
                    elif existing_el is None or not existing_el.SOLID:
                        self.update_pos(next_x, next_y)
                except IndexError:
                    self.board.draw_msg("Where do you think you're going fool?")


    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []





####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    
    dwayne_johnson_positions = [
        (2,1),
        (1,2),
        (3,2),
        (2,3)
        ]

    dwayne_johnsons = []

    for pos in dwayne_johnson_positions:
        dwayne = Rock()
        GAME_BOARD.register(dwayne)
        GAME_BOARD.set_el(pos[0], pos[1], dwayne)
        dwayne_johnsons.append(dwayne)

    random.choice(dwayne_johnsons).SOLID = False

    for dwayne in dwayne_johnsons:
        print dwayne

    zelda = Character()
    GAME_BOARD.register(zelda)
    GAME_BOARD.set_el(2,2, zelda)
    print zelda

    blue_gem = Gem()
    GAME_BOARD.register(blue_gem)
    GAME_BOARD.set_el(3, 1, blue_gem)

    green_gem = Gem("GreenGem")
    GAME_BOARD.register(green_gem)
    GAME_BOARD.set_el(4,4, green_gem)

    orange_gem = Gem("OrangeGem")
    GAME_BOARD.register(orange_gem)
    GAME_BOARD.set_el(0,0,orange_gem)