from gps import *
import os
import sys
import csv
import struct
import yagmail
import bluetooth._bluetooth as bluez
import bluetooth
import RPi.GPIO as GPIO
import time
import math

#System Value
a = 6378245.0
ee = 0.00669342162296594323
x_pi = 3.14159265358979324 * 3000.0 / 180.0;
send_flag = 0
#Bluetooth Device Address
dev_addr = "7C:03:AB:43:ED:D2"
#dev_addr = "48:3C:0C:9D:2E:02"
#GPIO Set
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#Buzzer warning
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.LOW)
#Web GPIO Control
GPIO.setup(4, GPIO.IN)
#GPS session Set
session = gps(mode=WATCH_ENABLE)
#Print Devices Addr and Name
#nearby_devices = bluetooth.discover_devices(lookup_names=True)
#print(" found %d devices" % len(nearby_devices))
#for addr, name in nearby_devices:
#    print("  %s - %s" % (addr, name))

#Bluetooth range distance module
def printpacket(pkt):
    for c in pkt:
        sys.stdout.write("%02x " % struct.unpack("B",c)[0])
    print() 

def read_inquiry_mode(sock):
    """returns the current mode, or -1 on failure"""
    # save current filter
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # Setup socket filter to receive only events related to the
    # read_inquiry_mode command
    flt = bluez.hci_filter_new()
    opcode = bluez.cmd_opcode_pack(bluez.OGF_HOST_CTL, 
            bluez.OCF_READ_INQUIRY_MODE)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    bluez.hci_filter_set_event(flt, bluez.EVT_CMD_COMPLETE);
    bluez.hci_filter_set_opcode(flt, opcode)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

    # first read the current inquiry mode.
    bluez.hci_send_cmd(sock, bluez.OGF_HOST_CTL, 
            bluez.OCF_READ_INQUIRY_MODE )

    pkt = sock.recv(255)

    status,mode = struct.unpack("xxxxxxBB", pkt)
    if status != 0: mode = -1

    # restore old filter
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
    return mode

def write_inquiry_mode(sock, mode):
    """returns 0 on success, -1 on failure"""
    # save current filter
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # Setup socket filter to receive only events related to the
    # write_inquiry_mode command
    flt = bluez.hci_filter_new()
    opcode = bluez.cmd_opcode_pack(bluez.OGF_HOST_CTL, 
            bluez.OCF_WRITE_INQUIRY_MODE)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    bluez.hci_filter_set_event(flt, bluez.EVT_CMD_COMPLETE);
    bluez.hci_filter_set_opcode(flt, opcode)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

    # send the command!
    bluez.hci_send_cmd(sock, bluez.OGF_HOST_CTL, 
            bluez.OCF_WRITE_INQUIRY_MODE, struct.pack("B", mode) )

    pkt = sock.recv(255)

    status = struct.unpack("xxxxxxB", pkt)[0]

    # restore old filter
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
    if status != 0: return -1
    return 0

def device_inquiry_with_with_rssi(sock):
    # save current filter
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # perform a device inquiry on bluetooth device #0
    # The inquiry should last 8 * 1.28 = 10.24 seconds
    # before the inquiry is performed, bluez should flush its cache of
    # previously discovered devices
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

    duration = 4
    max_responses = 255
    cmd_pkt = struct.pack("BBBBB", 0x33, 0x8b, 0x9e, duration, max_responses)
    bluez.hci_send_cmd(sock, bluez.OGF_LINK_CTL, bluez.OCF_INQUIRY, cmd_pkt)

    results = []

    done = False
    while not done:
        pkt = sock.recv(255)
        ptype, event, plen = struct.unpack("BBB", pkt[:3])
        if event == bluez.EVT_INQUIRY_RESULT_WITH_RSSI:
            pkt = pkt[3:]
            nrsp = bluetooth.get_byte(pkt[0])
            for i in range(nrsp):
                addr = bluez.ba2str( pkt[1+6*i:1+6*i+6] )
                rssi = bluetooth.byte_to_signed_int(
                        bluetooth.get_byte(pkt[1+13*nrsp+i]))
                results.append( ( addr, rssi ) )
                #Compare device addr is connected device
                if addr == dev_addr:
                    power = (abs(rssi)-59)/(10*2.0)
                    meter = pow(10, power)
                    print("[%s] RSSI: [%d]" % (addr, rssi))
                    print("Distance: [%.2f]" % meter)
                    if meter > 2:
                        #change GPS coordinate
                        #report = session.next()
                        #if report['class'] == 'TPV':
                        #    y = report.lon
                        #    x = report.lat
                        y = 112.926
                        x = 27.8505
                        #change GPS coordinate
                        loc=wgs2bd(x,y)
                        #write GPS Information to csvfile
                        csvfile = open('GPS_Info.csv','w')
                        nodes = csv.writer(csvfile)
                        nodes.writerow(['lng','lat'])
                        data=[]
                        data.append(['%.4f' % loc[0],'%.4f' % loc[1]])
                        nodes.writerow(data)
                        csvfile.close()
                        #Send GPS Info E-mail
                        yag = yagmail.SMTP(user = '1144626145@qq.com', password = 'vrcbsrxuyclyhaji', host = 'smtp.qq.com')
                        yag.send(to = ['17352623503@163.com'],subject = 'GPS Info',contents = ['GPS Coordinate','/home/pi/GPS_Info.csv'])
                        #buzzer warning
                        GPIO.output(23, GPIO.HIGH)
                        time.sleep(1)
                        GPIO.output(23, GPIO.LOW)
                        time.sleep(1)
                                                                       
        elif event == bluez.EVT_INQUIRY_COMPLETE:
            done = True
        elif event == bluez.EVT_CMD_STATUS:
            status, ncmd, opcode = struct.unpack("BBH", pkt[3:7])
            if status != 0:
                print("uh oh...")
                printpacket(pkt[3:7])
                done = True
        elif event == bluez.EVT_INQUIRY_RESULT:
            pkt = pkt[3:]
            nrsp = bluetooth.get_byte(pkt[0])
            for i in range(nrsp):
                addr = bluez.ba2str( pkt[1+6*i:1+6*i+6] )
                results.append( ( addr, -1 ) )
                print("[%s] (no RRSI)" % addr)
        #else:
        #    print("unrecognized packet type 0x%02x" % ptype)
        #print("event ", event)
        
    # restore old filter
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )

    return results
#GPS Coordinate Change module
#change Longitude
def transformLat(lat,lon):
    ret = -100.0 + 2.0 * lat + 3.0 * lon + 0.2 * lon * lon + 0.1 * lat * lon +0.2 * math.sqrt(abs(lat))
    ret += (20.0 * math.sin(6.0 * lat * math.pi) + 20.0 * math.sin(2.0 * lat * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lon * math.pi) + 40.0 * math.sin(lon / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lon / 12.0 * math.pi) + 320 * math.sin(lon * math.pi  / 30.0)) * 2.0 / 3.0
    return ret
 
#change Latitude
def transformLon(lat,lon):
    ret = 300.0 + lat + 2.0 * lon + 0.1 * lat * lat + 0.1 * lat * lon + 0.1 * math.sqrt(abs(lat))
    ret += (20.0 * math.sin(6.0 * lat * math.pi) + 20.0 * math.sin(2.0 * lat * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * math.pi) + 40.0 * math.sin(lat / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lat / 12.0 * math.pi) + 300.0 * math.sin(lat / 30.0 * math.pi)) * 2.0 / 3.0
    return ret
 
#Wgs transform to gcj
def wgs2gcj(lat,lon):
    dLat = transformLat(lon - 105.0, lat - 35.0)
    dLon = transformLon(lon - 105.0, lat - 35.0)
    radLat = lat / 180.0 * math.pi
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * math.pi)
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * math.pi)
    mgLat = lat + dLat
    mgLon = lon + dLon
    loc=[mgLat,mgLon]
    return loc
 
#gcj transform to bd2
def gcj2bd(lat,lon):
    x=lon
    y=lat
    z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) + 0.000003 * math.cos(x * x_pi)
    bd_lon = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    bdpoint = [bd_lon,bd_lat]
    return bdpoint
 
#wgs transform to bd
def wgs2bd(lat,lon):
    wgs_to_gcj = wgs2gcj(lat,lon)
    gcj_to_bd = gcj2bd(wgs_to_gcj[0], wgs_to_gcj[1])
    return gcj_to_bd;
dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
except:
    print("error accessing bluetooth device...")
    sys.exit(1)

try:
    mode = read_inquiry_mode(sock)
except Exception as e:
    print("error reading inquiry mode.  ")
    print("Are you sure this a bluetooth 1.2 device?")
    print(e)
    sys.exit(1)
print("current inquiry mode is %d" % mode)

if mode != 1:
    print("writing inquiry mode...")
    try:
        result = write_inquiry_mode(sock, 1)
    except Exception as e:
        print("error writing inquiry mode.  Are you sure you're root?")
        print(e)
        sys.exit(1)
    if result != 0:
        print("error while setting inquiry mode")
    print("result: %d" % result)
#try:
while True:
    device_inquiry_with_with_rssi(sock)
    #Web GPIO Control
    if GPIO.input(4) == 0:
        yag = yagmail.SMTP(user = '1144626145@qq.com', password = 'vrcbsrxuyclyhaji', host = 'smtp.qq.com')
        yag.send(to = ['17352623503@163.com'],subject = 'GPS Info',contents = ['GPS Coordinate','/home/pi/GPS_Info.csv'])
#        if report['class'] == 'VERSION':
#            print 'connect GPS successfully'
#        if report['class'] == 'DEVICES':
#            print 'searching satellite...'
#        if report['class'] == 'WATCH':
#             print 'search satellite successfully'
#        if report['class'] == 'SKY':
#            print 'satellites NO.',len(report.satellites)
#        time.sleep(3)
#except StopIteration:
#           print "GPSD has teminated"