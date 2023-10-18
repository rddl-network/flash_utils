# flash_utils

This repository contains basic tools to flash devices with RDDL Network compatible firmwares.

Please download supported firmwares from 
https://github.com/rddl-network/Tasmota/releases

and run the bash script ```./rddl_esp_flasher.sh``` with the type of the target MCU that you want to flash, the firmwaefile .bin, e.g.

```
./rddl_esp_flasher.sh esp32c3 firmware.bin
``` 

Firmware with preattested machine IDs to interact with the RDDL Network can be retrieved from

https://testnet-ta.rddl.io/firmware/esp32
and
https://testnet-ta.rddl.io/firmware/esp32c3
