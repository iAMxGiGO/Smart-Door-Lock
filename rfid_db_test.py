from time import sleep
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
import mysql.connector
#connect to database
mydb = mysql.connector.connect(host="localhost", user="root", passwd="Ahmed",database="smartlock")
mycursor = mydb.cursor()
#print all records in the user table from database
mycursor.execute("select * from users;")
for i in mycursor:
    print(i)

try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print("ID: %s\nUser Is: %s" % (id,text))
        sleep(5)
        tag = str(id)
        #search for the scanned rfid tag id in the user table
		mycursor.execute("select username , name from users WHERE rfid = "+tag+";")
        #print results of the search
		for i in mycursor:
            print(i)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise
