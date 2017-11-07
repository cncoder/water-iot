By connecting their devices to AWS IoT, users can securely work with the message broker, rules, and the device shadow (sometimes referred to as a thing shadow) provided by AWS IoT and with other AWS services like AWS Lambda, Amazon Kinesis, Amazon S3, and more.

### prepare

#### Register a Device in the Thing Registry

In this demo, your must create Thing that name is "waterflower"
http://docs.aws.amazon.com/iot/latest/developerguide/register-device.html

#### Create and Activate a Device Certificate

http://docs.aws.amazon.com/iot/latest/developerguide/create-device-certificate.html

#### Create an AWS IoT Policy

http://docs.aws.amazon.com/iot/latest/developerguide/create-iot-policy.html

#### Attach an AWS IoT Policy to a Device Certificate

http://docs.aws.amazon.com/iot/latest/developerguide/attach-policy-to-certificate.html

#### Attach a Certificate to a Thing

http://docs.aws.amazon.com/iot/latest/developerguide/attach-cert-thing.html

### Configure Your Device

Install Driver for sensor

> sudo curl -kL dexterindustries.com/update_grovepi | bash

> pip install AWSIoTPythonSDK

And then reboot the raspberry

> git clone git@github.com:cncoder/water-iot.git

### Input your credentials for authentication(ThinsShadowEcho.py)
endpoint = "XXXX.iot.XXXX.amazonaws.com" (BJS will be diff)
rootCAPath = "cert/rootCA.cert"
certificatePath = "cert/certificate.pem"
privateKeyPath = "cert/private.pem.key"
thingName = "waterflower"

if your don't want to report error with wechat, you must set the **senderror.py** file:
    > reporter = true
    & change WECHAT_URL with https://sc.ftqq.com/3.version

### Main function:

> run.sh

Must be change in the code:

### sensordata

if your just want to run this demo without sensor, you can return random sensor data in sensordata.py

### Device state

if your have LCD , please insert it on the I2C port.

If the LCD show in blue color, it is starting now.

If the LCD show in red color, your must shutdown the raspberry(must be power off), and power on again.

<img src="https://raw.githubusercontent.com/cncoder/water-iot/master/static/demo-web.jpg" height="800" alt="demo"/>

### Licensed under the Apache License, Version 2.0 (the "License").