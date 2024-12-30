####################################################
############# Coin flip mini game ##################
####################################################


#imports#
import random
import time
import os
###class definitions###
class difficulty:
    def __init__(self, lmultiplier, wmultiplier):
        self.lmultiplier=lmultiplier
        self.wmultiplier=wmultiplier
class player:
    def __init__(self, attempts, balance, score, cstreak, lstreak, infunds, name):
        self.attempts=attempts
        self.balance=balance
        self.score=score
        self.cstreak=cstreak
        self.lstreak=lstreak
        self.infunds=infunds
        self.name=name
    def turnover(self,win,diff):
        self.attempts=self.attempts+1
        if win==True:
            #aggregation used here for calculating player scores based on difficulty setting##
            self.balance=self.balance*diff.wmultiplier
            self.score=self.score+1
            self.cstreak=self.cstreak+1
            if self.cstreak>self.lstreak:
                self.lstreak=self.cstreak
        else:
            self.balance=round(self.balance/diff.lmultiplier,2)
            self.cstreak=0
        return self
    def funds(self, infunds):
        self.balance=self.balance+infunds
        self.infunds=self.infunds+infunds
#functions and procedures#

#misc subroutines#

#'clear' used to reset the console#
def clear():
    os.system('cls')
    
#prints relevant variables and calculates data to summarise the game#
def end(player,offplayer,mode):
    if mode=="1":
        clear()
        print(player.name,"\nScore: ",player.score,"\nAttempts: ",player.attempts,"\nLongest Streak: ",player.lstreak,"\nPoints: ",round(player.balance,2))
        if player.balance>player.infunds:
            print("\nWell Done! You gained ",player.balance-player.infunds, " points")
        elif player.balance==player.infunds:
            print("\nFair Play, You Had No Net Gain Or Loss.")
        else:
            print("\nToo Bad, You Lost ",player.infunds-player.balance, " points")
    else:
        clear()
        print("Player: ",player.name,"\n\nScore: ",player.score,"\nAttempts: ",player.attempts,"\nLongest Streak: ",player.lstreak,"\nPoints: ",round(player.balance,2),"\n\nPlayer: ",offplayer.name,"\n\nScore: ",offplayer.score,"\nAttempts: ",offplayer.attempts,"\nLongest Streak: ",offplayer.lstreak,"\nPoints: ",round(offplayer.balance,2))
        if player.balance>offplayer.balance:
            print("\n\n",player.name," Wins\n\n",offplayer.name," You Were This Close: ",round(player.balance-offplayer.balance,2))
        elif offplayer.balance>player.balance:
            print("\n\n",offplayer.name," Wins\n\n",player.name," You Were This Close: ",round(offplayer.balance-player.balance,2))
        else:
            print("Woah! A Draw!")
    time.sleep(2)
    x=input("Press Enter To Continue.")
    start()
    
#takes all inputs for game setup with validation#
def start(diffs):
    clear()
    begin=input("Press Enter To Start")
    clear()
    mode=input("How Many Players? (1-2)\n")
    if not mode.isdigit():
        print("Invalid Input")
        time.sleep(2)
        start()
    else:
        name1=""
        name2=""
        while name1=="" or name2=="":
            clear()
            if mode=='1':
                name1=input("Please Enter A Name: ")
                name2="N/A"
                p1=player(0,0,0,0,0,0,name1)
                p2=player(0,0,0,0,0,0,name2)
            elif mode=='2':
                name1=input("PLAYER 1 What Is Your Name?\n")
                name2=input("PLAYER 2 What Is Your Name?\n")
                if name1.isspace() or name2.isspace() or name1=="" or name2=="":
                    clear()
                    print("Invalid Input")
                    time.sleep(2)
                    start()
                #recursion used here to handle invalid inputs#
                while name1[0]==" ":
                    name1=name1[1:]
                while name2[0]==" ":
                    name2=name2[1:]
                while name1[len(name1)-1]==" ":
                    name1=name1[:len(name1)-1]
                while name2[len(name2)-1]==" ":
                    name2=name2[:len(name2)-1]
                clear()
                if name1.lower() != name2.lower():
                    p1=player(0,0,0,0,0,0,name1)
                    p2=player(0,0,0,0,0,0,name2)
                else:
                    clear()
                    print("Names Must Be Different.")
                    time.sleep(2)
                    start()
                    #recursion used here to handle invalid inputs#
            else:
                print("Invalid Input")
                time.sleep(2)
                start()
                #recursion used here to handle invalid inputs#
    diff=""
    while diff=="":
        clear()
        temp=input("Please Select A Difficulty (easy/medium/hard)\n")
        try:
            temp=temp.lower()
            diff=diffs[temp]
        except:
            clear()
            print("Invalid Input")
            time.sleep(2)
            continue
    while p1.infunds==0:
        clear()
        infunds=input("Please Enter The Amount Of Points You Wish To Start With: \n")
        if not infunds.isdigit():
            clear()
            print("Invalid Input")
            time.sleep(2)
            continue
        else:
            infunds=int(infunds)
            p2.funds(infunds)
            p1.funds(infunds)
            game(p1,diff,p2,mode)

#mini game code, takes round inputs, generates random values and comapres them#
def game(player,diff,offplayer,mode):
    clear()
    if player.balance==0.01 or offplayer.balance==0.01:
        print("Game Over!")
        time.sleep(2)
        end(player,offplayer,mode)
    print(player.name,"\nScore: ",player.score,"\nAttempts: ",player.attempts,"\nStreak: ",player.cstreak,"\nLongest Streak: ",player.lstreak,"\nPoints: ",round(player.balance,2),"\n\nIf You Wish To Quit, Type 'quit'.\nHeads or Tails?")
    guess=input("")
    if guess.isalpha():
        guess=guess.lower()
        if guess=="heads" or guess=="h":
            g=1
        elif guess=="tails" or guess=="t":
            g=0
        elif guess=="quit" or guess=="q":
            end(player,offplayer,mode)
        else:
            clear()
            print("Invalid Input")
            time.sleep(2)
            game(player,diff,offplayer,mode)
            #recursion used here to handle invalid inputs#
    else:
        clear()
        print("Invalid Input")
        time.sleep(2)
        game(player,diff,offplayer,mode)
        #recursion used here to handle invalid inputs#
    coin=random.randint(0,2)
    if coin==g:
        win=True
        print("Winner!")
    else:
        win=False
        print("Loser!")
    time.sleep(2)
    player.turnover(win,diff)
    if mode=="2":
        game(offplayer,diff,player,mode)
        #recursion used here to handle invalid inputs#
    else:
        game(player,diff,offplayer,mode)
        #recursion used here to handle invalid inputs#
    
