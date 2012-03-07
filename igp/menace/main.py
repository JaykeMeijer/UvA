import sys
from ai import Ai

started = False
status = [0, 0, 0, 0, 0, 0, 0, 0, 0]
ai = None


def startGame():
    '''Start the game.'''
    print "The computer makes the first step"
    ai = Ai()
    started = True
    ai.play()
    print "The board now looks like this:"
    printBoard(convert(status))

def play(field):
    '''Handle the move of a player and print start the AI move after that.'''
    print "You played", field
    
    if field < 1 or field > 9:
        print "That is not a field"
        return
    
    if status[field - 1] == 0:
        status[field - 1] = 1
    else:
        print "This field is already played"
        return
    
    ai.play()
    print "The board now looks like this:"
    printBoard(convert(status))
    checkField()


def checkField():
    '''Check if there are three in a row yet.'''
    # horizontal
    for i in [0, 3, 6]:
        if status[i]:
            if status[i + 1] == status[i] and status[i + 2] == status[i]:
                gameEnd(status[i])

    # vertical
    for i in [0, 1, 2]:
        if status[i]:
            if status[i + 3] == status[i] and status[i + 6] == status[i]:
                gameEnd(status[i])

    # diagonal
    if status[0]:
        if status[4] == status[0] and status[8] == status[0]:
            gameEnd(status[0])
    if status[6]:
        if status[4] == status[6] and status[2] == status[6]:
            gameEnd(status[4])


def gameEnd(value):
    '''Game has ended, deal with it.'''
    if value == 1:
        print "Congratulations, you won!"
    else:
        print "Sadly, you lost!"

    sys.exit(0)


def convert(toconvert):
    '''Convert the integer field to a character field to print.'''
    converted = []
    
    for i in toconvert:
        if i == 1:
            temp = "x"
        elif i == 2:
            temp = "o"
        else:
            temp = " "
        converted.append(temp)
    
    return converted


def printBoard(toshow):
    '''Print the board with the given fields.'''
    for i in xrange(9):
        sys.stdout.write(" ")

        sys.stdout.write(toshow[i])

        sys.stdout.write(" ")

        if not i in [2, 5, 8]:
            sys.stdout.write("|")
        
        if (i + 1) % 3 == 0 and i < 8:
            sys.stdout.write("\n---+---+---\n")
        elif i == 8:
            sys.stdout.write("\n")


def printNumbers():
    '''Print the numbers of the fields.'''
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    printBoard(numbers)


def printHelp():
    '''Print all the possible commands.'''
    print "The following commands are supported: \n\
           help:     Show this help\n\
           numbers:  Show which field has which number\n\
           start:    Start the game\n\
           play [.]: Play at this number\n\
           board:    Show the current board\n\
           quit:     Quit the program"


def main():
    '''User input handling.'''
    print "Welcome to Tic-Tac-Toe!\n"
    print "Type 'help' to see the available commands or type 'start' to \n\
start playing right away."
    print "Type your command:"

    ipt = sys.stdin.readline()
    while(ipt != "quit\n"):
        if ipt == "help\n":
            printHelp()
        elif ipt == "numbers\n":
            printNumbers()
        elif ipt == "start\n":
            startGame()
        elif ipt[0:4] == "play":
            if started:
                play(int(ipt[5:-1]))
            else:
                print "Game not started yet. Type 'start' to begin."
        elif ipt == "board\n":
            print "The current board is:"
            printBoard(convert(status))
        elif ipt != "quit\n":
            print "Unknown command. Type 'help' for all available commands."
        print ""
        
        print "Type your command:"
        ipt = sys.stdin.readline()


# Start the program
main()
