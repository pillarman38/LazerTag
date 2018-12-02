from tkinter import *
import gameVars as gv
root = Tk()
root.title("Lazer Tag")

gameTypeSelected = StringVar(root)
gameTypeSelected.set("Classic") # default value

gameTypelbl = Label(root, text="Game Type")
gameTypelbl.pack()

gameType = OptionMenu(root, gameTypeSelected,'Classic','Showdown','capture the Flag')
gameType.pack()

timerlbl = Label(root, text="Time")
timerlbl.pack()

timer = Spinbox(root, from_=1, to=60)
timer.pack()

numOfPlayersLbl = Label(root, text="Select number of players")
numOfPlayersLbl.pack()

numOfPlayers = Spinbox(root, from_=1, to_=6)
numOfPlayers.pack()

waitingTimeLbl = Label(root, text="Select game wait time")
waitingTimeLbl.pack()

waitingTime = Spinbox(root, from_=5, to_=10000)
waitingTime.pack()

def callback():
    gv.init()
    
    gv.game_mode = gameTypeSelected.get()
    gv.timer = int(timer.get())
    gv.num_players = int(numOfPlayers.get())
    gv.wait_time = int(waitingTime.get())
    print("Playing " + gameTypeSelected.get() + " with "+ " lives and " + str(timer.get()) + " minutes on the clock.")
    gv_dict=dict(wait_time=gv.wait_time,num_players=gv.num_players,game_mode=gv.game_mode)
    
    root.destroy()
    
b = Button(root, text="Play Game", command=callback)
b.pack()

root.mainloop()