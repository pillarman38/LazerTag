from tkinter import *
import gameVars as gv

root = Tk()
root.title("Lazer Tag")

playAgain = False

def displayStats(player1,player2,player3,numOfPlayers,numOfStatsRcvd):
    while numOfStatsRcvd <= numOfPlayers:
        print(player1)

def playGame():
    gv.playAgain = True
    root.destroy()

def quitGame():
    gv.playAgain = False
    root.destroy()
    
playBtn = Button(root, text="Play again", command=playGame)
playBtn.pack()

quitBtn = Button(root, text="Quit", command=quitGame)
quitBtn.pack()

root.mainloop()