# esp-idf-can2http
CANbus to http bridge using esp32.   
It's purpose is to be a bridge between a CAN-Bus and a HTTP-Server.    

![slide0001](https://user-images.githubusercontent.com/6020549/125031346-7ae6ec80-e0c7-11eb-8d8a-f419154d277c.jpg)
![slide0002](https://user-images.githubusercontent.com/6020549/125031353-7d494680-e0c7-11eb-8382-df74fab44737.jpg)
![slide0003](https://user-images.githubusercontent.com/6020549/125031358-7e7a7380-e0c7-11eb-9880-07c42a1a7d64.jpg)


# Software requirement
ESP-IDF V4.4/V5.x.   
ESP-IDF V5.1 is required when using ESP32C6.   

# Hardware requirements
- SN65HVD23x CAN-BUS Transceiver   
SN65HVD23x series has 230/231/232.   
They differ in standby/sleep mode functionality.   
Other features are the same.   

- Termination resistance   
I used 150 ohms.   

# Wireing   
|SN65HVD23x||ESP32|ESP32-S2/S3|ESP32-C3/C6||
|:-:|:-:|:-:|:-:|:-:|:-:|
|D(CTX)|--|GPIO21|GPIO17|GPIO0|(*1)|
|GND|--|GND|GND|GND||
|Vcc|--|3.3V|3.3V|3.3V||
|R(CRX)|--|GPIO22|GPIO18|GPIO1|(*1)|
|Vref|--|N/C|N/C|N/C||
|CANL|--||||To CAN Bus|
|CANH|--||||To CAN Bus|
|RS|--|GND|GND|GND|(*2)|

(*1) You can change using menuconfig. But it may not work with other GPIOs.  

(*2) N/C for SN65HVD232



# Test Circuit   
```
   +-----------+   +-----------+   +-----------+ 
   | Atmega328 |   | Atmega328 |   |   ESP32   | 
   |           |   |           |   |           | 
   | Transmit  |   | Receive   |   | 21    22  | 
   +-----------+   +-----------+   +-----------+ 
     |       |      |        |       |       |   
   +-----------+   +-----------+     |       |   
   |           |   |           |     |       |   
   |  MCP2515  |   |  MCP2515  |     |       |   
   |           |   |           |     |       |   
   +-----------+   +-----------+     |       |   
     |      |        |      |        |       |   
   +-----------+   +-----------+   +-----------+ 
   |           |   |           |   | D       R | 
   |  MCP2551  |   |  MCP2551  |   |   VP230   | 
   | H      L  |   | H      L  |   | H       L | 
   +-----------+   +-----------+   +-----------+ 
     |       |       |       |       |       |   
     +--^^^--+       |       |       +--^^^--+
     |   R1  |       |       |       |   R2  |   
 |---+-------|-------+-------|-------+-------|---| BackBorn H
             |               |               |
             |               |               |
             |               |               |
 |-----------+---------------+---------------+---| BackBorn L

      +--^^^--+:Terminaror register
      R1:120 ohms
      R2:150 ohms(Not working at 120 ohms)
```

__NOTE__   
3V CAN Trasnceviers like VP230 are fully interoperable with 5V CAN trasnceviers like MCP2551.   
Check [here](http://www.ti.com/lit/an/slla337/slla337.pdf).


# Installation
```
git clone https://github.com/nopnop2002/esp-idf-can2http
cd esp-idf-can2http
idf.py set-target {esp32/esp32s2/esp32s3/esp32c3/esp32c6}
idf.py menuconfig
idf.py flash
```

# Configuration
![config-main](https://user-images.githubusercontent.com/6020549/123870635-92a6ce00-d96d-11eb-9b67-7b6a26e95fbd.jpg)
![config-app](https://user-images.githubusercontent.com/6020549/123870638-94709180-d96d-11eb-94da-b4860148be6a.jpg)

## CAN Setting
![config-can](https://user-images.githubusercontent.com/6020549/160263252-f2a10f2b-a970-44bf-ab9c-22ae7baa4ab5.jpg)

## WiFi Setting
![config-wifi-1](https://user-images.githubusercontent.com/6020549/125028704-73254900-e0c3-11eb-9a44-25482d7a08be.jpg)

You can use static IP.   
![config-wifi-2](https://user-images.githubusercontent.com/6020549/125028738-80423800-e0c3-11eb-984f-9dc4f892bdb6.jpg)

You can connect using mDNS.   
![config-wifi-3](https://user-images.githubusercontent.com/6020549/125028763-89cba000-e0c3-11eb-921d-9baca5ec58d4.jpg)

## External HTTP Server Setting   
The External HTTP Server receives CAN Bus received data.   
![config-http](https://user-images.githubusercontent.com/6020549/160263251-1b1a4771-a5f0-43f2-b75e-572fa6904ac9.jpg)

__Note__   
The Built-in HTTP Server receives CAN Bus transmittion data.   

# Definition from CANbus to HTTP
When CANbus data is received, it is sent by HTTP POST according to csv/can2http.csv.   
The file can2http.csv has three columns.   
In the first column you need to specify the CAN Frame type.   
The CAN frame type is either S(Standard frame) or E(Extended frame).   
In the second column you have to specify the CAN-ID as a __hexdecimal number__.    
In the last column you have to specify the HTTP-POST-Path of external HTTP server.   
Each CAN-ID is allowed to appear only once in the whole file.   

```
S,101,/post
E,101,/post
S,103,/post
E,103,/post
```

When a CAN frame with ID 0x101 is received, POST with the 'canid':257.   
When a CAN frame with ID 0x103 is received, POST with the 'canid':259.   

POST Parameter Example:  
CAN-ID is a decimal number, not a hexadecimal number.   

```
{"canid":257, "frame": "standard", "data": [16, 17, 18]}
{"canid":257, "frame": "extended", "data": [16, 17, 18]}
{"canid":259, "frame": "standard", "data": [16, 17, 18]}
{"canid":259, "frame": "extended", "data": [16, 17, 18]}
```

__CAN messages not registered in csv/can2http.csv are discarded and not POSTed to HTTP.__

# Definition from HTTP to CANbus
Not exist.   
You can send any CAN-ID.   


# Send CANBus frame using curl   
CAN-ID is specified in __decimal number__.   
```
$ curl -X POST -H "Content-Type: application/json" -d '{"canid": 513, "frame": "standard", "data": [16, 17, 18]}' http://esp32-server.local:8000/api/twai/send
twai send successfully

$ curl -X POST -H "Content-Type: application/json" -d '{"canid": 513, "frame": "extended", "data": [16, 17, 18]}' http://esp32-server.local:8000/api/twai/send
twai send successfully
```

CANBus reception using UNO.

![send_standard](https://user-images.githubusercontent.com/6020549/125029834-2c385300-e0c5-11eb-8f25-f3af82e90038.jpg)

![send_extended](https://user-images.githubusercontent.com/6020549/125029930-5558e380-e0c5-11eb-951b-baee58e66d18.jpg)


---

# HTTP Server Using Tornado
```
cd $HOME
sudo apt install python3-pip python3-setuptools
python3 -m pip install -U pip
python3 -m pip install -U wheel
python3 -m pip install tornado
git clone https://github.com/nopnop2002/esp-idf-can2http
cd esp-idf-can2http
cd tornado
python3 can.py
```

You can specify the number of lines to display and the port number.   
The default port number is 8000 and the default number of display lines is 20.   
Redisplay every 5 seconds.   
![can2http-tornado](https://user-images.githubusercontent.com/6020549/202159913-74fab7ef-d95c-4774-8432-ceceac24af4e.jpg)


# HTTP Server Using Flask
```
cd $HOME
sudo apt install python3-pip python3-setuptools
python3 -m pip install -U pip
python3 -m pip install -U wheel
python3 -m pip install -U Werkzeug
python3 -m pip install flask
git clone https://github.com/nopnop2002/esp-idf-can2http
cd esp-idf-can2http
cd flask
python3 can.py
```

You can specify the number of lines to display and the port number.   
The default port number is 8000 and the default number of display lines is 20.   
Redisplay every 5 seconds.   
![can2http-flask](https://user-images.githubusercontent.com/6020549/202165156-dea58ea4-cbb8-4e35-bdc8-a19e5be575e7.jpg)


# Brows received data Using Tornado/Flask   
Open your browser and put the Server's IP in the address bar.   

![can2http-browser](https://user-images.githubusercontent.com/6020549/202160043-0ca6e869-f6bc-4319-b8db-48a8fe9b1c5f.jpg)

# Visualize CAN-Frame

## Using python
There is a lot of information on the internet about the Python + visualization library.   
- [matplotlib](https://matplotlib.org/)
- [seaborn](https://seaborn.pydata.org/index.html)
- [bokeh](https://bokeh.org/)
- [plotly](https://plotly.com/python/)

## Using node.js
There is a lot of information on the internet about the node.js + __real time__ visualization library.   
- [epoch](https://epochjs.github.io/epoch/real-time/)
- [plotly](https://plotly.com/javascript/streaming/)
- [chartjs-plugin-streaming](https://nagix.github.io/chartjs-plugin-streaming/1.9.0/)

# Troubleshooting   
There is a module of SN65HVD230 like this.   
![SN65HVD230-1](https://user-images.githubusercontent.com/6020549/80897499-4d204e00-8d34-11ea-80c9-3dc41b1addab.JPG)

There is a __120 ohms__ terminating resistor on the left side.   
![SN65HVD230-22](https://user-images.githubusercontent.com/6020549/89281044-74185400-d684-11ea-9f55-830e0e9e6424.JPG)

I have removed the terminating resistor.   
And I used a external resistance of __150 ohms__.   
A transmission fail is fixed.   
![SN65HVD230-33](https://user-images.githubusercontent.com/6020549/89280710-f7857580-d683-11ea-9b36-12e36910e7d9.JPG)

If the transmission fails, these are the possible causes.   
- There is no receiving app on CanBus.
- The speed does not match the receiver.
- There is no terminating resistor on the CanBus.
- There are three terminating resistors on the CanBus.
- The resistance value of the terminating resistor is incorrect.
- Stub length in CAN bus is too long. See [here](https://e2e.ti.com/support/interface-group/interface/f/interface-forum/378932/iso1050-can-bus-stub-length).

# Reference
https://github.com/nopnop2002/esp-idf-candump

https://github.com/nopnop2002/esp-idf-can2mqtt

https://github.com/nopnop2002/esp-idf-can2usb

https://github.com/nopnop2002/esp-idf-can2websocket

https://github.com/nopnop2002/esp-idf-can2socket

https://github.com/nopnop2002/esp-idf-CANBus-Monitor

