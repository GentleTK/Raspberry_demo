from gps import *
import time
session = gps(mode=WATCH_ENABLE)
try:
    while True:
        report = session.next()
        if report['class'] == 'VERSION':
            print 'connect GPS successfully'
        if report['class'] == 'DEVICES':
            print 'searching satellite...'
        if report['class'] == 'WATCH':
            print 'search satellite successfully'
        if report['class'] == 'TPV':
            print 'Latitude:  ',report.lat
            print 'Longitude: ',report.lon
        if report['class'] == 'SKY':
            print 'satellites NO.',len(report.satellites)
        time.sleep(3)
except StopIteration:
            print "GPSD has teminated"