from bluepy.bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEException
import struct
import sys

# Characteristic UUIDs
BATTERY_VOLTAGE_CHARACTERISTIC    = "00002a19-0000-1000-8000-00805f9b34fb"
DEVICE_INFORMATION_CHARACTERISTIC = "00002a29-0000-1000-8000-00805f9b34fb"
LED_MATRIX_CHARACTERISTIC         = "f29b1523-cb19-40f3-be5c-7241ecb82fd1"
FLY_CHARACTERISTIC                = "f29b1526-cb19-40f3-be5c-7241ecb82fd2"
SWIPE_CHARACTERISTIC              = "f29b1527-cb19-40f3-be5c-7241ecb82fd2"
ROTATION_CHARACTERISTIC           = "f29b1528-cb19-40f3-be5c-7241ecb82fd2"
BUTTON_CLICK_CHARACTERISTIC       = "f29b1529-cb19-40f3-be5c-7241ecb82fd2"

# Characteristic value handles
BATTERY_VALUE_HANDLE   = 11
FLY_VALUE_HANDLE       = 32
SWIPE_VALUE_HANDLE     = 35
ROTATION_VALUE_HANDLE  = 38
CLICK_VALUE_HANDLE     = 29
LEDMATRIX_VALUE_HANDLE = 26

# Notification handles
BATTERY_NOTIFICATION_HANDLE  = BATTERY_VALUE_HANDLE + 1
FLY_NOTIFICATION_HANDLE      = FLY_VALUE_HANDLE + 1
SWIPE_NOTIFICATION_HANDLE    = SWIPE_VALUE_HANDLE + 1
ROTATION_NOTIFICATION_HANDLE = ROTATION_VALUE_HANDLE + 1
CLICK_NOTIFICATION_HANDLE    = CLICK_VALUE_HANDLE + 1

# Notification data
NOTIFICATION_ON  = struct.pack("BB", 0x01, 0x00)
NOTIFICATION_OFF = struct.pack("BB", 0x00, 0x00)

class NuimoDelegate(DefaultDelegate):

    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        if int(cHandle) == BATTERY_VALUE_HANDLE:
            print "BATTERY", ord(data[0])
        elif int(cHandle) == FLY_VALUE_HANDLE:
            value = ord(data[0]) + ord(data[1]) << 8
            if value >= 1 << 15:
                value = value - 1 << 16
            print "FLY", value
        elif int(cHandle) == SWIPE_VALUE_HANDLE:
            print "SWIPE", ord(data[0])
        elif int(cHandle) == ROTATION_VALUE_HANDLE:
            value = ord(data[0]) + (ord(data[1]) << 8)
            if value >= 1 << 15:
                value = value - (1 << 16)
            print "ROTATION", value
        elif int(cHandle) == CLICK_VALUE_HANDLE:
            print "CLICK", ord(data[0])


class Nuimo:

    def __init__(self, macAddress='FA:48:12:00:CA:AC'):
        self.macAddress = macAddress

    def connect(self):
        try:
            self.peripheral = Peripheral(self.macAddress, addrType='random')
        except BTLEException:
            return False
        try:
            self.enableNotifications()
            self.peripheral.setDelegate(NuimoDelegate())
        except BTLEException:
            self.peripheral.disconnect()
            self.peripheral = None
            return False
        return True

    def enableNotifications(self):
        self.peripheral.writeCharacteristic(CLICK_NOTIFICATION_HANDLE,    NOTIFICATION_ON)
        self.peripheral.writeCharacteristic(BATTERY_NOTIFICATION_HANDLE,  NOTIFICATION_ON)
        self.peripheral.writeCharacteristic(FLY_NOTIFICATION_HANDLE,      NOTIFICATION_ON)
        self.peripheral.writeCharacteristic(SWIPE_NOTIFICATION_HANDLE,    NOTIFICATION_ON)
        self.peripheral.writeCharacteristic(ROTATION_NOTIFICATION_HANDLE, NOTIFICATION_ON)

    def waitForNotifications(self):
        try:
            self.peripheral.waitForNotifications(1.0)
            return True
        except BTLEException as e:
            return False

    def displayLedMatrix(self, matrix, brightness, timeout):
        self.peripheral.writeCharacteristic(LEDMATRIX_VALUE_HANDLE, struct.pack("BBBBBBBBBBBBB", 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python nuimo.py <Nuimo's MAC address>"
        sys.exit()

    nuimo = Nuimo(sys.argv[1])

    # Connect to Nuimo
    print "Trying to connect to %s. Press Ctrl+C to cancel." % sys.argv[1]
    if not nuimo.connect():
        print "Failed to connect to %s. Make sure to:\n  1. Enable the Bluetooth device: hciconfig hci0 up\n  2. Enable BLE: btmgmt le on\n  3. Pass the right MAC address: hcitool lescan | grep Nuimo" % nuimo.macAddress
        sys.exit()
    print "Connected. Waiting for input events..."

    # Display all LEDs on and wait for notifications
    nuimo.displayLedMatrix("*********", 1.0, 10.0)
    while True:
        if not nuimo.waitForNotifications():
            break
