'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import json
import sensordata
import grovepi
import powerctl

# Connect the Grove RELAY to analog port D6
# SIG,NC,VCC,GND
relay = 6

# relay status
global status
status = 0

# offline Device version

while True:
    try:
        senData = {}
        senData["state"] = {}
        senData["state"]["reported"] = {}
        tempData = sensordata.getSensorData()
        senData["state"]["reported"]['mois'] = tempData['mois']
        senData["state"]["reported"]['temp'] = tempData['temp']
        senData["state"]["reported"]['light'] = tempData['light']
        #print(">>>>>>>>>>")
        #print(senData)
        #senData["state"]["reported"]["status"] = "off"
        status = powerctl.ctl(senData["state"]["reported"]['mois'],20)

        time.sleep(2)

    except KeyboardInterrupt:
        print("key interrput")
    except IOError:
        print ("Error")
    except TypeError, e:
        print(str(e))
        print("TypeError Need reboot?")
    finally:
        grovepi.digitalWrite(relay,0)