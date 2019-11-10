from nltk.corpus import words
import random

class Boggle():

    def __init__(self):
        self.score = 0
        self.answers = []
        self.dice = []
        self.boggleBoard = []
        self.setup()

    def setup(self):
        del self.answers[:]
        del self.dice[:]
        del self.boggleBoard[:]

        self.dice = [['A', 'E', 'A', 'N', 'E', 'G'],
            ['A', 'H', 'S', 'P', 'C', 'O'],
            ['A', 'S', 'P', 'F', 'F', 'K'],
            ['O', 'B', 'J', 'O', 'A', 'B'],
            ['I', 'O', 'T', 'M', 'U', 'C'],
            ['R', 'Y', 'V', 'D', 'E', 'L'],
            ['L', 'R', 'E', 'I', 'X', 'D'],
            ['E', 'I', 'U', 'N', 'E', 'S'],
            ['W', 'N', 'G', 'E', 'E', 'H'],
            ['L', 'N', 'H', 'N', 'R', 'Z'],
            ['T', 'S', 'T', 'I', 'Y', 'D'],
            ['O', 'W', 'T', 'O', 'A', 'T'],
            ['E', 'R', 'T', 'T', 'Y', 'L'],
            ['T', 'O', 'E', 'S', 'S', 'I'],
            ['T', 'E', 'R', 'W', 'H', 'V'],
            ['N', 'U', 'I', 'H', 'M', 'Qu']]

        random.shuffle(self.dice)
        for die in self.dice:
            random.shuffle(die)
            self.boggleBoard.append(die[0])

    def findInGrid(self, word, boggleBoard):
        #look for starting locations
        possibleLocations = []
        for index, dice in enumerate(boggleBoard):
            if dice[0] == word[0]:
                possibleLocations.append(index)
        #return false if no starting locations
        if not possibleLocations:
            return False

        #recursively search the grid and return boolean values
        #to determine if the word is in the grid
        previousDice = []
        found = []
        for pos in possibleLocations:
            found.append(self.adjacent(pos, boggleBoard, word, 0, previousDice))

        if any(found):
            return True
        return False

    def getCoords(self, i):
        """getCoords simply takes an index in a list ex. 4
        then it calculates the x and y coordinates in the
        boggle board. getCoords assumes a 4x4 grid and the
        index passed into it will not exceed 15"""
        return int(i%4), int(i/4)

    def getIndex(self, x, y):
        """getIndex is the opposite of getCoords. it takes in
        a tuple of x,y coordinates and calculates the index
        in the list. it also assumes a 4x4 grid and that 15
        will be the largest number"""
        return int(y * 4 + x)

    def adjacent(self, i, boggleBoard, word, letter, previousDice):
        if word[letter] == 'Q':
            letter = letter+1
        if i in previousDice:
            return False
        previousDice.append(i)
        if letter == len(word) - 1:
            return True
        letter += 1
        x, y = self.getCoords(i)
        
        if x > 0:
            if boggleBoard[self.getIndex(x-1, y)] == word[letter]:
                if self.adjacent(self.getIndex(x-1, y), boggleBoard, word, letter, previousDice):
                    return True
        if x < 3:
            if boggleBoard[self.getIndex(x+1, y)] == word[letter]:
                if self.adjacent(self.getIndex(x+1, y), boggleBoard, word, letter, previousDice):
                    return True
        if y > 0:
            if boggleBoard[self.getIndex(x, y-1)] == word[letter]:
                if self.adjacent(self.getIndex(x, y-1), boggleBoard, word, letter, previousDice):
                    return True
        if y < 3:
            if boggleBoard[self.getIndex(x, y+1)] == word[letter]:
                if self.adjacent(self.getIndex(x, y+1), boggleBoard, word, letter, previousDice):
                    return True
        if x > 0 and y > 0:
            if boggleBoard[self.getIndex(x-1, y-1)] == word[letter]:
                if self.adjacent(self.getIndex(x-1, y-1), boggleBoard, word, letter, previousDice):
                    return True
        if x < 3 and y < 3:
            if boggleBoard[self.getIndex(x+1, y+1)] == word[letter]:
                if self.adjacent(self.getIndex(x+1, y+1), boggleBoard, word, letter, previousDice):
                    return True
        if x > 0 and y < 3:
            if boggleBoard[self.getIndex(x-1, y+1)] == word[letter]:
                if self.adjacent(self.getIndex(x-1, y+1), boggleBoard, word, letter, previousDice):
                    return True
        if x < 3 and y > 0:
            if boggleBoard[self.getIndex(x+1, y-1)] == word[letter]:
                if self.adjacent(self.getIndex(x+1, y-1), boggleBoard, word, letter, previousDice):
                    return True
        return False

    def score_game(self):
        """The word must not have already been scored.
        It must be at least three letters long.
        It must be a word in the English language.
        It must be present in the 4x4 grid of dice.
        It may not use the same letter cube more than once per word"""

        seen = set()
        self.score = 0
        for ans in self.answers:
            word = str(ans).upper()
            if word not in seen:
                seen.add(word)
            else:
                print("The word %r has already been used." % (word))
                continue
            if len(word) < 3:
                print("The word %r is too short." % (word))
                continue
            if word.lower() not in words.words():
                print("The word %r is ... not a word." % (word))
                continue
            if self.findInGrid(word, self.boggleBoard):
                if len(word) < 5:
                    print("The word %r is worth 1 points." % (word))
                    self.score = self.score + 1
                elif len(word) < 6:
                    print("The word %r is worth 2 points." % (word))
                    self.score = self.score + 2
                elif len(word) < 7:
                    print("The word %r is worth 3 points." % (word))
                    self.score = self.score + 3
                elif len(word) < 8:
                    print("The word %r is worth 5 points." % (word))
                    self.score = self.score + 5
                else:
                    print("The word %r is worth 11 points." % (word))
                    self.score = self.score + 11
            else:
                print("The word %r is not present." % (word))

        print("Your total score is %d points!" % (self.score))