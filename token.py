import json
import urllib

class Token:
  baseurl = "http://gallows.hulu.com/play?code=w9leung@uwaterloo.ca" 
  filename = "play"

  def parseFile(self):
    file = open(self.filename, 'r')
    data = json.loads(file.read())
    self.status = data['status']
    self.token = data['token']
    self.state = data['state']
    self.remaining_guesses = data['remaining_guesses']

  def getNewToken(self):
    #get file 
    urllib.urlretrieve (self.baseurl, self.filename)
    self.parseFile()

  def guess(self, letter):
    #get new token with guess 
    url = self.baseurl + '&token=' + self.token + '&guess=' + letter
    urllib.urlretrieve (url, self.filename)
    self.parseFile()
    
  def printToken(self):
    print 'Token: ' + self.token
    print 'Status: ' + self.status
    print 'Remaining guesses: ' + str(self.remaining_guesses)
    print 'State: ' + self.state
    print
 
