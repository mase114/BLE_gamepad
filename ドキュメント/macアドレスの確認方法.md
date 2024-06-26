# macアドレスの確認方法

## macアドレスとはなに？

macアドレスは、ネットワークデバイスがネットワーク上で一意に識別されるための物理的なアドレスです。通常、イーサネットやWi-Fiなどのネットワークインターフェースに関連付けられています。macアドレスは、ハードウェアに固有の識別子であり、ネットワーク上でデータを送受信するために使用されます。

macアドレスは、BLEデバイスの一意の識別子として機能し、周囲のデバイスと通信する際に使用されます。

## BLEアドバタイズメントについて

BLEアドバタイズメントは、BLEデバイスが自身の存在を周囲のデバイスに通知するために使用されるメカニズムです。これは、デバイスが接続可能な状態になる前に、スキャンしているデバイスがそれを検出できるようにするために使用されます。

#### BLEアドバタイズメントには、次のような情報が含まれます.

- macアドレス
- サービス情報
- 電源レベル
- デバイスの名前
- カスタムデータ

## [gamepad_scan.py](https://github.com/mase114/BLE_gamepad/blob/main/gamepad_scan.py)を使う

[gamepad_scan.py](https://github.com/mase114/BLE_gamepad/blob/main/gamepad_scan.py)を愛用してmacアドレスを取得するため
ゲームパッドをアドバタイズメント状態にし、コードを実行します。

[ble_gamepad.py](https://github.com/mase114/BLE_gamepad/blob/main/ble_gamepad.py)をマイコンに書き込んでおく

ターミナルに表示されるデバイス名`今回はZM T-12`の`ADDR=`の値をコピーします。

![IMG_9650](https://github.com/mase114/BLE_gamepad/assets/142933261/b224aff7-fec1-4b6a-8057-d59d398c330f)
