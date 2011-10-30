from dictionary import Dictionary

minPriority = 1.0/3

def countBlanks(string):
  count = 0
  for char in string:
    if char == '_':
      count += 1
  return count

#lower value is higher priority.
#priority is determined by amount of string solved
def getPriority(string):
  priority = 1 - 1.0*countBlanks(string)/len(string)
  return priority

class Guesser:
  vowels = ['a', 'e', 'i', 'o', 'u']
  one_letter = ['a', 'i']
  post_apostrophe = ['t', 'm', 's', 'v'] # v for ve. e will be guessed eventually...

  def __init__(self):
    #init dictionary
    self.dict = Dictionary()

    #import letter order
    self.letters = []
    f = open('letters.txt', 'r')
    for line in f:
      for char in line.strip().split():
        self.letters.append(char)

    #import two letter words
    self.twoLetteredWords = [] 
    f = open('2letter.txt', 'r')
    for line in f:
      for word in line.strip().split():
        self.twoLetteredWords.append(word)

    self.reset()

  def reset(self):
    #build list of letters sorted by decreasing frequency
    self.lettersLeft= list(self.letters)
    
    #list of next guesses
    self.next = list();

  def makeGuess(self, state):
    #handle apostrophes
    if "'_" in state:
      for char in self.post_apostrophe:
        if char in self.lettersLeft:
          self.lettersLeft.remove(char)
          return char

    state = state.lower()
    words = state.split()
    
    #handle single letter words
    if "_" in words:
      for char in self.one_letter:
        if char in self.lettersLeft:
          self.lettersLeft.remove(char)
          return char

    #handle special cases 
    for word in words:
      #should have some letters guessed first
      if '_' in word and getPriority(word) > minPriority:
        if len(word) == 2:
          #use common two letter list
          index = 1 - word.find('_') 
          char = word[index]

          for twoLetteredWord in self.twoLetteredWords:
            if twoLetteredWord[index] == char:
              retChar = twoLetteredWord[1-index]
              if retChar in self.lettersLeft:
                self.lettersLeft.remove(retChar)
                return twoLetteredWord[1-index]

        #handle 'and' and 'the'
        if len(word) == 3:
          for str in ['and', 'the']:
            valid = True
            index = -1

            #check that characters match position
            for i in range(len(word)):
              if word[i] == '_' and str[i] in self.lettersLeft:
                index = i
              elif word[i] != str[i]:
                valid = False

            if valid == True and index != -1:
              char = str[index]
              self.lettersLeft.remove(char)
              return char
 
    #sort words by priority (by % of word solved)
    #only care about words that have been solved to some degree,
    #defined by minPriority
    priority = list()
    for word in words:
      if '_' not in word or getPriority(word) < minPriority:
        continue

      if len(priority) == 0:
        priority.append(word)
      else:
        i = 0
        while i < len(priority) and getPriority(word) < getPriority(priority[i]):
          i += 1
        priority.insert(i, word)

    #handle by priority (highest % solved)
    for word in priority:
      possibleWords = self.dict.getPossibleWords(word) 
      possibleLetters = set()
      for possibleWord in possibleWords:
        for char in possibleWord:
          if char in self.lettersLeft:
            possibleLetters.add(char)
      for char in self.lettersLeft:
        if char in possibleLetters:
          self.lettersLeft.remove(char)
          return char

    #if all else fails, guess letters by frequency
    char = self.lettersLeft.pop(0)
    return char
