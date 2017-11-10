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

# (just for Real environment) import grovepi
import time

def ctl(mosi,threshold):
    # Connect the Grove MOSFET to analog port D6
    # SIG,NC,VCC,GND
    relay = 6

    if mosi <= threshold:
        # switch on for 1 seconds
        # (just for Real environment) grovepi.digitalWrite(relay,1)
        print ("on")
        time.sleep(1.5)
        # (just for Real environment) grovepi.digitalWrite(relay,0)
        return 1
    else:
        # (just for Real environment) grovepi.digitalWrite(relay,0)
        print ("off")
        time.sleep(1)
        return 0