"""
object to find point-winning patterns in 5-dice roll
pattern.py
Max Shinno
"""

class Pattern:

    # initiate the object in a valid state
    def __init__(self):
        self._rolls = []    # define rolls (list of dice) as a global variable
        self._counts = []    # counts the frequency of each dice value where each index is a dice value
        self._patterns = []    # define patterns list as a global variable

    def getPatterns(self, rolls):
        self._patterns.clear()    # reset global patterns list
        self._rolls = rolls    # set global rolls list to param
        self.get_counts()    # get new counts
        # call all pattern functions to refill patterns dicitonary
        if self.yammerslammer():
            return self._patterns
        self.large()
        self.four_of_a_kind()
        self.full_house()
        self.flush()
        self.small()
        self.three_of_a_kind()
        self.two_pairs()
        # return patterns dictionary
        return self._patterns

    # check for yamslam (5 of a kind)
    def yammerslammer(self):
        # iterate through global counts list
        for i in range(len(self._counts)):
            if self._counts[i] == 5:    # if there is a count of 5, Yamslam
                # after rolling Yamslam, pick any chip & roll again
                self._patterns.append(50)
                self._patterns.append(40)
                self._patterns.append(30)
                self._patterns.append(25)
                self._patterns.append(20)
                self._patterns.append(10)
                self._patterns.append(5)
                return True
        return False

    # function to check for large straight (5 numbers in ascending order, i.e. 1 2 3 4 5)
    def large(self):
        # starting at 1 and then 2 in counts list...
        for i in range(2):
            # initialize bool (true if large straight, false if none)
            is_large = True
            # iterate through next 5 indices of counts list
            for j in range(i, i+5):
                # if any one of those 5 wasn't in the dice roll, set is_large to false
                if self._counts[j] == 0:
                    is_large = False
            # if large straight was found, set score
            if is_large:
                self._patterns.append(50)

    # function to check for four of a kind
    def four_of_a_kind(self):
        # iterate through counts list
        for i in range(len(self._counts)):
            # if count of 4 is found, set score
            if self._counts[i] == 4:
                self._patterns.append(40)

    # check for full house (one two-of-a-kind and one three-of-a-kind)
    def full_house(self):
        # initialize variables to check for three of a kind and two of a kind
        triple = False
        double = False
        # iterate through counts list
        for i in range(len(self._counts)):
            # if a count of three is found, set triple variable to true
            if self._counts[i] == 3:
                triple = True
            # if a count of two is found, set double variable to true
            if self._counts[i] == 2:
                double = True
        # set score if a double and a triple, to 0 if either or both is missing
        if double and triple:
            self._patterns.append(30)

    # check for flush (all even or all odd)
    def flush(self):
        # initialize bool (true if there is a flush, false if none)
        is_flush = True
        # iterate through even numbers in count
        for i in range(0, len(self._counts), 2):
            # if there are any even numbers, then there is no odd flush
            if self._counts[i] != 0:
                is_flush = False
        if is_flush:
            self._patterns.append(25)
        is_flush = True
        # iterate through odd numbers in count
        for i in range(1, len(self._counts), 2):
            # if there are any odd numbers, then there is no even flush
            if self._counts[i] != 0:
                is_flush = False
        # if a current is_flush is false, then no flush was found either time
        if is_flush:
            self._patterns.append(25)

    # check for small straight (only 4 numbers in ascending order, i.e. 1, 3, 4, 5, 6 — 1 is not part of the straight)
    def small(self):
        # start at 1, 2, or 3
        for i in range(3):
            # initialize bool (true if found a small straight, false if none)
            is_small = True
            # iterate through next 4 numbers in counts list
            for j in range(i, i+4):
                # if a number in the straight is missing, it's not self current straight
                if self._counts[j] == 0:
                    is_small = False
            # if straight found, set score
            if is_small:
                self._patterns.append(20)

    # procedure to check for three-of-a-kind
    def three_of_a_kind(self):
        # iterate through counts list (data structure filled by get_counts())
        for i in range(len(self._counts)):
            # if a count of 3 is found, set score
            if self._counts[i] > 2:
                self._patterns.append(10)

    # function to check for two pairs
    def two_pairs(self):
        # initialize pairs count
        pairs = 0
        # iterate through counts list
        for i in range(len(self._counts)):
            # if a pair is found, increment pairs count
            if self._counts[i] == 4:
                self._patterns.append(5)
                return
            elif self._counts[i] > 1:
                pairs += 1
        # if at least two pairs, set score, otherwise to 0
        if pairs > 1:
            self._patterns.append(5)

    # procedure to find the number of times each number (1-6) appears in the dice roll
    def get_counts(self):
        counts = [0, 0, 0, 0, 0, 0]    # initialize data structure: list of counts
        # iterate through the global rolls list
        for i in range(len(self._rolls)):
            counts[self._rolls[i]-1] += 1    # if 1 is found, increment index 0 by 1, etc.
        self._counts = counts    # set global list of counts