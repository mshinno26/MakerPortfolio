"""
objects representing each player
player.py
Max Shinno
"""

class Player:

    def __init__(self, name, index):
        self._index = index
        self._name = name
        self._score = 0

    def getIndex(self):
        return self._index

    def getName(self):
        return self._name

    def addPoints(self, points):
        self._score += points

    def getScore(self):
        return self._score