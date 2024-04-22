import utime
import ubluetooth
import ble_gamepad

ble = ubluetooth.BLE()
pad = ble_gamepad.gamepad(ble)
pad.scan()

while not pad.is_connected():
    for i in range(2, 0, -1):
        print(i)
        utime.sleep(1)