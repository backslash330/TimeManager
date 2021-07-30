  
# Notes
# Program Requires installation of Selenium Chrome Webdriver to run
# Program Requires Windows 10 Notifications to run


# Imports
import PySimpleGUI as sg
from datetime import datetime
from mysql import connector
import mysql.connector
from mysql.connector import cursor 
from mysql.connector.cursor import MySQLCursor
import time
import sys

from PySimpleGUI.PySimpleGUI import Combo, DropDown, Text


def main():

    # Initialize webpages to check for stock
    dictionary = {}
    list = ["Nick", "Perry", "Albert", "Cruz", "Kaleb", "Wayne", "Ted"]

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "UrsaMajor",
        database = "employee_timesheets"
    )    
    cursor = MySQLCursor(mydb)
    cursor =mydb.cursor(buffered=True)


    # Initilize webpages as keys in a dictionary with zero'd values
    for i in range(len(list)):
        dictionary[list[i]] = 0

    # Initilze first PySimpleGui window where personal information is entered for purchasing
    window1 = window_1()
    while True:
        event, values  = window1.read()
        if event == "Sign In":
            sign_in_protocol(values, cursor, mydb)
        if event == "Sign out":
            sign_out_protocol()
        if event == "Payroll Hours":   
            payroll_protocol()
        if event == sg.WIN_CLOSED:
            break
    window1.close()


def window_1():
    # Input window Layout
    layout = [
                [sg.Text("North Star Automation")],
                [sg.Text("Employee Name")],
                [sg.Listbox(values=["Nick","Albert","Norm","Kabel"], size=(10,10), key="Employee_Listbox")],
                [sg.Button("Sign In")],
                [sg.Button("Sign out")],
                [sg.Button("Payroll Hours")],
                [sg.Button("Request Hours Adjustment")],
                [sg.Button("Change Employee Settings")],
                [sg.Button("Add Employee")]
    ]
    return sg.Window("North Star Automation", layout)

def sign_in_protocol(values, cursor, mydb):
    name=""
    for val in values["Employee_Listbox"]:
        name=val
    signin = 1
    signout = 0
    d = datetime.now()
    date = d.date()
    sql = "SELECT * FROM records WHERE name = (%s) and date = (%s) and signin = (%s)"
    data = (name, date, signin)
    cursor.execute(sql, data)
    mydb.commit()
    for x in cursor:
        print(x)
    if x is not None:
        sg.popup("Already Signed In!")
    else:
        time = d.time()
        # CHECK IF ALREADY LOGGED IN
        sql = "INSERT INTO records (name, date, time, signin, signout) VALUES (%s, %s, %s, %s, %s)"
        data = (name, date, time, signin, signout)
        cursor.execute(sql, data)
        mydb.commit()
        for x in cursor:
            print(x)
        print(data)
        sg.popup("Successfully Logged In!")

def sign_out_protocol():
    name=""
    for val in values["Employee_Listbox"]:
        name=val
    d = datetime.now()
    date = d.date()
    time = d.time()
    signin = 1
    signout = 0
    # CHECK IF ALREADY LOGGED IN
    sql = "INSERT INTO records (name, date, time, signin, signout) VALUES (%s, %s, %s, %s, %s)"
    data = (name, date, time, signin, signout)
    cursor.execute(sql, data)
    mydb.commit()
    for x in cursor:
        print(x)
    print(data)
    sg.popup("Successfully Logged Out!")

def payroll_protocol():
    data ="2021-07-21"
    sql = "SELECT * FROM records WHERE date like '{}';".format(data)
    cursor.execute(sql)
    print(sql)
    mydb.commit()
    for x in cursor:
        print(x)
    calendar = calendar_1()
    while True:
            if event == sg.WIN_CLOSED:
                break 

if __name__ == '__main__':
    main()