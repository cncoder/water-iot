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
 
from grove_rgb_lcd import *

import os
import re

def valid_ip(ip):
    if ("255" in ip) or ( ip == "127.0.0.1") or ( ip == "0.0.0.0" ):
        return False
    else:
        return True

def get_ip(valid_ip):
    ipss = ''.join(os.popen("ifconfig").readlines())
    match = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    ips = re.findall(match, ipss, flags=re.M)
    ip = filter(valid_ip, ips)
    return ''.join(ip)

ip_addr = get_ip(valid_ip)
print ip_addr

setText("Bad networking\n"+str(ip_addr))
setRGB(0,128,64)

time.sleep(3)

setRGB(0,0,0)