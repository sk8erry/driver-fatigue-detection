import gps
import RPi.GPIO as GPIO
import time
import os

time.sleep(20)
print "sleep time over"
os.system("sudo killall gpsd")
print "sudo killall gpsd executed"
os.system("sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock")
print "gpsd restarted"
# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

 
while True:
    print "code is here"
    try:
        report = session.next()
        # Wait for a 'TPV' report and display the current time
        # To see all report data, uncomment the line below
        # print report
        if report['class'] == 'TPV':
            if hasattr(report, 'speed'):
                #print report.speed
                if report.speed > 15:
                    GPIO.setmode(GPIO.BCM)
                    GPIO.setwarnings(False)
                    GPIO.setup(18,GPIO.OUT)
                    GPIO.output(18,GPIO.HIGH)
                else:
                    GPIO.setmode(GPIO.BCM)
                    GPIO.setwarnings(False)
                    GPIO.setup(18,GPIO.OUT)
                    GPIO.output(18,GPIO.LOW)
                    
                        
                    

    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
        print "GPSD has terminated"
