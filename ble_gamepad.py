import ubluetooth
import struct
import utime
from micropython import const

_IRQ_SCAN_RESULT                 = const(5)
_IRQ_SCAN_DONE                   = const(6)
_IRQ_PERIPHERAL_CONNECT          = const(7)
_IRQ_PERIPHERAL_DISCONNECT       = const(8)
_IRQ_GATTC_SERVICE_RESULT        = const(9)
_IRQ_GATTC_SERVICE_DONE          = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE   = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT     = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE       = const(14)
_IRQ_GATTC_READ_RESULT           = const(15)
_IRQ_GATTC_READ_DONE             = const(16)
_IRQ_GATTC_WRITE_DONE            = const(17)
_IRQ_GATTC_NOTIFY                = const(18)
_IRQ_GATTC_INDICATE              = const(19)

_ADV_IND         = const(0x00)
_ADV_DIRECT_IND  = const(0x01)
_ADV_SCAN_IND    = const(0x02)
_ADV_NONCONN_IND = const(0x03)

_ADV_TYPE_FLAGS            = const(0x01)
_ADV_TYPE_NAME             = const(0x09)
_ADV_TYPE_UUID16_COMPLETE  = const(0x3)
_ADV_TYPE_UUID32_COMPLETE  = const(0x5)
_ADV_TYPE_UUID128_COMPLETE = const(0x7)
_ADV_TYPE_APPEARANCE       = const(0x19)


# decode field name
def decode_field(payload, adv_type):
    i = 0
    result = []
    while( i + 1 < len(payload) ):
        if payload[i + 1] == adv_type:
            result.append(payload[i + 2:i + payload[i] + 1])
        i += 1 + payload[i]
    return result


# decode device name
def decode_name(payload):
    n = decode_field(payload, _ADV_TYPE_NAME)
    return str(n[0], 'utf-8') if n else ''


# decode service UUID
def decode_services(payload):
    services = []
    for u in decode_field(payload, _ADV_TYPE_UUID16_COMPLETE):
        services.append(bluetooth.UUID(struct.unpack('<h', u)[0]))
    for u in decode_field(payload, _ADV_TYPE_UUID32_COMPLETE):
        services.append(bluetooth.UUID(struct.unpack('<d', u)[0]))
    for u in decode_field(payload, _ADV_TYPE_UUID128_COMPLETE):
        services.append(bluetooth.UUID(u))
    return services


# decode MAC address
def decode_addr(payload):
    ret = ''
    for d in payload:
        ret = ret + ':' + '{:02X}'.format(d)
    return ret[1:]


# encode MAC address
def encode_addr(payload):
    ret = []
    d   = ''
    for c in payload:
        if( c == ':' or c == '-' ):
            ret.append( int( d, 16 ) )
            d = ''
        else:
            d = d + c            
    ret.append( int( d, 16 ) )
    return ret


class GamePadStatus(object):
    buttons: int
    btnA:  bool
    btnB:  bool
    btnX:  bool
    btnY:  bool
    btnL:  bool
    btnR:  bool
    btnLT: bool
    btnRT: bool    
    btnLB: bool
    btnRB: bool
    btnLS: bool
    btnRS: bool
    btnSTART: bool
    btnSELECT: bool    
    axis: []
    axisLX:   byte
    axisLY:   byte
    axisRX:   byte
    axisRY:   byte
    pads: byte
    padU: bool
    padL: bool
    padD: bool
    padR: bool
    

# BLE GamePad central object
class gamepad(object):
    def __init__(self, ble):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        self._reset()
        
        # initialize gamepad status
        self._count        = 0
        self._pad          = GamePadStatus()
        self._pad.buttons  = 0
        self._pad.btnA     = False
        self._pad.btnB     = False
        self._pad.btnX     = False
        self._pad.btnY     = False
        self._pad.btnL     = False
        self._pad.btnR     = False
        self._pad.btnLT    = False
        self._pad.btnRT    = False
        self._pad.btnLB    = False
        self._pad.btnRB    = False
        self._pad.btnLS    = False
        self._pad.btnRS    = False
        self._pad.btnSTART  = False
        self._pad.btnSELECT = False        
        self._pad.axes     = [0, 0, 0, 0]
        self._pad.axisLX   = 0
        self._pad.axisLY   = 0
        self._pad.axisRX   = 0
        self._pad.axisRY   = 0
        self._pad.pad      = 0
        self._pad.padU     = False
        self._pad.padL     = False
        self._pad.padD     = False
        self._pad.padR     = False

    # reset
    def _reset(self):
        # Cached name and address from a successful scan.
        self._name      = None
        self._addr_type = None
        self._addr      = None

        # Cached value (if we have one)
        self._value     = None

        # callback function
        self._conn_callback = None
        self._read_callback = None

        # Persistent callback for when new data is notified from the device.
        self._notify_callback = None

        # Connected device.
        self._conn_handle  = None
        self._start_handle = None
        self._end_handle   = None
        self._value_handle = None
        
        self._is_scanning  = False
        self._is_connected = False


    # interrupt function
    def _irq(self, event, data):
        # check event
        if(event == _IRQ_SCAN_RESULT):
            # get scan result            
            (addr_type, addr, adv_type, rssi, adv_data) = data # get detected device data
            mac = decode_addr(list(bytes(addr)))
            print( 'FOUND DEVICE! : TYPE={}\tADDR={}\tNAME={}'.format(addr_type, mac, decode_name(adv_data)) )
            # device check

        elif(event == _IRQ_SCAN_DONE):
            #print('### SCAN DONE ###')            
            # scanned all devices
            self._is_scanning   = False

        elif(event == _IRQ_PERIPHERAL_CONNECT):
            #print('### CONNECT ###')
            # connect successful
            (conn_handle, addr_type, addr) = data
            if( addr_type == self._addr_type and addr == self._addr):
                self._is_connected = True                
                self._conn_handle  = conn_handle
                self._ble.gattc_discover_services(self._conn_handle)

        elif(event == _IRQ_PERIPHERAL_DISCONNECT):
            #print('### DISCONNECT ###')
            # disconnect
            (conn_handle, _, _) = data
            if(conn_handle == self._conn_handle):
                self._is_connected = False                
                self._reset()                

        elif(event == _IRQ_GATTC_SERVICE_RESULT):
            #print('### SERVICE RESULT ###')
            (conn_handle, start_handle, end_handle, uuid) = data
            print(conn_handle, start_handle, end_handle, uuid)

        elif(event == _IRQ_GATTC_SERVICE_DONE):
            #print('### SERVICE DONE ###')
            print(data)
            # Service query complete.
            if(self._start_handle and self._end_handle):
                self._ble.gattc_discover_characteristics(
                    self._conn_handle, self._start_handle, self._end_handle
                )
            else:
                print("Failed to find environmental sensing service.")

        elif(event == _IRQ_GATTC_CHARACTERISTIC_RESULT):
            #print('### CHARACTERISTIC RESULT ###')            
            # Connected device returned a characteristic.
            (conn_handle, def_handle, value_handle, properties, uuid) = data

        elif(event == _IRQ_GATTC_CHARACTERISTIC_DONE):
            #print('### CHARACTERISTIC DONE ###')
            print(data)
            # Characteristic query complete.
            if(self._value_handle):
                # We've finished connecting and discovering device, fire the connect callback.
                if(self._conn_callback):
                    self._conn_callback()
            else:
                print("Failed to find temperature characteristic.")

        elif(event == _IRQ_GATTC_READ_RESULT):
            #print('### READ RESULT ###')            
            # A read completed successfully.
            (conn_handle, value_handle, char_data) = data

        elif(event == _IRQ_GATTC_READ_DONE):
            #print('### READ DONE ###')            
            # Read completed (no-op).
            ( conn_handle, value_handle, status ) = data

        elif(event == _IRQ_GATTC_NOTIFY):
            #print('### NOTIFY ###')
            self._count = self._count + 1
            ( conn_handle, value_handle, notify_data ) = data
            state = list(notify_data)
            self._pad.btnA  = state[5] & 0x01
            self._pad.btnB  = state[5] & 0x02
            self._pad.btnX  = state[5] & 0x08
            self._pad.btnY  = state[5] & 0x10
            self._pad.btnL  = state[5] & 0x40
            self._pad.btnR  = state[5] & 0x80

            self._pad.btnLT     = state[6] & 0x01
            self._pad.btnRT     = state[6] & 0x02
            self._pad.btnSELECT  = state[6] & 0x04
            self._pad.btnSTART = state[6] & 0x08
            self._pad.btnLS     = state[6] & 0x20
            self._pad.btnRS     = state[6] & 0x40
            
            self._pad.axisLX = state[0]-128
            self._pad.axisLY = state[0]-128
            self._pad.axisRX = state[0]-128
            self._pad.axisRY = state[0]-128
            self._pad.axes   = [ state[0]-128, state[1]-128, state[2]-128, state[3]-128 ]
            
            self._pad.pad     = state[4]
            self._pad.buttons = state[6] * 256 + state[5]
            
            #print(self._pad.buttons)
            #print(self._count, conn_handle, value_handle, state)
            
    def status(self):
        return self._pad


    # connect check
    def is_connected(self):
        return(self._is_connected)


    # scanning check
    def is_scanning(self):
        return(self._is_scanning)    


    # scan
    def scan(self, callback=None):
        self._addr_type     = None
        self._addr          = None
        self._is_scanning   = True
        self._ble.gap_scan(2000, 30000, 30000)


    # connect
    def connect(self, addr_type=None, addr=''):
        self._addr_type = addr_type
        self._addr      = bytes(encode_addr(addr))
        print(self._addr)
        if( self._addr is None ):            
            return False
        
        # connect to peripheral
        self._ble.gap_connect(self._addr_type, self._addr)
        return True


    # disconnect
    def disconnect(self):
        if(not self._conn_handle):
            return
        self._ble.gap_disconnect(self._conn_handle)
        self._reset()


    # Issues an (asynchronous) read, will invoke callback with data.
    def read(self, callback):
        if not self.is_connected():
            return
        self._read_callback = callback
        self._ble.gattc_read(self._conn_handle, self._value_handle)


    # set notify callback
    def on_notify(self, callback):
        self._notify_callback = callback

