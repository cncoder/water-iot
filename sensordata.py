import time,sys
import grovepi
import senderror
from grove_rgb_lcd import *

# Connect the Grove Temperature Sensor to analog port A0
# SIG,NC,VCC,GND
tempsensor = 0

# Connect the Moisture sensor to analog port A1
# SIG,NC,VCC,GND
moisturesensor = 1

# Connect the Grove Light Sensor to analog port A2
# SIG,NC,VCC,GND
light_sensor = 2
grovepi.pinMode(light_sensor,"INPUT")

#setRGB(255,255,187)

if sys.platform == 'uwp':
    import winrt_smbus as smbus
    bus = smbus.SMBus(1)
else:
    import smbus
    import RPi.GPIO as GPIO
    rev = GPIO.RPI_REVISION
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)

# this device has two I2C addresses
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

# set backlight to (R,G,B) (values from 0..255 for each)
def setRGB(r,g,b):
    bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
    bus.write_byte_data(DISPLAY_RGB_ADDR,3,g)
    bus.write_byte_data(DISPLAY_RGB_ADDR,2,b)

# send command to display (no need for external use)
def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

# set display text \n for second line(or auto wrap)
def setText(text):
    textCommand(0x01) # clear display
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

#Update the display without erasing the display
def setText_norefresh(text):
    textCommand(0x02) # return home
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    while len(text) < 32: #clears the rest of the screen
        text += ' '
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

# Get all sensor data, and return sensordata['temp'],['mois'],['light']
def getSensorData():
    mosfet = 6
    while True:
        sensordata = {}
        try:
            # temp
            temp = grovepi.temp(tempsensor,'1.2')
            #print("temp =", temp)
            temp = float('%.1f' %(temp))
            sensordata["temp"] = temp

            #Moisture
            moisture = grovepi.analogRead(moisturesensor)
            #print(moisture)
            sensordata["mois"] = moisture
            # Get grovepi sensor value
            sensor_value = grovepi.analogRead(light_sensor)
            sensordata["light"] = sensor_value

            # Calculate resistance of sensor in K
            resistance = (float)(1023 - sensor_value) * 10 / sensor_value
            
            '''
            if moisture < 10:
                grovepi.analogWrite(6,255)
                print ("full speed")
                #sensordata["state"] = "on"
            else:
                grovepi.analogWrite(6,0)
                sensordata["state"] = "off"
                #print ("off")
            '''

            print("sensor_value = %d resistance =%.2f" %(sensor_value,  resistance))
            #setText("Temp  Mois light\n%.2f  %d    %d" %(temp, moisture, sensor_value))
            setText_norefresh("Mois Temp  light{}   {}   {}".format(str(moisture),str(temp),str(sensor_value)))
            time.sleep(.5)
            return sensordata

        except KeyboardInterrupt:
            grovepi.analogWrite(mosfet,0)
            break
        except TypeError:

            REPORTER = "Please power off your raspberry3, and start it again!"
            print("The raspberry is overcurrent >>>>>")
            print(REPORTER)
            senderror.wechatreporter("Raspberry3 overcurrent",REPORTER)
            break
        except IOError:
            grovepi.analogWrite(mosfet,0)
            print ("Error")