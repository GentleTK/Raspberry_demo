import RPi.GPIO as GPIO
import yagmail
#Web GPIO set
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)
while True:
    if GPIO.input(4) == 0:
        yag = yagmail.SMTP(user = '1144626145@qq.com', password = 'vrcbsrxuyclyhaji', host = 'smtp.qq.com')
        yag.send(to = ['17352623503@163.com'],subject = 'GPS Info',contents = ['GPS Coordinate','/home/pi/GPS_Info.csv'])