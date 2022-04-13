from time import sleep
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print("ID: %s\nUser Is: %s" % (id,text))
        sleep(5)
        tag = str(id)
		print("The RFID tag is: "+tag)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise
