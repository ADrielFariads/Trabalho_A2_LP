import pygame
from enum import Enum
from background import CollisionSprite

pygame.init()

# info = pygame.display.get_window_size()
# ScreenWidth = info[0]
# ScreenHeight = info[1]
# print(ScreenWidth, ScreenHeight)

class FilesPath(Enum):
    EXPLOSION1 = [f"assets\\images\\explosions\\explosion1\\Explosion_{i}.png" for i in range(1, 10)]
    BACKGROUND = "assets\\background_files\\map007.png"

class RectColiddersMap(Enum):
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




def collisionSpritesGenerator():
    colliders = []
    for each in rects_data:
        rect = CollisionSprite(each[0], each[1])
        colliders.append(rect)
    
    return colliders




def load_explosion_images():
    sprite_sheet = [pygame.image.load(image) for image in FilesPath.EXPLOSION1.value]
    return sprite_sheet

