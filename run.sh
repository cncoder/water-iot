#!/bin/bash

## Running this script, and init demo. & Running Monitor...

cd /home/pi/water-flower-pythonfile
list="baidu.com"

if ping -c1 ${list} >/dev/null;then
    echo  $date:'Internet normally'
    python ThingShadowEcho.py &
else
    echo  $date:'Bad networking'
    python LcdBadNetworking.py
    python offlineDevice.py &
fi
sleep 30

echo $date:"Init Monitor..."
while true
do
    if ! ps -ef | grep ThingShadowEcho | grep -v grep >/dev/null ;then
        echo $date:"Need to run Script"
        if ping -c1 ${list} >/dev/null;then
            echo  $date:'Internet normally'
            if ps -ef | grep offlineDevice | grep -v grep >/dev/null ;then
                ps -ef | grep offlineDevice | awk '{print $2}' | xargs kill -9
            fi
            python ThingShadowEcho.py &
        else
            echo  $date:'Bad networking'
            if ! ps -ef | grep offlineDevice | grep -v grep >/dev/null ;then    
                    python LcdBadNetworking.py
                    python offlineDevice.py &
            fi
        fi
    else
        echo $date:"Alread Running!"
    fi
    sleep 20
done
