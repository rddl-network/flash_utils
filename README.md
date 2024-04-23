# flash_utils

This repository contains basic tools to flash devices with RDDL Network compatible firmware.

Please download supported firmware from 
https://github.com/rddl-network/Tasmota/releases

and run the bash script ```./rddl_esp_flasher.sh``` with the type of the target MCU that you want to flash, the firmware file .bin, e.g.

```
./rddl_esp_flasher.sh esp32c3 firmware.bin
``` 

Firmware with pre-attested machine IDs to interact with the RDDL Network can be retrieved from

https://testnet-ta.rddl.io/firmware/esp32
and
https://testnet-ta.rddl.io/firmware/esp32c3
