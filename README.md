# esp-idf-can2http
CANbus to http bridge using esp32.   
It's purpose is to be a bridge between a CAN-Bus and a HTTP-Server.    

I inspired from [here](https://github.com/c3re/can2mqtt).

![esp-idf-can2http](https://user-images.githubusercontent.com/6020549/123870583-773bc300-d96d-11eb-8c07-27747faf7bb4.jpg)


# Software requirement
esp-idf v4.2-dev-2243 or later.   
Use twai(Two-Wire Automotive Interface) driver instead of can driver.   

# Hardware requirements
1. SN65HVD23x CAN-BUS Transceiver   

|SN65HVD23x||ESP32|ESP32-S2||
|:-:|:-:|:-:|:-:|:-:|
|D(CTX)|--|GPIO21|GPIO20|(*1)|
|GND|--|GND|GND||
|Vcc|--|3.3V|3.3V||
|R(CRX)|--|GPIO22|GPIO21|(*1)|
|Vref|--|N/C|N/C||
|CANL|--|||To CAN Bus|
|CANH|--|||To CAN Bus|
|RS|--|GND|GND|(*2)|

(*1) You can change using menuconfig.

(*2) N/C for SN65HVD232

2. Termination resistance   
I used 150 ohms.   


# Test Circuit   
```
   +-----------+ +-----------+ +-----------+ 
   | Atmega328 | | Atmega328 | |   ESP32   | 
   |           | |           | |           | 
   | Transmit  | | Receive   | | 21    22  | 
   +-----------+ +-----------+ +-----------+ 
     |       |    |        |     |       |   
   +-----------+ +-----------+   |       |   
   |           | |           |   |       |   
   |  MCP2515  | |  MCP2515  |   |       |   
   |           | |           |   |       |   
   +-----------+ +-----------+   |       |   
     |      |      |      |      |       |   
   +-----------+ +-----------+ +-----------+ 
   |           | |           | | D       R | 
   |  MCP2551  | |  MCP2551  | |   VP230   | 
   | H      L  | | H      L  | | H       L | 
   +-----------+ +-----------+ +-----------+ 
     |       |     |       |     |       |   
     +--^^^--+     |       |     +--^^^--+
     |   R1  |     |       |     |   R2  |   
 |---+-------|-----+-------|-----+-------|---| BackBorn H
             |             |             |
             |             |             |
             |             |             |
 |-----------+-------------+-------------+---| BackBorn L

      +--^^^--+:Terminaror register
      R1:120 ohms
      R2:150 ohms(Not working at 120 ohms)
```

__NOTE__   
3V CAN Trasnceviers like VP230 are fully interoperable with 5V CAN trasnceviers like MCP2551.   
Check [here](http://www.ti.com/lit/an/slla337/slla337.pdf).


# Installation for ESP32
```
git clone https://github.com/nopnop2002/esp-idf-can2http
cd esp-idf-can2htp
idf.py set-target esp32
idf.py menuconfig
idf.py flash
```

# Installation for ESP32-S2
```
git clone https://github.com/nopnop2002/esp-idf-can2http
cd esp-idf-can2http
idf.py set-target esp32s2
idf.py menuconfig
idf.py flash
```

# Configuration
![config-main](https://user-images.githubusercontent.com/6020549/123870635-92a6ce00-d96d-11eb-9b67-7b6a26e95fbd.jpg)
![config-app](https://user-images.githubusercontent.com/6020549/123870638-94709180-d96d-11eb-94da-b4860148be6a.jpg)

## CAN Setting
![config-can](https://user-images.githubusercontent.com/6020549/123870665-a05c5380-d96d-11eb-89b1-78a274bfd957.jpg)

## WiFi Setting
![config-wifi](https://user-images.githubusercontent.com/6020549/123870681-a81bf800-d96d-11eb-8637-66295408b055.jpg)

## HTTP Server Setting
![config-http](https://user-images.githubusercontent.com/6020549/123870716-b702aa80-d96d-11eb-8954-6ca365e78639.jpg)

# Definition from CANbus to HTTP
When CANbus data is received, it is sent by HTTP according to csv/can2http.csv.   
The file can2http.csv has three columns.   
In the first column you need to specify the CAN Frame type.   
The CAN frame type is either S(Standard frame) or E(Extended frame).   
In the second column you have to specify the CAN-ID as a __hexdecimal number__.    
In the last column you have to specify the HTTP-Path.   
Each CAN-ID and each HTTP-Path is allowed to appear only once in the whole file.   

```
S,101,/post
E,101,/post
S,103,/post
E,103,/post
```

When a Standard CAN frame with ID 0x101 is received, it is POST by PATH of "/post".   
When a Extended CAN frame with ID 0x101 is received, it is POST by PATH of "/post".   
http://{HTTP-Server-IP}:{HTTP-Server-Port}/post/{CAN-Data}

# HTTP Server Using Tornado
```
sudo apt install python3-pip python3-setuptools python3-magic
python -m pip install -U pip
python -m pip install -U wheel
python -m pip install tornado
cd tornado
python can.py
```
![can2http-tornado](https://user-images.githubusercontent.com/6020549/123871778-18774900-d96f-11eb-95b6-df9713047c30.jpg)

# HTTP Server Using Flask
```
sudo apt install python3-pip python3-setuptools python3-magic
python -m pip install -U pip
python -m pip install -U wheel
python -m pip install -U Werkzeug
python -m pip install flask
cd flask
python can.py
```

![can2http-flask](https://user-images.githubusercontent.com/6020549/123871850-35ac1780-d96f-11eb-9d03-c1a0b547e9c8.jpg)


# List data Using Brouser
Open your browser and put the IP address in the address bar.   

![can2http-browser](https://user-images.githubusercontent.com/6020549/123872025-71df7800-d96f-11eb-8832-8d9e1169c993.jpg)

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

