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

## macアドレスの確認

[macアドレスの確認方法を参照](https://github.com/mase114/BLE_gamepad/blob/main/%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88/mac%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%81%AE%E7%A2%BA%E8%AA%8D%E6%96%B9%E6%B3%95.md)

## 各ボタンの入力信号の値

| 変数名 | 値 | ボタン名 |
| --- | -- | :----: |
| `sw.btnA` | `1` | A |
| `sw.btnB` | `2` | B |
| `sw.btnX` | `8` | X |
| `sw.btnY` | `16` | Y |
| `sw.btnL` | `64` | BL |
| `sw.btnR` | `128` | BR |
| `sw.btnLT` | `1` | LT |
| `sw.btnRT` | `2` | RT |
| `sw.btnLS` | `32` | Lスティックボタン and 背面L |
| `sw.btnRS` | `64` | Rスティックボタン and 背面R |
| `sw.btnSELECT` | `4` | SELECT |
| `sw.btnSTART` | `8` | START |
| `sw.pad` | `0` | ↑ |
| `sw.pad` | `6` | ← |
| `sw.pad` | `4` | ↓ |
| `sw.pad` | `2` | → |
| `sw.pad` | `7` | ←↑ |
| `sw.pad` | `1` | ↑→ |
| `sw.pad` | `5` | ←↓ |
| `sw.pad` | `3` | ↓→ |
| `sw.axisLX` | `127~-128` | スティックL_X |
| `sw.axisLY` | `127~-128` | スティックL_Y |
| `sw.axisRX` | `127~-128` | スティックR_X |
| `sw.axisRY` | `127~-128` | スティックR_Y |

使用デバイス:`ZM T-12`
