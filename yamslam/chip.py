"""
chip manager & chip sprite objects
chip.py
Max Shinno
"""

import pygame
from enum import Enum
from yamGuiUtil import YamGuiUtil

"""
enum for 4 chip states
"""
class ChipState(Enum):
    DEPLETED = 0
    UNAVAIL = 1
    AVAIL = 2
    SELECTED = 3

class ChipManager():
    def __init__(self, chipSurface):
        self._chipSurface = chipSurface
        self._chipSurface.fill((0, 0, 0))
        self._chipGroup = pygame.sprite.Group()
        self._chipValueSelected = 0
        self._chipsDepleted = []

    """
    procedure to create all chip objects in correct states
    """
    def loadChips(self, chipDict, imagesLocation, scale, x, xIncrement, y, yIncrement):
        self._chipGroup.empty()
        currChip = 0
        chips = list(chipDict.keys())
        chips.sort()
        for chip in chips:
            match chipDict[chip]:
                case 0:
                    chipState = ChipState.DEPLETED
                case 1:
                    chipState = ChipState.UNAVAIL
                case 2:
                    chipState = ChipState.AVAIL
                case 3:
                    chipState = chipState.SELECTED
            # 2 columns:
            if currChip % 2 == 0:
                x = 0
                y += yIncrement
            else:
                x = xIncrement
            self._chipGroup.add(Chip(chip, chipState, imagesLocation, x, y, scale, self._chipSurface, currChip == len(chips)-1))
            currChip += 1
        self._chipValueSelected = 0    # when starting or next turn, no chips should be selected

    """
    procedure to call all chips' draw methods
    """
    def drawChips(self):
        for chip in self._chipGroup:
            value = chip.draw()
            if value == 0:    # deselection
                self._chipValueSelected = 0
            elif value > 0:    # select a chip
                self._chipValueSelected = value
                self.deselectOldChips(value)

    """
    procedure to check if any chip is available
    """
    def isChipsAvail(self):
        for chip in self._chipGroup:
            if chip.getState() == ChipState.AVAIL:
                return True
        return False

    """
    procedure to deselect all chips except one
    """
    def deselectOldChips(self, newChipValue):
        for chip in self._chipGroup:
            if chip.getState() == ChipState.SELECTED and chip.getValue() != newChipValue:
                chip.deselect()

    def getChipSelected(self):
        return self._chipValueSelected

class Chip(pygame.sprite.Sprite):
    def __init__(self, value, state, imageFolder, x, y, scale, chipSurface, centerChip):
        super(Chip, self).__init__()
        self._value = value    # 5, 10, 20, 25, 30, 40, or 50
        imageFilename = self.getImageFilename(value, state, imageFolder)
        self._guiUtil = YamGuiUtil()
        self._image = self._guiUtil.loadImage(imageFilename, scale)
        self._width = self._image.get_width() * 2 if centerChip else self._image.get_width    # Large Straight width *2 so don't have to worry abt centering
        self._height = self._image.get_height()
        self._scale = scale
        self._rect = self._image.get_rect().move(x, y)
        if centerChip:
            self._rect = self._image.get_rect().move(x+(self._image.get_width()/2), y)    # so rect is centered on width
        self._clicked = False
        self._selected = False
        self._state = state
        self._chipSurface = chipSurface
        self._imageFolder = imageFolder

    def getValue(self):
        return self._value

    def deselect(self):
        if not self._selected:
            return
        self._selected = False
        self._state = ChipState.AVAIL
        imageFilename = self.getImageFilename(self._value, self._state, self._imageFolder)
        self._image = self._guiUtil.loadImage(imageFilename, self._scale)
        self._chipSurface.blit(self._image, (self._rect.x, self._rect.y))

    """
    @returns -1 if nothing happens, 0 if the chip is deselected, or its value if it is selected
    """
    def draw(self):
        value = -1    # value of chip that is selected
        pos = self._guiUtil.getMousePosition(self._chipSurface)    # mouse position
        if self._rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and not self._clicked:
            self._clicked = True
            # deselect chip that was selected
            if self._state == ChipState.SELECTED:
                self.deselect()
                value = 0
            elif self._state == ChipState.AVAIL:
                value = self._value
                self._state = ChipState.SELECTED
                imageFilename = self.getImageFilename(self._value, self._state, self._imageFolder)
                self._image = self._guiUtil.loadImage(imageFilename, self._scale)
                self._selected = True
        if pygame.mouse.get_pressed()[0] == 0:
            self._clicked = False
        self._chipSurface.blit(self._image, (self._rect.x, self._rect.y))
        return value

    def getImageFilename(self, value, state, folder):
        filename = folder + "/" + str(value)
        match state:
            case ChipState.DEPLETED:
                filename += "depleted.png"
            case ChipState.UNAVAIL:
                filename += "unavail.png"
            case ChipState.AVAIL:
                filename += ".png"
            case ChipState.SELECTED:
                filename += "selected.png"
        return filename

    def getState(self):
        return self._state

    def getValue(self):
        return self._value