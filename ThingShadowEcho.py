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
# import sensordata
import powerctl
# Are you want to Mock data ?
import mocksensordata

'''
/*
* Please import package in Real environment
*/
import grovepi
import setLcdinit
import LcdBadDevice
'''

# Connect the Grove RELAY to analog port D6
# SIG,NC,VCC,GND
relay = 6

# relay status
global status
status = 0

'''
* To do list
* Input your credentials for authentication
'''
endpoint = "XXXX.iot.us-west-2.amazonaws.com"
rootCAPath = "cert/rootCA.cert"
certificatePath = "cert/certificate.pem"
privateKeyPath = "cert/private.pem.key"
thingName = "waterflower"
clientId = "myClientID"
clientId2 = "sensorClientID"
topic = "sensor/data"

class shadowCallbackContainer:

    threshould = 30

    def __init__(self, deviceShadowInstance):
        self.deviceShadowInstance = deviceShadowInstance

    # Custom Shadow callback
    def customShadowCallback_Delta(self, payload, responseStatus, token):
        # payload is a JSON string ready to be parsed using json.loads(...)
        # in both Py2.x and Py3.x
        
        print("Received a delta message:")
        payloadDict = json.loads(payload)
        deltaMessage = json.dumps(payloadDict["state"])
        print("!!!!!!!!!!")
        print(deltaMessage)
        if payloadDict["state"].has_key('threshould'): 
            shadowCallbackContainer.threshould = int(payloadDict["state"]['threshould'])
            print("access to fix threshould =>>>>"+ str(shadowCallbackContainer.threshould))
        print("Request to update the reported state...")
        newPayload = '{"state":{"reported":' + deltaMessage + '}}'
        self.deviceShadowInstance.shadowUpdate(newPayload, None, 5)
        print("Sent.")

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message)

# Shadow MQTT message callback
def getShadowCallback(client, userdata, message):
    print(">>>>>>>>Received a new getShadowCallback message: ")
    print(userdata)
    print(message)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTShadowClient
myAWSIoTMQTTShadowClient = None
myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
myAWSIoTMQTTShadowClient.configureEndpoint(endpoint, 8883)
myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTShadowClient configuration
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT
myAWSIoTMQTTShadowClient.connect()

# Create a deviceShadow with persistent subscription
deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)
shadowCallbackContainer_Bot = shadowCallbackContainer(deviceShadowHandler)

# Listen on deltas
deviceShadowHandler.shadowRegisterDeltaCallback(shadowCallbackContainer_Bot.customShadowCallback_Delta)


# General message notification callback
def customOnMessage(message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


# Suback callback
def customSubackCallback(mid, data):
    print("Received SUBACK packet id: ")
    print(mid)
    print("Granted QoS: ")
    print(data)
    print("++++++++++++++\n\n")


# Puback callback
def customPubackCallback(mid):
    print("Received PUBACK packet id: ")
    print(mid)
    print("++++++++++++++\n\n")

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId2)
myAWSIoTMQTTClient.configureEndpoint(endpoint, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 600, 300)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(600)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.onMessage = customOnMessage

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
# Note that we are not putting a message callback here. We are using the general message notification callback.
myAWSIoTMQTTClient.subscribeAsync(topic, 1, ackCallback=customSubackCallback)

# Publish to the same topic in a loop forever

while True:
    try:
        senData = {}
        senData["state"] = {}
        senData["state"]["reported"] = {}

        # (just for Real environment) tempData = sensordata.getSensorData()
        tempData = mocksensordata.getSensorData()

        senData["state"]["reported"]['mois'] = tempData['mois']
        senData["state"]["reported"]['temp'] = tempData['temp']
        senData["state"]["reported"]['light'] = tempData['light']

        #senData["state"]["reported"]["status"] = "off"
        print("class threshold >>>>"+str(shadowCallbackContainer.threshould))
        new_threshold = shadowCallbackContainer.threshould
        if new_threshold !=30:
            status = powerctl.ctl(senData["state"]["reported"]['mois'],new_threshold)
        else:
            senData["state"]["reported"]['threshould'] = new_threshold
            print("init-threshould"+str('30'))
            status = powerctl.ctl(senData["state"]["reported"]['mois'],30)

        senData["state"]["reported"]["status"] = status
        print(">>>>>>>>>>")
        print(senData)
        deviceShadowHandler.shadowUpdate(json.dumps(senData), customCallback, 5)

        myAWSIoTMQTTClient.publishAsync(topic, json.dumps(senData), 1, ackCallback=customPubackCallback)
        time.sleep(2)

    except KeyboardInterrupt:
        print("key interrput")
        break
    except IOError:
        print ("Error")
    except TypeError, e:
        print(str(e))
        print("TypeError Need reboot?")
        # show red color & remind shutdown
        # (just for Real environment) LcdBadDevice.device_broken()
        break
    finally:
        print ("finally process!")
        # (just for Real environment) grovepi.digitalWrite(relay,0)