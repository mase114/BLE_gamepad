from machine import Pin,ADC,PWM
import utime
import ubluetooth
import ble_gamepad

ble = ubluetooth.BLE()
pad = ble_gamepad.gamepad(ble)
pad.scan()
sw = pad.status()
pad.connect(addr_type=0, addr='変更')

#I/Oピン入出力設定
"""
入出力設定
"""

while not pad.is_connected():
    for i in range(2, 0, -1):
        print(i)
        utime.sleep(1)

while pad.is_connected():
    print(sw.btnA,sw.btnB,sw.btnX,sw.btnY,sw.btnL,sw.btnR,sw.btnLT,sw.btnRT,sw.btnLS,sw.btnRS,sw.btnSELECT,sw.btnSTART,sw.pad,sw.axes,sw.buttons)
    """
    スイッチ動作処理
    """
    utime.sleep_us(10)   #チャタリング防止
