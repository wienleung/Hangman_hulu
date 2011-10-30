from token import Token
from guesser import Guesser

#init
guesser = Guesser()
token = Token()

for times in range(1):
  guesser.reset()
  token.getNewToken()
  token.printToken()

  guessCount = 0
  while token.status == 'ALIVE':
    guess = guesser.makeGuess(token.state)
    print 'Guess: ' + guess
    token.guess (guess)
    token.printToken()
    guessCount += 1

  print 'Total guesses: ' + str(guessCount)
  print '+'*60

