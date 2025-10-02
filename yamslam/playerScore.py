"""
objects for printing scoreboard
playerScore.py
Max Shinno
"""

import pygame
from yamGuiUtil import YamGuiUtil

class PlayerScore(pygame.sprite.Sprite):
    def __init__(self, text, x, y, turn):
        super(PlayerScore, self).__init__()
        if turn:
            imageFilename = "miscImages/boardTurn.png"
        else:
            imageFilename = "miscImages/board.png"
        guiUtil = YamGuiUtil()
        self._image = guiUtil.loadImage(imageFilename, 1.0)
        self._rect = self._image.get_rect().move(x, y)
        font = pygame.font.Font("fonts/NovaMono.ttf", 24)
        self._text = font.render(text, True, (0, 0, 0))
        self._textRect = self._text.get_rect(center=self._image.get_rect().center)

    def draw(self, scoreboardSurface):
        self._image.blit(self._text, self._textRect)
        scoreboardSurface.blit(self._image, self._rect)