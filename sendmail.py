import yagmail
yag = yagmail.SMTP(user = '1144626145@qq.com', password = 'vrcbsrxuyclyhaji', host = 'smtp.qq.com')
yag.send(to = ['17352623503@163.com'],subject = 'GPS Info',contents = ['GPS Coordinate','/home/pi/GPS_Info.csv'])