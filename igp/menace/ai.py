import pickle

class Ai:
    '''The AI class.'''
    matchboxes = []

    def __init__(self):
        '''Init the AI machine.'''
        loadMatchboxes(self)
        
    def loadMatchboxes(self):
        '''Load the matchboxes from file, if any exists.'''
        self.matchboxes = pickle.load('one.save')
        
    def saveMatchboxes(self):
        '''Save the matchboxes to the file and close the file.'''
        pickle.dump(self.matchboxes, 'one.save')

    def play():
        '''Let the ai make a move.'''
        print "Computer now playing"
