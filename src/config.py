import pygame
from enum import Enum
from background import CollisionSprite
import random


# info = pygame.display.get_window_size()
# ScreenWidth = info[0]
# ScreenHeight = info[1]
# print(ScreenWidth, ScreenHeight)

class FilesPath(Enum):
    """
    An enumeration defining file paths for game assets.

    Attributes:
        EXPLOSION1 (list): File paths for explosion sprite images.
        BACKGROUND (str): File path for the background image.
        ANDROMALUIS (str): File path for the Andromalius enemy image.
        SLIME (str): File path for the Slime enemy image.
        ALIENBAT (str): File path for the Alien Bat enemy image.
    """
    EXPLOSION1 = [f"assets\\images\\explosions\\explosion1\\Explosion_{i}.png" for i in range(1, 10)]
    BACKGROUND = "assets\\background_files\\map009.png"
    ANDROMALUIS = "assets\\images\\enemies\\andromaluis\\andromalius.png"
    SLIME = "assets\\images\\enemies\\Slime\\slime_idle.png"
    ALIENBAT = "assets\\images\\enemies\\alien_bat\\alien_bat.png"
    GOBLIN = "assets\\images\\enemies\\goblins\\goblinsword.png"
    CYBORGIDLE = "assets\\images\\Player\\cyborg\\Idle.png"
    CYBORGWALK = "assets\\images\Player\cyborg\\Walk.png"
    CYBORGWALKUP = "assets\\images\\Player\\cyborg\\WalkUp.png"
    CYBORGWALKDOWN = "assets\\images\\Player\cyborg\\WalkDown.png"
    BLADEMASTERIDLE = "assets\\images\\Player\\blademaster\\Idle.png"
    BLADEMASTERWALK = "assets\\images\\Player\\blademaster\\Walk.png"
    BLADEMASTERWALKUP = "assets\\images\\Player\\blademaster\\WalkUp.png"
    BLADEMASTERWALKDOWN = "assets\\images\\Player\\blademaster\\WalkDown.png"
    BERSERKERIDLE = "assets\\images\\Player\\berserker\\Idle.png"
    BERSERKERWALK = "assets\\images\\Player\\berserker\\Walk.png"
    BERSERKERWALKUP = "assets\\images\\Player\\berserker\\WalkUp.png"
    BERSERKERWALKDOWN = "assets\\images\\Player\\berserker\\WalkDown.png"




class RectColiddersMap(Enum):
    """
    An enumeration defining collision boundaries for the game map.

    Attributes:
        MAPBOUNDS (pygame.Rect): A rectangle defining the map's boundaries.
    """
    MAPBOUNDS = pygame.Rect(1020, 710, 6460, 3480)


rects_data = [((1660, 1080), (200, 130)), ((1750, 974), (170, 150)), ((1810, 830), (100, 100)), ((1700, 890), (30, 30)), ((1713, 855), (25, 25)),((1722, 833), (20,20)) ,((1830, 775), (25, 25)), 
              ((1823, 742), (20,20)), #starship_rects
              ((6585, 1317), (25, 25)), ((6633, 1225), (25, 25)), ((6716, 1148), (25, 25)), ((6796, 1114), (25, 25)), ((6975, 1050), (25, 25)), ((6874, 1085), (25, 25)), ((7081, 1075), (25, 25)),
              ((7161, 1101), (25, 25)), ((7236, 1172), (25, 25)), ((7251, 1293), (25, 25)), ((7240, 1394), (25, 25)), ((7211, 1471), (25, 25)), ((7156, 1531), (25, 25)), ((7083, 1582), (25, 25)),
              ((7252, 1279), (30, 30)), ((7033, 1036), (20, 20)), ((6887, 1053), (20, 20)), ((7095, 1064), (20, 20)), ((6552, 1400), (18, 18)), ((7164, 1096), (20, 20)), ((7246, 1163), (20, 20)),
                ((7078, 1068), (88, 132)), ((7189, 1115), (135, 20)), #cave_rects
                ((2233,3771), (390,452)), ((2169,3516), (302,175)), ((2009,3433), (161,190)), ((1842,3331), (208,153)), ((1657,3226), (339,161)), ((1384,3083), (209,255)), ((1517,3118), (138,248)),
                ((1416,3500), (211,95)), ((1350,3297), (75,108)), ((1340,3431), (73,99)), ((1450,3532), (239,129)), ((1520,3650), (97,87)), ((1670,3720), (170,97)), ((1850,3800), (162,92)), ((1973,3850), (205,70))
]


def random_pos():
    """
    Generates a random position within defined bounds.

    Returns:
        tuple: A tuple (x, y) representing a random position.
    """
    x_pos = random.randint(1100, 6400)
    y_pos = random.randint(720, 3400)
    return x_pos, y_pos


def collisionSpritesGenerator():
    """
    Creates and returns a list of collision sprites based on predefined data.

    Returns:
        list: A list of CollisionSprite objects created from `rects_data`.
    """
    colliders = []
    for each in rects_data:
        rect = CollisionSprite(each[0], each[1])
        colliders.append(rect)
    
    return colliders


def load_explosion_images():
    """
    Loads and returns explosion images as surfaces.

    Returns:
        list: A list of pygame.Surface objects representing explosion frames.
    """
    sprite_sheet = [pygame.image.load(image) for image in FilesPath.EXPLOSION1.value]
    return sprite_sheet


def load_enemies_images():
    """
    Placeholder for loading enemy images.

    """
    pygame.init()
    subset = list(FilesPath)[2:6]
    image_dict = {item.name: pygame.image.load(item.value) for item in subset}
    return image_dict


def load_player_images():

    pygame.init()
    subset = list(FilesPath)[6:]
    cyborg_dict = {
        item.name.removeprefix("CYBORG"): pygame.image.load(item.value)
        for item in subset
        if item.name.startswith("CYBORG")
    }

    blademaster_dict = {
        item.name.removeprefix("BLADEMASTER"): pygame.image.load(item.value)
        for item in subset
        if item.name.startswith("BLADEMASTER")
    }

    berserker_dict = {
        item.name.removeprefix("BERSERKER"): pygame.image.load(item.value)
        for item in subset
        if item.name.startswith("BERSERKER")
    }


    return [cyborg_dict, blademaster_dict, berserker_dict]
