from collections import defaultdict

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n',
    'o','p','q','r','s','t','u','v','w','x','y','z']

def sortCharInStr(string):
  arr = list(string)
  arr.sort()
  return ''.join(arr)

class Dictionary:
  def __init__(self):
    #import dicitonary file
    rawDict = set(line.strip() for line in open('dictionary.txt'))
    
    #The dictionary consists of an array containing hash tables. The indices of the array
    #represent the number of letters in the word. The hash tables have keys of the characters
    #in the word sorted, and values of all the words that can by formed by rearranging the
    #characters in the key
    self.dict = []

    #init dictionies
    for i in range(50):
      self.dict.append(defaultdict(list))
    for word in rawDict:
      #filter out words with odd characters
      word = word.lower()
      validWord = True
      for char in word:
        if char not in alphabet:
          validWord = False
      if validWord == True:
        key = sortCharInStr(word)
        self.dict[len(word)][key].append(word)

  def getPossibleWords(self, word):
    validKeys = list()
    possibleWords = list()

    #get keys to words that can contain the same characters
    keys = self.dict[len(word)].keys()
    for key in keys:
      if set(key + '_').issuperset(word):
        #also ensure that letters appear the same # of times
        validWord = True
        for char in word:
          if char == '_':
            continue
          if word.count(char) != key.count(char):
            validWord = False 
        if validWord == True:
          validKeys.append(key)

    #ensure that the characters' positions match
    for key in validKeys:
      for possibleWord in self.dict[len(word)][key]:
        match = True 
        for index in range(len(word)):
          if word[index] != '_' and word[index] != possibleWord[index]:
           match = False 
           break
        if match == True:
          possibleWords.append(possibleWord)

    return possibleWords
