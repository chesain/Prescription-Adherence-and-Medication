import mysql.connector
from pyfiglet import Figlet
# Import the query functions
from functions import *

import getpass
from colorama import Fore, Back, Style

print()
passo = getpass.getpass("Enter your MySQL Password: ")
print()

# Establishing connection to the database
db = mysql.connector.connect(
    user='root', password=passo, host='localhost', database='MEDICATION_SCHEMA')

cursor = db.cursor(buffered=True)
#ubcursor = db.cursor(buffered=False)


stop = 'n'

f = Figlet(font='big')
print(f.renderText('P. A . M'))
print("*******************************************")
print("Prescription Adherence and Management (PAM)")
print("*******************************************")
print()
print()

while stop == 'n':
    print()
    print(Fore.WHITE + Back.BLUE + 'MENU:' + Style.RESET_ALL)
    
    print("1. Create a new prescription")
    print("2. Delete exisiting prescription")
    print("3. Track patients prescription adherence")
    print("4. View all prescriptions")
    print("5. Quit")

    print()
    user_ch = input("Select one of the following menu options: ")

    match user_ch:
            case "1":
                create_prescription(cursor, db)
            case "2":
                delete_prescription(cursor, db)
            case "3":
                check_adherence(cursor)
            case "4":
                view_prescriptions(cursor)
            case "5":
                stop = 'y'

cursor.close()
db.close()
              
                




