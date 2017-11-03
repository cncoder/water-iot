import grovepi
import time

def ctl(mosi,threshold):
    # Connect the Grove MOSFET to analog port D6
    # SIG,NC,VCC,GND
    relay = 6

    if mosi < threshold:
        # switch on for 1 seconds
        grovepi.digitalWrite(relay,1)
        print ("on")
        time.sleep(1)
        grovepi.digitalWrite(relay,0)
        time.sleep(5)
        return 1
    else:
        grovepi.digitalWrite(relay,0)
        print ("off")
        time.sleep(1)
        return 0