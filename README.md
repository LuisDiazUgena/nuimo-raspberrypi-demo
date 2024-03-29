# Nuimo Python script for Raspberry Pi
Python script demonstrating the communication with Nuimo on a Raspberry Pi

## Installation

### 1. Install bluez library

The [bluez library](http://www.bluez.org/) will be used to enable your Bluetooth dongle. It also provides tools to manually interact with Bluetooth Low Energy (BLE) devices.

1. `sudo apt-get install --no-install-recommends bluetooth` (Installs bluez)
2. `sudo hciconfig hci0 up` (Enables your Bluetooth dongle)
3. `sudo hcitool lescan` (Should discover your Nuimo, press Ctrl+C to stop discovery)

##### Manually connect to Nuimo with bluez (optional, skip this step if you are not interested)

1. `sudo hcitool lescan | grep Nuimo` (Copy your Nuimo's MAC address and press Ctrl+C to stop discovery)
2. `sudo gatttool -b FA:48:12:00:CA:AC -t random -I` (Replace the MAC address with the address from step 1)
3. `connect` (Should successfully connect to Nuimo)
4. `char-write-req 1e 0100` (Registers for button click events – press Nuimo's button to test)
5. `exit` to leave `gatttool`

### 2. Install bluepy library

The [bluepy library](https://github.com/IanHarvey/bluepy) is written in Python and will be used to communicate with your Bluetooth dongle in Python scripts.

From your home folder do:

1. `sudo apt-get install build-essential libglib2.0-dev libdbus-1-dev` (Installs build dependencies)
2. `git clone https://github.com/IanHarvey/bluepy.git`
3. `cd bluepy`
4. `python setup.py build` (Compiles files to the `build` folder)
5. `sudo python setup.py install` (Installs bluepy Python scripts and `bluepy-helper` to `/usr/local/lib/python-2.7/dist-packages/bluepy`)
6. `cd ..` (Navigate back to your home folder)

### 3. Download the Nuimo Python script

From your home folder do:

1. `wget https://raw.githubusercontent.com/getsenic/nuimo-raspberrypi-demo/master/nuimo.py` (Downloads `nuimo.py`)
2. `nano nuimo.py` (If you want to modify the Nuimo demo script, Ctrl+X to quit `nano`)

## Run the Nuimo Python script

From your home folder do:

1. `sudo hcitool lescan | grep Nuimo` (Copy your Nuimo's MAC address and press Ctrl+C to stop discovery)
2. `python nuimo.py FA:48:12:00:CA:AC` (Replace the MAC address with the address from step 1)
3. Perform input events on your Nuimo, they will show up on your console

# Support

If you have questions or comments, please visit https://senic.com or shoot us an email to developers@senic.com.
