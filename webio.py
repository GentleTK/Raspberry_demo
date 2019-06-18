import RPi.GPIO as GPIO
import yagmail
import time
#Web GPIO set
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

while True:
    #webio = GPIO.input(4)
    #if GPIO.input(4) != webio:
    if GPIO.input(4) == 1:
        yag = yagmail.SMTP(user = '1144626145@qq.com', password = 'vrcbsrxuyclyhaji', host = 'smtp.qq.com')
        yag.send(to = ['17352623503@163.com'],subject = 'GPS Info',contents = ['GPS Coordinate','/home/pi/MarkPoint.html'])
        print ("OK")
