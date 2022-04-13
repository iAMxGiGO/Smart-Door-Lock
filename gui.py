from tkinter import *
keypad = Tk()
keypad.title("keypad")
operator = ""
message = "Enter Your 6 Digit Passcode"
input = StringVar()
labelText = StringVar()
labelText.set(message)
x = Label(keypad, textvariable=labelText, font=('times new roman',15,'bold'), justify='center').grid(row=0, column=0, columnspan=3)
display = Entry(keypad, bd=10, font=('times new roman',20,'bold'), fg='black', justify='left', textvariable=input).grid(row=1, column=0, columnspan=3)
btn1 = Button(keypad, padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='1').grid(row=2,column=0)
btn2 = Button(keypad, padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='2').grid(row=2,column=1)
btn3 = Button(keypad, padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='3').grid(row=2,column=2)
btn4 = Button(keypad, padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='4').grid(row=3,column=0)
btn5 = Button(keypad, padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='5').grid(row=3,column=1)
btn6 = Button(keypad, padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='6').grid(row=3,column=2)
btn7 = Button(keypad, padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='7').grid(row=4,column=0)
btn8 = Button(keypad, padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='8').grid(row=4,column=1)
btn9 = Button(keypad, padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='9').grid(row=4,column=2)
btn0 = Button(keypad, padx=16, pady=16, fg='black',font=('times new roman',30,'bold'), text='0').grid(row=5,column=1)
btnClear = Button(keypad, padx=19, pady=40, fg='black',font=('times new roman',12,'bold'), text='Clear').grid(row=5,column=0)
btnOTP = Button(keypad, padx=21, pady=40, fg='black',font=('times new roman',12,'bold'), text='OTP').grid(row=5,column=2)
btnEnter = Button(keypad, padx=18, pady=16, fg='black',font=('times new roman',12,'bold'), text='Enter').grid(row=6,column=0, columnspan=3)


keypad.mainloop()

