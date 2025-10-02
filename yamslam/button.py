"""
button sprite object
button.py
Max Shinno
"""

import pygame
from yamGuiUtil import YamGuiUtil

class Button(pygame.sprite.Sprite):
    def __init__(self, isActive, folder, type, x, y, scale):
        super(Button, self).__init__()
        self._scale = scale
        self._imageFilename = self.getImageFilename(folder, type, isActive)
        self._yamGuiUtil = YamGuiUtil()
        self._image = self._yamGuiUtil.loadImage(self._imageFilename, self._scale)
        self._rect = self._image.get_rect().move(x, y)
        self._clicked = False    # to prevent hold-clicks
        self._isActive = isActive

    def draw(self, screen):
        self.isClicked(screen)
        screen.blit(self._image, self._rect)
        return self._clicked

    """
    procedure to check if button is currently clicked, and set global variable
    """
    def isClicked(self, surface = None):
        pos = self._yamGuiUtil.getMousePosition(surface)    # mouse position
        # if active, sprite is touching mouse, mouse down, and not already clicked
        if self._isActive and self._rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and not self._clicked:
            self._clicked = True
        else:
            self._clicked = False
        if pygame.mouse.get_pressed()[0] == 0:    # [0] = left mouse button, 0 = not clicked
            self._clicked = False
        return self._clicked

    def getImageFilename(self, folder, type, active):
        filename = folder + "/" + type
        if active:
            filename += ".png"
        else:
            filename += "Inactive.png"
        return filename