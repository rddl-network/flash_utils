#!/bin/bash

# Check if the required binary files are in the same directory as the script
script_dir="$(dirname "$0")"

if [ $# -eq 0 ]; then
    echo "Please indicate what kind of ESP you want to flash. esp32 or esp32c3?"
    exit 1
fi

boot_app0_file="$script_dir/boot_app0.bin"
if [ "$1" == "esp32" ]; then
    echo "The argument is $1."
    bootloader_file="$script_dir/esp32/bootloader.bin"
    partitions_file="$script_dir/esp32/partitions.bin"
    firmware_file="$script_dir/tasmota32-rddl.bin"
    safeboot_file="$script_dir/esp32/tasmota32-safeboot.bin"
elif [ "$1" == "esp32c3" ]; then
    bootloader_file="$script_dir/esp32c3/bootloader.bin"
    partitions_file="$script_dir/esp32c3/partitions.bin"
    firmware_file="$script_dir/tasmota32c3-rddl.bin"
    safeboot_file="$script_dir/esp32c3/tasmota32c3-safeboot.bin"
else
    echo "Please indicate what kind of ESP you want to flash.\esp32 or esp32c3?"
    exit 1
fi


if [ ! -e "$bootloader_file" ] || [ ! -e "$partitions_file" ] || [ ! -e "$firmware_file" ] || [ ! -e "$safeboot_file" ] || [ ! -e "$boot_app0_file" ]; then
    echo "One or more required binary files (bootloader.bin, partitions.bin, tasmota32c3-safeboot.bin or firmware.bin) not found in the same directory as the script. Exiting."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Installing Python..."
    sudo apt-get update
    sudo apt-get install -y python3
else
    echo "Python is already installed."
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip is not installed. Installing pip..."
    sudo apt-get install -y python3-pip
else
    echo "pip is already installed."
fi

# Check if esptool is installed
if ! command -v esptool.py &> /dev/null; then
    echo "esptool is not installed. Installing esptool..."
    pip3 install esptool
else
    echo "esptool is already installed."
fi

# Find ESP Port
output=/tmp/configFile
rm -f $output

# check USB ports
for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev); do
    (
        syspath="${sysdevpath%/dev}"
        devname="$(udevadm info -q name -p $syspath)"
        [[ "$devname" == "bus/"* ]] && exit
        eval "$(udevadm info -q property --export -p $syspath)"
        [[ -z "$ID_SERIAL" ]] && exit
        #echo "/dev/$devname - $ID_SERIAL"

        if [[ $ID_SERIAL == *"Espressif_USB_JTAG"* ]]; then
            echo "Found ESP Device"
            echo "/dev/$devname" | tee -a $output
        fi
    )
done

# Check if Port found
if test -f "$output"; then
	port_path=$(head -n 1 $output)
	rm -f $output
else
	echo "Couldnt find ESP Port"
	# Ask the user for the Esp port
	read -p "Enter the port path of the ESP device (e.g., /dev/ttyUSB0): " port_path
fi

# Run your fatih.py script
esptool.py -p $port_path -b 460800 --before default_reset --after hard_reset --chip auto write_flash --flash_mode dio --flash_size detect --flash_freq=keep 0x0000 "$bootloader_file" 0x8000 "$partitions_file" 0xe000 "$boot_app0_file" 0x10000 "$safeboot_file" 0xe0000 "$firmware_file"