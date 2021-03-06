# Notes
# Program Requires installation of Selenium Chrome Webdriver to run
# Program Requires Windows 10 Notifications to run


# Imports
import PySimpleGUI as sg
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector.cursor import MySQLCursor


def main():
    # Initialize connection to mysql server and create cursor
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="UrsaMajor",
        database="employee_timesheets"
    )
    cursor = MySQLCursor(mydb)
    cursor = mydb.cursor(buffered=True)

    # Initialize first PySimpleGui window where options are selected and functions are called
    window1 = window_1()
    while True:
        event, values = window1.read()
        if event == "Sign In":
            sign_in_protocol(values, cursor, mydb)
        if event == "Sign out":
            sign_out_protocol(values, cursor, mydb)
        if event == "Payroll Hours":
            payroll_protocol(values, cursor, mydb)
        if event == sg.WIN_CLOSED:
            break
    window1.close()


def window_1():
    # Input window Layout
    layout = [
        [sg.Text("North Star Automation")],
        [sg.Text("Employee Name")],
        [sg.Listbox(values=["Nick", "Albert", "Norm", "Kabel"], size=(10, 10), key="Employee_Listbox")],
        [sg.Button("Sign In")],
        [sg.Button("Sign out")],
        [sg.Text("Payroll Start Date(KEEP FORMATTING AS BELOW)")],
        [sg.Input("2020-12-01", key='-start-')],
        [sg.Text("Payroll End Date(KEEP FORMATTING AS BELOW)")],
        [sg.Input("2020-12-31", key='-end-')],
        [sg.Button("Payroll Hours")],
        [sg.Button("Request Hours Adjustment")],
        [sg.Button("Change Employee Settings")],
        [sg.Button("Add Employee")],
    ]
    return sg.Window("North Star Automation", layout)


def sign_in_protocol(values, cursor, mydb):

    # Create approriate Variables for SQL search and insertion
    name = ""
    for val in values["Employee_Listbox"]:
        name = val
    signin = 1
    signout = 0
    d = datetime.now()
    date = d.date()

    # Confirm name was selected and employee has not already logged in
    sql = "SELECT * FROM records WHERE name = (%s) and date = (%s) and signin = (%s)"
    data = (name, date, signin)
    cursor.execute(sql, data)
    x = None
    mydb.commit()
    for x in cursor:
        print(x)
    if name == "":
        sg.popup("Select Name Please")
    elif x is not None:
        sg.popup("Already Signed In!")

    # Log employee into SQL Database
    else:
        time = d.time()
        sql = "INSERT INTO records (name, date, time, signin, signout) VALUES (%s, %s, %s, %s, %s)"
        data = (name, date, time, signin, signout)
        cursor.execute(sql, data)
        mydb.commit()
        for x in cursor:
            print(x)
        print(data)
        sg.popup("Successfully Logged In!")


def sign_out_protocol(values, cursor, mydb):

    # Create approriate Variables for SQL search and insertion
    name = ""
    for val in values["Employee_Listbox"]:
        name = val
    signin = 0
    signout = 1
    d = datetime.now()
    date = d.date()

    # Confirm name was selected and employee has not already logged in
    sql = "SELECT * FROM records WHERE name = (%s) and date = (%s) and signout = (%s)"
    data = (name, date, signout)
    cursor.execute(sql, data)
    x = None
    mydb.commit()
    for x in cursor:
        print(x)
    if name == "":
        sg.popup("Select Name Please")
    elif x is not None:
        sg.popup("Already Signed Out!")

    # Log employee into SQL Database
    else:
        time = d.time()
        sql = "INSERT INTO records (name, date, time, signin, signout) VALUES (%s, %s, %s, %s, %s)"
        data = (name, date, time, signin, signout)
        cursor.execute(sql, data)
        mydb.commit()
        for x in cursor:
            print(x)
        print(data)
        sg.popup("Successfully Logged Out!")


def payroll_protocol(values, cursor, mydb):

    # Convert dates inputted by user into date-time objects
    start_input = values['-start-']
    end_input = values['-end-']
    start = datetime.strptime(start_input, "%Y-%m-%d")
    end = datetime.strptime(end_input, "%Y-%m-%d")
    day = timedelta(days=1)

    # Iterate over all dates between and included dates given by user
    while start <= end:
        payroll_dates = str(start.date())

        # Find all approriate SQL entries on iterated date
        sql = "SELECT time FROM records WHERE date like '{}' and signin=1;".format(payroll_dates)
        cursor.execute(sql)
        mydb.commit()

        # Skip loop if cursor is empty, otherwise UnboundLocalError
        if cursor == None:
            start = start + day
            continue

        # if cursor is populated turn sql time string and iterated date string into date-time object
        for x in cursor:
            signin_time = x
        signin_time_string = ''.join(signin_time)
        signin_time_final = payroll_dates + " " + signin_time_string
        signin_datetime_object = datetime.strptime(signin_time_final, "%Y-%m-%d %H:%M:%S.%f")

        # Find all approriate SQL entries on iterated date
        sql = "SELECT time FROM records WHERE date like '{}' and signout=1;".format(payroll_dates)
        print(sql)
        cursor.execute(sql)
        mydb.commit()

        # Skip loop if cursor is empty, otherwise UnboundLocalError
        if cursor == None:
            start = start + day
            continue

        # if cursor is populated turn sql time string and iterated date string into date-time object
        for x in cursor:
            signout_time = x
        signout_time_string = ''.join(signout_time)
        signout_time_final = payroll_dates + " " + signout_time_string
        signout_datetime_object = datetime.strptime(signout_time_final, "%Y-%m-%d %H:%M:%S.%f")
        print(signout_datetime_object)

        # Find Hours, Minutes and Seconds worked by employee on iterated date
        diff = signout_datetime_object - signin_datetime_object
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        print("Nick Worked ", hours, minutes, seconds)

        # Move loop forward
        start = start + day


if __name__ == '__main__':
    main()

# TO DO
# round dates
# payroll potocol
# create way for employees to request adjustment 
# Make adjustments easier?
# make employee list dynamic
