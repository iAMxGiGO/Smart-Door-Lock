from tkinter import *
from twilio.rest import Client
from random import randint
import os
import bluetooth
from time import sleep
import sys
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

import mysql.connector

keypad = Tk()
keypad.title("keypad")
account_sid = 'SECRET'
auth_token = 'SECRET'
client = Client(account_sid, auth_token)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
currentOTP = ""
mydb = mysql.connector.connect(host="localhost", user="root", passwd="Ahmed",database="smartlock")
mycursor = mydb.cursor()

mycursor.execute("select * from users;")
for i in mycursor:
    print(i)

def click(num):
    global operator
    global passcode
    global message
    if (num == -1):
        passcode = int(operator)
        print(passcode)
        message = "Thank You, Please Enter The OTP"
        labelText.set(message)
        otp = client.messages.create(
                              from_='whatsapp:+141SECRET',
                              body='Your SDL OTP is: '+randomOTP(),
                              to='whatsapp:+966SECRET'
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
            GPIO.output(12, 1)
            sleep(5)
            GPIO.output(12, 0)
        else:
            message = "OTP Is Wrong"
            labelText.set(message)
    elif (num == -4):
        try:
            reader = SimpleMFRC522()
            print("Hold a tag near the reader")
            id, text = reader.read()
            print("ID: %s\nUser Is: %s" % (id,text))
            GPIO.output(12, 1)
            sleep(5)
            tag = str(id)
            mycursor.execute("select username , name from users WHERE rfid = "+tag+";")
            for i in mycursor:
                print(i)
            sleep(5)    
            GPIO.output(12, 0)
        
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
input = StringVar()
labelText = StringVar()
labelText.set(message)
passcode = 0
x = Label(keypad, textvariable=labelText, font=('times new roman',15,'bold'), justify='center').grid(row=0, column=0, columnspan=3)
display = Entry(keypad, bd=2, font=('times new roman',20,'bold'), fg='black', justify='center', textvariable=input).grid(row=1, column=0, columnspan=3)
btn1 = Button(keypad,command=lambda:click(1), padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='1').grid(row=2,column=0)
btn2 = Button(keypad,command=lambda:click(2), padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='2').grid(row=2,column=1)
btn3 = Button(keypad,command=lambda:click(3), padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='3').grid(row=2,column=2)
btn4 = Button(keypad,command=lambda:click(4), padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='4').grid(row=3,column=0)
btn5 = Button(keypad,command=lambda:click(5), padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='5').grid(row=3,column=1)
btn6 = Button(keypad,command=lambda:click(6), padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='6').grid(row=3,column=2)
btn7 = Button(keypad,command=lambda:click(7), padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='7').grid(row=4,column=0)
btn8 = Button(keypad,command=lambda:click(8), padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='8').grid(row=4,column=1)
btn9 = Button(keypad,command=lambda:click(9), padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='9').grid(row=4,column=2)
btn0 = Button(keypad,command=lambda:click(0), padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='0').grid(row=5,column=1)
btnClear = Button(keypad,command=lambda:click(-2), padx=16, pady=16, fg='black',font=('times new roman',15,'bold'), text='Clear').grid(row=5,column=0)
btnOTP = Button(keypad,command=lambda:click(-3), padx=8, pady=8, fg='black',font=('times new roman',15,'bold'), text='OTP').grid(row=5,column=2)
btnEnter = Button(keypad,command=lambda:click(-1), padx=8, pady=8, fg='black',font=('times new roman',15,'bold'), text='Enter').grid(row=6,column=1)
btnRFID = Button(keypad,command=lambda:click(-4), padx=8, pady=8, fg='black',font=('times new roman',15,'bold'), text='RFID').grid(row=6,column=0)
btnBLE = Button(keypad,command=lambda:click(-5), padx=8, pady=8, fg='black',font=('times new roman',15,'bold'), text='Bluetooth').grid(row=6,column=2)

keypad.mainloop()

