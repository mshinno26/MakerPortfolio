"""
GUI utility for Yamslam objects
yamGuiUtil.py
Max Shinno
"""

import pygame

class YamGuiUtil():
    def __init__(self):
        pass

    def loadImage(self, imageFile, scale):
        image = pygame.image.load(imageFile).convert_alpha()
        width = image.get_width()
        height = image.get_height()
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        return image

    def getMousePosition(self, surface = None):
        offset = (0, 0) if surface is None else surface.get_offset()
        posTemp = pygame.mouse.get_pos()
        pos = (posTemp[0] - offset[0], posTemp[1] - offset[1])
        return pos