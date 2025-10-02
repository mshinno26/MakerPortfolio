"""
Yamslam object connecting other game engine objects
yamslam.py
Max Shinno
"""

from pattern import Pattern
from player import Player
import sys
import random

class Yamslam:

    def __init__(self, names):
        self._players = []
        for i in range(len(names)):
            self._players.append(Player(names[i], i))
        self._curr_player = self._players[0]
        self._pattern = Pattern()
        self._chips = {}
        self.set_chips()
        self._winner = None
        self._yamslam = False
        self._rollNum = 0

    # function to reroll certain dice in a list
    def roll(self, dice, rerolls):
        if self._rollNum > 2:
            print("Error: Too many rolls.")
            sys.exit(1)
        for i in rerolls:
            dice[i] = random.randint(1, 6)
        self._rollNum += 1
        return dice

    # procedure to call pattern.getPatterns() and assign numbered states to each chip
    # sequencing: if lines 30 or 42 came later, the procedure would not work
    def pattern(self, dice):
        hands = self._pattern.getPatterns(dice)
        if len(hands) == 7:
            self._yamslam = True
        patterns = {}
        # 2 = chip matches roll & chips left; 1 = chips left but not part of roll; 0 = no chips left
        # iteration
        for chip in self._chips:
            # selection
            if chip in hands and self._chips[chip] > 0:
                patterns.update({chip: 2})
            elif self._chips[chip] > 0:
                patterns.update({chip: 1})
            else:
                patterns.update({chip: 0})
        return patterns

    # function to fill chips structure at the beginning of the game
    def set_chips(self):
        self._chips.update({5: 4})
        self._chips.update({10: 4})
        self._chips.update({20: 4})
        self._chips.update({25: 4})
        self._chips.update({30: 4})
        self._chips.update({40: 4})
        self._chips.update({50: 4})

    def checkChip(self, chip):
        return chip in self._chips

    # function to remove one chip from the structure, return True if Yamslam
    def score(self, points):
        self._chips[points] -= 1
        self._curr_player.addPoints(points)
        self.calcWinner()
        if not self._yamslam:
            self._rollNum = 3
            return False
        else:
            # after rolling Yamslam, roll again
            self._rollNum = 0
            self._yamslam = False
            return True

    # function to check if no chips left
    def end(self):
        for stack in self._chips.values():
            if stack != 0:
                return False
        return True

    def getChips(self):
        return self._chips

    def getScores(self):
        scores = {}
        for player in self._players:
            scores.update({player.getName(): player.getScore()})
        return scores

    def calcWinner(self):
        highscore = -1
        for player in self._players:
            if player.getScore() > highscore:
                highscore = player.getScore()
                self._winner = player

    def getWinner(self):
        return self._winner

    def nextTurn(self):
        self._curr_player = self._players[(self._curr_player.getIndex()+1) % len(self._players)]
        self._rollNum = 0

    def getCurrPlayer(self):
        return self._curr_player

    def getCurrPlayerNum(self):
        return self._curr_player.getIndex()

    def rollsLeft(self):
        return self._rollNum < 3

    def getNumRolls(self):
        return self._rollNum

    def resetRolls(self):
        self._rollNum = 0