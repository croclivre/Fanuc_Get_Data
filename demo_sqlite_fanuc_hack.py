import sqlite3
import pandas as pd
from fanuc_hack import *


column_name = robot_url_pointer("file:///home/pi/Documents/LR-Mate1.html",1,6,"COLUMN_NAME")
register = robot_url_pointer("file:///home/pi/Documents/LR-Mate1.html",1,6,"REG")
#alarm = robot_url_pointer("file:///home/pi/Documents/LR-Mate1.html",301,350,"REG")

from datetime import datetime
date_temps = [datetime.date(datetime.now()).strftime('%-d/%-m/%-Y'),datetime.time(datetime.now()).strftime('%-H:%M:%S')]
register.extend(date_temps)

try:
    sqliteConnection = sqlite3.connect('file.db')

    cursor = sqliteConnection.cursor()
  
    cursor.execute('create table if not exists exemple_database(Override FLOAT,LastCycleTime FLOAT,CycleCount FLOAT,HomePath FLOAT,TotalCount FLOAT, Date TEXT, Temps TEXT);')
    cursor.execute("insert into exemple_database (Override,LastCycleTime,CycleCount,HomePath,TotalCount,Date,Temps) VALUES (?,?,?,?,?,?,?);", register)
    cursor.execute('select * from exemple_database;')

    result = cursor.fetchall()
    #fetch the data from the sql table
    print(result)
  
    sqliteConnection.commit()
    cursor.close()
    
except sqlite3.Error as error:
    print('Error occured - ', error)
  
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print('SQLite Connection closed')


