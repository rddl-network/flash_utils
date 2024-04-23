# Flash Utils

This repository contains basic tools to flash devices with RDDL Network compatible firmware.

Please download supported firmware from 
https://github.com/rddl-network/Tasmota/releases

## Requirements
Set up a virtual python environment and activate it

```
virtualenv .venv
source .venv/bin/activate
``` 
Install the required python packages.
```
pip install -r requirements.txt
``` 

## Getting a pre-attested RDDL-Network firmware
A firmware with a pre-attested machine ID to interact with the RDDL Network can be retrieved from

https://testnet-ta.rddl.io/firmware/esp32
and
https://testnet-ta.rddl.io/firmware/esp32c3

## Flashing ESP32 or ESP32-C3
Now, you can execute the script ```./rddl_esp_flasher.sh``` with the type of the target MCU that you want to flash and the firmware file (.bin) as parameters, e.g.

```
./rddl_esp_flasher.sh esp32c3 firmware.bin
``` 

## UI
A small UI delegating thought the potential configuration can be used by executing

```
python main.py
```
