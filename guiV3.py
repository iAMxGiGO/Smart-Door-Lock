from tkinter import *
from twilio.rest import Client
from random import randint
import bluetooth
from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
#unused
import os
import sys

#initializing GUI
gui = Tk()
gui.title("SDL")
#twilio credentials
account_sid = 'ACe6efcb98178d7fdc4a02ed513a1844f7'
auth_token = 'a6df87db787bde3c842b3dbcf631a255'
client = Client(account_sid, auth_token)
#GPIO setup
relay = 12
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay, GPIO.OUT)
#database connection setup
mydb = mysql.connector.connect(host="localhost", user="root", passwd="Ahmed",database="smartlock")
mycursor = mydb.cursor()
#database connection test and user table check
mycursor.execute("select * from users;")
for i in mycursor:
    print(i)

currentOTP = ""
def guiEventHandler(num):
    global operator
    global passcode
    global message
    if (num == -1):
        passcode = int(operator)
        print(passcode)
        message = "Thank You, Please Enter The OTP"
        labelText.set(message)
        otp = client.messages.create(
                              from_='whatsapp:+14155238886',
                              body='Your SDL OTP is: '+randomOTP(),
                              to='whatsapp:+966539322030'
                          )
        print(otp.sid)
        print(currentOTP)
        operator = ""
        input.set(operator)
    elif(num == -2):
        operator = ""
        input.set(operator)
        message = "Enter Your 6 Digit Passcode"
        labelText.set(message)
    elif (num == -3):
        if (currentOTP == operator):
            message = "OTP Is Correct"
            labelText.set("OTP Is Correct")
            sleep(1)
            GPIO.output(relay, 1)
            sleep(5)
            GPIO.output(relay, 0)
        else:
            message = "OTP Is Wrong"
            labelText.set(message)
    elif (num == -4):
        try:
            reader = SimpleMFRC522()
            tag = -1
            id = None
            rows = -1
            print("\nHold a tag near the reader")
            id, text = reader.read()
            print("ID: %s\nUser Is: %s" % (id,text))
            tag = str(id)
            searchForTagQuery = "select username , name from users WHERE rfid = "+tag+";"
            mycursor.execute(searchForTagQuery)
            for i in mycursor:
                print(i)
            rows = mycursor.rowcount
            print("rows = "+str(rows))
            if rows == -1:
                print ("\nNo User Found")
            else:
                print("door open")
                GPIO.output(relay, 1)
                sleep(5)
                GPIO.output(relay, 0) 
            sleep(2)
        except KeyboardInterrupt:
            GPIO.cleanup()
            raise
    elif (num == -5):
        print("Performing inquiry...")

        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True,
                                            flush_cache=True, lookup_class=False)

        print("Found {} devices".format(len(nearby_devices)))

        for addr, name in nearby_devices:
            try:
                print("   {} - {}".format(addr, name))
            except UnicodeEncodeError:
                print("   {} - {}".format(addr, name.encode("utf-8", "replace")))
    else:
        operator = operator+str(num)
        input.set(stars(operator))
        labelText.set(message)
def randomOTP():
    global currentOTP
    otpCode = str(randint(100000, 999999))
    currentOTP = otpCode
    return otpCode
def stars(string):
    global operator
    x = ""
    for i in range(len(string)):
       x = x + "*"
    return x
operator = ""
message = "Enter Your 6 Digit Passcode"
passcode = 0
input = StringVar()
labelText = StringVar()
labelText.set(message)
x = Label(gui, textvariable=labelText, font=('times new roman', 15, 'bold'), justify='center').grid(row=0, column=0, columnspan=3)
display = Entry(gui, bd=2, font=('times new roman', 20, 'bold'), fg='black', justify='center', textvariable=input).grid(row=1, column=0, columnspan=3)
btn1 = Button(gui, command=lambda:guiEventHandler(1), padx=16, pady=16, fg='black', font=('times new roman', 30, 'bold'), text='1').grid(row=2, column=0)
btn2 = Button(gui, command=lambda:guiEventHandler(2), padx=16, pady=16, fg='black', font=('times new roman', 30, 'bold'), text='2').grid(row=2, column=1)
btn3 = Button(gui, command=lambda:guiEventHandler(3), padx=16, pady=16, fg='black', font=('times new roman', 30, 'bold'), text='3').grid(row=2, column=2)
btn4 = Button(gui, command=lambda:guiEventHandler(4), padx=16, pady=16, fg='black', font=('times new roman', 30, 'bold'), text='4').grid(row=3, column=0)
btn5 = Button(gui, command=lambda:guiEventHandler(5), padx=16, pady=16, fg='black', font=('times new roman', 30, 'bold'), text='5').grid(row=3, column=1)
btn6 = Button(gui, command=lambda:guiEventHandler(6), padx=16, pady=16, fg='black', font=('times new roman', 30, 'bold'), text='6').grid(row=3, column=2)
btn7 = Button(gui, command=lambda:guiEventHandler(7), padx=16, pady=16, fg='black', font=('times new roman', 30, 'bold'), text='7').grid(row=4, column=0)
btn8 = Button(gui, command=lambda:guiEventHandler(8), padx=16, pady=16, fg='black', font=('times new roman', 30, 'bold'), text='8').grid(row=4, column=1)
btn9 = Button(gui, command=lambda:guiEventHandler(9), padx=16, pady=16, fg='black', font=('times new roman', 30, 'bold'), text='9').grid(row=4, column=2)
btn0 = Button(gui, command=lambda:guiEventHandler(0), padx=16, pady=16, fg='black', font=('times new roman', 30, 'bold'), text='0').grid(row=5, column=1)
btnClear = Button(gui, command=lambda:guiEventHandler(-2), padx=16, pady=16, fg='black', font=('times new roman', 15, 'bold'), text='Clear').grid(row=5, column=0)
btnOTP = Button(gui, command=lambda:guiEventHandler(-3), padx=8, pady=8, fg='black', font=('times new roman', 15, 'bold'), text='OTP').grid(row=5, column=2)
btnEnter = Button(gui, command=lambda:guiEventHandler(-1), padx=8, pady=8, fg='black', font=('times new roman', 15, 'bold'), text='Enter').grid(row=6, column=1)
btnRFID = Button(gui, command=lambda:guiEventHandler(-4), padx=8, pady=8, fg='black', font=('times new roman', 15, 'bold'), text='RFID').grid(row=6, column=0)
btnBLE = Button(gui, command=lambda:guiEventHandler(-5), padx=8, pady=8, fg='black', font=('times new roman', 15, 'bold'), text='Bluetooth').grid(row=6, column=2)

gui.mainloop()

