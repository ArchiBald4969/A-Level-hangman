###########################################################
######### Creating the database to store savedata #########
###########################################################


import sqlite3 as sq
fh=sq.connect('Hangman_UserData.db')
cursor=fh.cursor()
cursor.execute("""
CREATE TABLE tbl_players(
username VARCHAR(20) PRIMARY KEY,
password INTEGER,
skill INTEGER
)""")
