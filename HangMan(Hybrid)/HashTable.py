###############################################################
###used to sync the binary file dictionary with the database###
###############################################################

import sqlite3 as sq
import pickle
fh=sq.connect('Hangman_UserData.db')
cursor=fh.cursor()
cursor.execute("""
SELECT username
FROM tbl_players
""")
temp=cursor.fetchall()
fh.close()
arr=[]
total=0
for i in temp:
    value=str(i[0])
    num=8
    for j in range(0,len(value)-1):
        T=ord(value[j])
        T1=ord(value[j+1])
        total=total+(T*(T1*num))
        num=num*1.5
    indx=total%10000
    indx=round(indx)
    fh=open('HashTbl','rb')
    _dict=pickle.load(fh)
    fh.close()
    stored=False
    while not stored:
        if _dict[indx]=="":
            _dict[indx]=value
            stored=True
            fh=open('HashTbl','wb')
            pickle.dump(_dict,fh)
            fh.close()
        else:
            indx=indx+1
