# BLE_gamepad

## BLE通信でゲームパッドを使うには？

BLE通信を使用してゲームパッドとマイコンを接続するために、BLE対応ゲームパッドを使用しなければなリません。

今回使用したゲームパッドは[ZM T-12](https://www.amazon.co.jp/gp/product/B07XRW22C8/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&psc=1)コントローラーです。

## [gamepad_template.py](https://github.com/mase114/BLE_gamepad/blob/main/gamepad_template.py)の使い方

### macアドレスの入力

```python
ble = ubluetooth.BLE()
pad = ble_gamepad.gamepad(ble)
pad.scan()
sw = pad.status()
pad.connect(addr_type=0, addr='変更')
````

`addr=`の`'変更'`をスキャンしたmacアドレスに変更する。
`''は残す`
