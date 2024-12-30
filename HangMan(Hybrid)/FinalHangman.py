####################################
######## Hangman game code #########
####################################


#imports#
from CoinFlipMKII import *
import random
import sqlite3 as sq
import time
from hangman_art import *
import tkinter as tk
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import os
import sys
import math
import pickle

#class definitions#

#creates a self defined stack data type with relevant methods#
class mystack:
    def __init__(self,size):
        self.size=size
        self.data=[None]*size
        self.pointer=0
    def push(self, value):
        if self.isfull()==False:
            self.data[self.pointer]=value
            self.pointer=self.pointer+1
        else:
            return None
    def pop(self):
        if self.isempty()==False:
            self.pointer=self.pointer-1
            return self.data[self.pointer]
        else:
            return False
    def isfull(self):
        full=False
        if self.pointer==self.size:
            full=True
        return full
    def isempty(self):
        empty=False
        if self.pointer==0:
            empty=True
        return empty
    def peek(self):
        if self.isempty()==False:
            return self.data[self.pointer-1]
        else:
            return None

##functions and procedures##

#reruns the code from the beginning#
def restart():
    python=sys.executable
    os.execl(python, python, * sys.argv)

#sets up variables for the loading of an existing save#
def ldsave():
    global new
    acc.destroy()
    new=False
    acc_log('')

#sets up variables for the creation of a new save# 
def newsave():
    global new
    acc.destroy()
    new=True
    acc_log('')

##performs all checks for logging in and accessing the database. includes validation and encryption###
def acc_check():
    global user
    global skill
    number=8
    total=0
    nametemp=str(nameinput.get())
    nametemp=nametemp.lower()
    nametemp=nametemp.capitalize()
    passwordtemp=str(passwordinput.get())
    acc2.destroy()
    #hashing algorithm used to encrypt the password#
    for i in range(0,len(passwordtemp)-1):
        PT=ord(passwordtemp[i])
        PT1=ord(passwordtemp[i+1])
        total=total+(PT*(PT1*number))
        number=number*1.5
    total=total%10000
    total=round(total)
    fh=sq.connect('Hangman_UserData.db')
    cursor=fh.cursor()
    if new:
        _dict=pickle.load(open('HashTbl','rb'))
        num=8
        tot=0
    #hashing algorithm used to access a hash table for quick presence checks on existing usernames#
        for j in range(0,len(nametemp)-1):
            T=ord(nametemp[j])
            T1=ord(nametemp[j+1])
            tot=tot+(T*(T1*num))
            num=num*1.5
        indx=tot%10000
        indx=round(indx)
        stored=False
        while not stored:
            if _dict[indx]==nametemp:
                acc_log('Name Taken')
            elif _dict[indx]=="":
                _dict[indx]=nametemp
                stored=True
                fh1=open('HashTbl','wb')
                pickle.dump(_dict,fh1)
                fh1.close()
                cursor.execute("""
                INSERT INTO tbl_players(username,password,skill)
                VALUES(?,?,?)
                """,(nametemp,total,0))
                fh.commit()
                fh.close()
                skill=0
                user=nametemp
                Game_Select()
            else:
                indx=indx+1
    else:
        try:
            cursor.execute("""
            SELECT *
            FROM tbl_players
            WHERE username=?
            """,(nametemp,))
            tempsave=cursor.fetchall()
            tempsave=tempsave[0]
            fh.close()
        except:
            fh.close()
            acc_log('Save not found')
        else:
            if total!=tempsave[1]:
                fh.close()
                print(tempsave[1])
                print(total)
                acc_log("Incorrect username or password")
            else:
                skill=tempsave[2]
                user=tempsave[0]
                Game_Select()

##code to facilitate the use of custom files via file browser##
def open_file():
    global fh
    fh=askopenfile(mode='r',filetypes=[('Text Files','*txt')])
    if fh is not None:
        fa.set('File Attached')
    else:
        fa.set('')

##front end of file upload##
def uploadfiles():
    try:
        for line in fh:
            words.append(line.strip())
            scores.append(0)
        fh.close()
        progbar=Progressbar(sp, orient=tk.HORIZONTAL, length=220, mode="determinate")
        progbar.grid(row=4,column=0,columnspan=3)
        for i in range(0,5):
            sp.update_idletasks()
            progbar['value']+=20
            time.sleep(0.5)
        progbar.destroy()
        Label(sp,text='File Uploaded Successfully!',foreground="green",background="#42d5f5").grid(row=4,columnspan=3,pady=10)
        time.sleep(2)
        sp.destroy()
        word_select()
    except:
        Label(sp, text='No File Selected', foreground="red",background="#42d5f5").grid(row=4,columnspan=3,pady=10)
##front end of file attach##
def fileattach():
    global fa
    global sp
    learn=True
    gamemode.destroy()
    sp=tk.Tk()
    sp.title('Attach File')
    sp.geometry('400x200')
    sp.configure(bg='#42d5f5')
    fa=tk.StringVar()
    fa.set("")
    textfile=tk.Label(sp,text='Upload text file(Works better with shorter lists)')
    textfile.configure(bg="#42d5f5")
    textfile.grid(row=0,column=0, padx=10, columnspan=10)
    Label(sp,textvariable=fa,foreground='purple',background="#42d5f5").grid(row=1,column=2)
    attach=tk.Button(sp,text='Browse',command=lambda:open_file())
    attach.configure(bg='yellow')
    attach.grid(row=1,column=0,pady=10)
    upld=tk.Button(sp,text='Upload',command=uploadfiles)
    upld.configure(bg='yellow')
    upld.grid(row=2, column=0,pady=10)
    sp.mainloop

##sets variables up to be used in the practice gamemode##
def practicewords():
    gamemode.destroy()
    fh=open('words.txt','r')
    for line in fh:
        words.append(line.strip())
    word_select()

##sets variables up to be used in the challenge gamemode##
def wordchallenge():
    global challenge
    challenge=True
    gamemode.destroy()
    fh=open('words.txt','r')
    for line in fh:
        words.append(line.strip())
    word_select()

##front end of login options##
def acc_select():
    global acc
    acc=tk.Tk()
    acc.title("Setup Wizard")
    acc.configure(bg="#42d5f5")
    acc.geometry('400x200')
    Label(acc,text='Do you have an existing save?',background="#42d5f5").grid(row=0,column=1,padx=10, columnspan=3)
    loadsave=tk.Button(acc,text='Load Save',command=ldsave)
    loadsave.configure(bg="yellow")
    loadsave.grid(row=1,column=1)
    createsave=tk.Button(acc,text='Create New', command=newsave)
    createsave.configure(bg="yellow")
    createsave.grid(row=1, column=3)
    acc.mainloop()

##taeks inputs for account selection/creation##
def acc_log(error):
    global nameinput
    global passwordinput
    global acc2
    global errmsg
    if new==True:
        acc2title="Sign Up"
    else:
        acc2title="login"
    acc2=tk.Tk()
    acc2.title(acc2title)
    acc2.configure(bg="#42d5f5")
    acc2.geometry('400x200')
    errmsg=tk.StringVar()
    errmsg.set(error)
    Label(acc2,text='UserName:',background="#42d5f5").grid(row=1,column=1,padx=10,pady=10)
    Label(acc2,text='Password:',background="#42d5f5").grid(row=2,column=1,padx=10,pady=10)
    nameinput=tk.Entry(acc2)
    nameinput.grid(row=1,column=2,padx=10,pady=10)
    passwordinput=tk.Entry(acc2, show='*')
    passwordinput.grid(row=2,column=2,padx=10,pady=10)
    submit=tk.Button(acc2,text='Next',command=acc_check)
    submit.configure(bg="yellow")
    submit.grid(row=3,column=2,padx=10,pady=10)
    Label(acc2,textvariable=errmsg,foreground='red', background="#42d5f5").grid(row=4,column=2,columnspan=2,padx=10,pady=10)
    acc2.mainloop()

##sets variables for coin flip game mode##
def coinflip():
    gamemode.destroy()
    easy=difficulty(1.25,2)
    medium=difficulty(2,2)
    hard=difficulty(2,1.25)
    diffs={"easy":easy,"medium":medium,"hard":hard}
    start(diffs)

##front end and select varibaels used for gamemode selection screen##
def Game_Select():
    global words
    global scores
    global gamemode
    global challenge
    global learn
    global count
    count=0
    challenge=False
    learn=False
    gamemode=tk.Tk()
    gamemode.title('Select Mode')
    gamemode.configure(bg="#42d5f5")
    gamemode.geometry('400x200')
    words=[]
    scores=[]
    cf=tk.Button(gamemode, text='CoinFlipMiniGame',command=coinflip)
    cf.configure(bg="yellow")
    cf.grid(row=4,column=2,padx=10,pady=10)
    learn=tk.Button(gamemode, text='Learn',command=fileattach)
    learn.configure(bg="yellow")
    learn.grid(row=1,column=2,padx=10,pady=10)
    practice=tk.Button(gamemode,text='Practice', command=practicewords)
    practice.configure(bg="yellow")
    practice.grid(row=2,column=2,padx=10,pady=10)
    challenge=tk.Button(gamemode, text='Challenge', command=wordchallenge)
    challenge.configure(bg="yellow")
    challenge.grid(row=3,column=2,padx=10,pady=10)
    gamemode.mainloop()

##takes input from the game and compares to the solution to give appropriate resposne##
def guess(temp):
    global tempout1
    global count
    if temp in guesses.get() or temp not in word:
        num.set(num.get()+1)
        if num.get()>5:
            count=0
            end("Oh Dear :(")
    else:
        for i in range(0,len(word)):
            if word[i]==temp:
                tempout[i]=temp
    tempout1=""
    correct=""
    for i in tempout:
        tempout1=tempout1+i
        correct=correct+i
        tempout1=tempout1+" "
    if correct==word:
        count=count+1
        end("Congrats!")
    guesses.set(guesses.get()+temp)
    out.set(tempout1)
    try:
        pic.set(hangart[num.get()])
    except:
        quit()

##code is ran when a round is won or lost, figures out the result and displays that and the correct solution before setting up a new round##
def end(msg):
    global skill
    if challenge==True:
        if msg=="Congrats!":
            skill=skill+len(word)
        else:
            if skill<5:
                skill=0
            else:
                skill=skill-5
        fh=sq.connect('Hangman_UserData.db')
        cursor=fh.cursor()
        cursor.execute("""
        UPDATE tbl_players
        SET skill=?
        WHERE username=?
        """,(skill,user))
        fh.commit()
        fh.close()
    msgl=tk.Label(root, text=msg, font=f1)
    msgl.configure(bg="#42d5f5")
    msgl.grid(row=0, column=3,columnspan=5)
    L4=tk.Label(root, text="The word was: ", font=f1)
    L5=tk.Label(root, textvariable=answer, font=f1)
    L4.configure(bg="#42d5f5")
    L5.configure(bg="#42d5f5")
    L4.grid(row=1, column=3, columnspan=5)
    L5.grid(row=1, column=8, columnspan=6)
    root.update()
    time.sleep(3)
    root.destroy()
    word_select()

##individual subroutines for letters on the keyboard##
def Aa():
    temp="A"
    guess(temp)
def Bb():
    temp="B"
    guess(temp)
def Cc():
    temp="C"
    guess(temp)
def Dd():
    temp="D"
    guess(temp)
def Ee():
    temp="E"
    guess(temp)
def Ff():
    temp="F"
    guess(temp)
def Gg():
    temp="G"
    guess(temp)
def Hh():
    temp="H"
    guess(temp)
def Ii():
    temp="I"
    guess(temp)
def Jj():
    temp="J"
    guess(temp)
def Kk():
    temp="K"
    guess(temp)
def Ll():
    temp="L"
    guess(temp)
def Mm():
    temp="M"
    guess(temp)
def Nn():
    temp="N"
    guess(temp)
def Oo():
    temp="O"
    guess(temp)
def Pp():
    temp="P"
    guess(temp)
def Qq():
    temp="Q"
    guess(temp)
def Rr():
    temp="R"
    guess(temp)
def Ss():
    temp="S"
    guess(temp)
def Tt():
    temp="T"
    guess(temp)
def Uu():
    temp="U"
    guess(temp)
def Vv():
    temp="V"
    guess(temp)
def Ww():
    temp="W"
    guess(temp)
def Xx():
    temp="X"
    guess(temp)
def Yy():
    temp="Y"
    guess(temp)
def Zz():
    temp="Z"
    guess(temp)

##selects a random word from the relevant text file##
def word_select():
    global word
    if learn==True:
        score=math.floor(abs(random.randint(min(scores),max(scores))-random.randint(min(scores),max(scores)))*(1+max(scores)-min(scores))+min(scores))
        indx=scores.index(score)
        word=words[indx]
    else:
        indx=random.randint(0,len(words))
        word=words[indx]
    word=word.upper()
    game()

##runs the base game displaying all outputs on the front end##
def game():
    global guesses
    global root
    global tempout
    global num
    global out
    global pic
    global f1
    global answer
    global streak
    root=tk.Tk()
    root.title('Hangman')
    root.attributes('-fullscreen', 'True')
    root.configure(bg="#42d5f5")
    answer=tk.StringVar()
    answer.set(word)
    guesses=tk.StringVar()
    streak=tk.IntVar()
    streak.set(count)
    guesses.set("")
    tempout=[]
    tempout1=""
    correct=[]
    f1=('verdana',20)
    pic=tk.StringVar()
    num=tk.IntVar()
    num.set(0)
    out=tk.StringVar()
    for i in range(0,len(word)):
        tempout.append("_")
    for i in tempout:
        tempout1=tempout1+i
        tempout1=tempout1+" "
    out.set(tempout1)
    pic.set(hangart[num.get()])
    streaklabel=tk.Label(root,text="Streak:",font=f1,bg="#42d5f5")
    streaklabel.grid(row=0,column=11)
    streaktk=tk.Label(root,textvariable=streak, font=f1,bg="#42d5f5")
    streaktk.grid(row=0,column=12,padx=20)
    lq=tk.Button(root,text="Quit", command=quit, font=f1, bg="yellow")
    lq.grid(row=0,column=15)
    L1=tk.Label(root, textvariable=pic, font=f1,bg="#42d5f5")
    L1.grid(row=0, column=0,rowspan=5)
    L2=tk.Label(root, textvariable=guesses, font=f1,bg="#42d5f5")
    L2.grid(row=6, columnspan=2)
    L3=tk.Label(root, textvariable=out, font=f1,bg="#42d5f5")
    L3.grid(row=7, column=0)
    a=tk.Button(root, text='A', command=Aa, font=f1,bg="yellow")
    b=tk.Button(root, text='B', command=Bb, font=f1,bg="yellow")
    c=tk.Button(root, text='C', command=Cc, font=f1,bg="yellow")
    d=tk.Button(root, text='D', command=Dd, font=f1,bg="yellow")
    e=tk.Button(root, text='E', command=Ee, font=f1,bg="yellow")
    f=tk.Button(root, text='F', command=Ff, font=f1,bg="yellow")
    g=tk.Button(root, text='G', command=Gg, font=f1,bg="yellow")
    h=tk.Button(root, text='H', command=Hh, font=f1,bg="yellow")
    i=tk.Button(root, text='I', command=Ii, font=f1,bg="yellow")
    j=tk.Button(root, text='J', command=Jj, font=f1,bg="yellow")
    k=tk.Button(root, text='K', command=Kk, font=f1,bg="yellow")
    l=tk.Button(root, text='L', command=Ll, font=f1,bg="yellow")
    m=tk.Button(root, text='M', command=Mm, font=f1,bg="yellow")
    n=tk.Button(root, text='N', command=Nn, font=f1,bg="yellow")
    o=tk.Button(root, text='O', command=Oo, font=f1,bg="yellow")
    p=tk.Button(root, text='P', command=Pp, font=f1,bg="yellow")
    q=tk.Button(root, text='Q', command=Qq, font=f1,bg="yellow")
    r=tk.Button(root, text='R', command=Rr, font=f1,bg="yellow")
    s=tk.Button(root, text='S', command=Ss, font=f1,bg="yellow")
    t=tk.Button(root, text='T', command=Tt, font=f1,bg="yellow")
    u=tk.Button(root, text='U', command=Uu, font=f1,bg="yellow")
    v=tk.Button(root, text='V', command=Vv, font=f1,bg="yellow")
    w=tk.Button(root, text='W', command=Ww, font=f1,bg="yellow")
    x=tk.Button(root, text='X', command=Xx, font=f1,bg="yellow")
    y=tk.Button(root, text='Y', command=Yy, font=f1,bg="yellow")
    z=tk.Button(root, text='Z', command=Zz, font=f1,bg="yellow")
    a.grid(row=8,column=1)
    b.grid(row=8,column=2)
    c.grid(row=8,column=3)
    d.grid(row=8,column=4)
    e.grid(row=8,column=5)
    f.grid(row=8,column=6)
    g.grid(row=8,column=7)
    h.grid(row=8,column=8)
    i.grid(row=8,column=9)
    j.grid(row=8,column=10)
    k.grid(row=9,column=1)
    l.grid(row=9,column=2)
    m.grid(row=9,column=3)
    n.grid(row=9,column=4)
    o.grid(row=9,column=5)
    p.grid(row=9,column=6)
    q.grid(row=9,column=7)
    r.grid(row=9,column=8)
    s.grid(row=9,column=9)
    t.grid(row=9,column=10)
    u.grid(row=10,column=1)
    v.grid(row=10,column=2)
    w.grid(row=10,column=3)
    x.grid(row=10,column=4)
    y.grid(row=10,column=5)
    z.grid(row=10,column=6)
    if challenge==True:
        fh=sq.connect('Hangman_UserData.db')
        cursor=fh.cursor()
        cursor.execute("""
        SELECT *
        FROM tbl_players
        """)
        lb=cursor.fetchall()
        fh.close()
        n=len(lb)
    #bubble sort algorithm to order the lisyt of users in the leaderboard#
        swapped=False
        for i in range(n-1):
            for j in range(0,n-i-1):
                if (lb[j][2]>lb[j+1][2])or(lb[j][2]==lb[j+1][2]):
                    swapped=True
                    lb[j],lb[j+1]=lb[j+1],lb[j]
            if not swapped:
                return
    #stack is used to reverse the order of a list#
        lb1=mystack(len(lb))
        for i in lb:
            lb1.push(i)
        for i in range(0,len(lb)):
            lb[i]=lb1.pop()
        Label(root,text="___LEADERBOARD___",background="#42d5f5",font=f1).grid(row=0,column=17,columnspan=2,padx=30)
        Label(root,text="   ",background="#42d5f5",font=f1).grid(row=0,column=16)
        for i in range(0,len(lb)):
            Label(root,text=lb[i][0],background="#42d5f5",font=f1).grid(row=i+1,column=17)
            Label(root,text=lb[i][2],background="#42d5f5",font=f1).grid(row=i+1,column=18)
    root.mainloop()
##runs the first subroutine to begin the program##  
acc_select() 
