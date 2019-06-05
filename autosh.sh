sudo python /home/pi/Raspberry_demo/inquiry-with-rssi.py
sleep 1m
echo "GPS Coordinate" | mutt 17352623503@163.com -s "GPS Info" -a /home/pi/GPS_Info.csv
