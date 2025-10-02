"""
dice manager and dice sprite objects
dice.py
Max Shinno
"""

import pygame
from yamGuiUtil import YamGuiUtil

class DiceManager():
    def __init__(self, surface, imageFolder):
        self._diceSelections = []
        self._diceGroup = pygame.sprite.Group()
        self._diceSurface = surface
        self._imageFolder = imageFolder

    def isDiceSelected(self):
        return len(self._diceSelections) > 0

    def getDiceSelections(self):
        return self._diceSelections

    def getDice(self):
        vals = [0]*5
        for dice in self._diceGroup:
            vals[dice.getIndex()] = dice.getVal()
        return vals

    def createDice(self, diceList, spacing):
        self._diceGroup.empty()
        self._diceSelections.clear()
        x = 0
        for i in range(len(diceList)):
            self._diceGroup.add(Dice(i, diceList[i], self._imageFolder, x, 0, 1.0))
            x += spacing

    def drawDice(self):
        action = False
        for dice in self._diceGroup:
            if dice.draw(self._diceSurface):
                if dice.isSelected():
                    self._diceSelections.append(dice.getIndex())
                else:
                    # don't need to check if already in list, because dice.draw() returns action
                    self._diceSelections.remove(dice.getIndex())
                action = True
        return action

class Dice(pygame.sprite.Sprite):
    def __init__(self, index, value, imageFolder, x, y, scale):
        super(Dice, self).__init__()
        self._index = index
        self._value = value
        self._scale = scale
        self._imageFolder = imageFolder
        # call getImageFilename upon init and save; don't call again because new dice created every roll
        self._imageFilename = self.getImageFilename(value, imageFolder, False)
        self._imageFilenameSelected = self.getImageFilename(value, imageFolder, True)
        self._yamGuiUtil = YamGuiUtil()
        self._image = self._yamGuiUtil.loadImage(self._imageFilename, self._scale)
        self._width = self._image.get_width()
        self._height = self._image.get_height()
        self._rect = self._image.get_rect().move(x, y)    # used to detect object/mouse collisions
        self._clicked = False    # prevents multiple clicks at once
        self._selected = False    # indicates die to be rerolled or not

    def isSelected(self):
        return self._selected

    def getIndex(self):
        return self._index

    def getVal(self):
        return self._value

    """
    @returns True if Dice clicked
    """
    def draw(self, diceSurface):
        action = False    # for diceManager to know if anything happened
        pos = self._yamGuiUtil.getMousePosition(diceSurface)    # mouse position
        if self._rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and not self._clicked:
            action = True
            self._clicked = True
            if self._selected:    # deselect
                self._selected = False
                self._image = self._yamGuiUtil.loadImage(self._imageFilename, 1.0)
            else:    # select
                self._selected = True
                self._image = self._yamGuiUtil.loadImage(self._imageFilenameSelected, 1.0)
        if pygame.mouse.get_pressed()[0] == 0:
            self._clicked = False
        diceSurface.blit(self._image, (self._rect.x, self._rect.y))    # add dice to dice surface
        return action

    def getImageFilename(self, value, imageFolder, selected):
        filename = imageFolder + "/" + str(value)
        if selected:
            filename += "reroll.png"
        else:
            filename += ".png"
        return filename