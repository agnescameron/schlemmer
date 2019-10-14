# Example of low level interaction with a BLE UART device that has an RX and TX
# characteristic for receiving and sending data.  This doesn't use any service
# implementation and instead just manipulates the services and characteristics
# on a device.  See the uart_service.py example for a simpler UART service
# example that uses a high level service implementation.
# Author: Tony DiCola
import logging
import time
import uuid
import struct
# from chunnel import Socket

import Adafruit_BluefruitLE

import socket
import sys
import os

from Queue import Queue
from threading import Thread


# Enable debug output.
#logging.basicConfig(level=logging.DEBUG)

# Define service and characteristic UUIDs used by the UART service.
UART_SERVICE_UUID = uuid.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
TX_CHAR_UUID      = uuid.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E')
RX_CHAR_UUID      = uuid.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E')

# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

# how many devices are you working with
numDevices = 4

# Main function implements the program logic so it can run in a background
# thread.  Most platforms require the main thread to handle GUI events and other
# asyncronous events like BLE actions.  All of the threading logic is taken care
# of automatically though and you just need to provide a main function that uses
# the BLE provider.
def main():
    # Clear any cached data because both bluez and CoreBluetooth have issues with
    # caching data and it going stale.
    ble.clear_cached_data()

    # Get the first available BLE network adapter and make sure it's powered on.
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))

    # Disconnect any currently connected UART devices.  Good for cleaning up and
    # starting from a fresh state.
    print('Disconnecting any connected UART devices...')
    ble.disconnect_devices([UART_SERVICE_UUID])

    # Scan for UART devices.
    print('Searching for UART devices...')
    try:
        adapter.start_scan()
        # Search for the first UART device found (will time out after 60 seconds
        # but you can specify an optional timeout_sec parameter to change it).
        devices = []
        for i in range (0, numDevices):
            deviceName = 'temp%d' % i
            print(deviceName)
            device = ble.find_device(service_uuids=[UART_SERVICE_UUID], name=deviceName)
            if device is None:
                raise RuntimeError('Failed to find UART device %d!' % i)
            devices.append(device)


    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()

    print('Connecting to device...')
    for i in range (0, numDevices):
        devices[i].connect()

    # Once connected do everything else in a try/finally to make sure the device
    # is disconnected when done.
    try:
        # Wait for service discovery to complete for at least the specified
        # service and characteristic UUID lists.  Will time out after 60 seconds
        # (specify timeout_sec parameter to override).
        print('Discovering services...')
        rx = []
        tx = []
        uart = []

        for i in range (0, numDevices):
            devices[i].discover([UART_SERVICE_UUID], [TX_CHAR_UUID, RX_CHAR_UUID])
            uart.append(devices[i].find_service(UART_SERVICE_UUID))
            rx.append(uart[i].find_characteristic(RX_CHAR_UUID))
            tx.append(uart[i].find_characteristic(TX_CHAR_UUID))

        # Function to receive RX characteristic changes.  Note that this will
        # be called on a different thread so be careful to make sure state that
        # the function changes is thread safe.  Use queue or other thread-safe
        # primitives to send data to other threads.

        def received(data):
            if data is not None:
                ints = struct.unpack('II', data)
                print('Received:', ints)
                file = open('temp-live.txt', "w")
                file.write("%s %s\n" % (ints[0], ints[1])) #, randrange(5)
                file.close
            else:
                print('no data!')


        # Turn on notification of RX characteristics using the callback above.
        print('Subscribing to RX characteristic changes...')
        # rx[1].start_notify(received)
        for i in range (0, numDevices):
            rx[i].start_notify(received)

        time.sleep(3000)

    finally:
        print('well, got here')


file = open('temp-live.txt', "w")
file.write('')
file.close


# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)
