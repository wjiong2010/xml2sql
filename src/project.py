# -*- coding: utf-8 -*-

# History maintainers:
# Maintainer: John.Wang/Ernie.Hu
import re
import random


# Parse XML files
class ProtocolType:
    NAVIGATION = 0,  # 导航页
    TELEMETRY = 1,  # 遥测协议, 即通常说的 @Track 协议.
    TELEMETRY_PARSER = 2,  # 遥测协议对应的服务器端消息解析器用户手册
    BLUETOOTH = 7,  # Bluetooth RF 协议.


POSITION = 1,
DEVICE_INFO = 2,
REALTIME = 3,
EVENT_REPORT = 4,
DATA_REPORT = 5,
CRASH_DATA = 6,
CAN_INFO = 7,
UPDATE = 8,
CONNECTIVE = 9

SEPARATE_FLAG = ' | '

message_type_tuple = ('posi', 'dinf', 'rtrp', 'event', 'data', 'crash', 'cinf', 'updr', 'conr')


def get_message_type(i):
    try:
        return message_type_tuple[i]
    except IndexError:
        print('{0} is out of boundary!'.format(i))
        raise


class IDc:
    def model_check(self, v):
        if str(v) in self.model_list:
            return True
        else:
            return False

    def reset(self):
        self.valid = False
        self.model_list.clear()

    def __init__(self):
        self.valid = False
        self.name = ''
        self.model_list = []


class BitX:
    def __init__(self):
        self.valid = False
        self.value = '0'


# Class of Mask, mask string parser functions included.
class _Mask:
    def __init__(self):
        self.valid = False
        self.value = ''
        self.BitCnt = 0
        self.Bits = ''
        self.Bit = {0: BitX(), 1: BitX(), 2: BitX(), 3: BitX(), 4: BitX(), 5: BitX(), 6: BitX(), 7: BitX(),
                    8: BitX(), 9: BitX(), 10: BitX(), 11: BitX(), 12: BitX(), 13: BitX(), 14: BitX(), 15: BitX(),
                    16: BitX(), 17: BitX(), 18: BitX(), 19: BitX(), 20: BitX(), 21: BitX(), 22: BitX(), 23: BitX(),
                    24: BitX(), 25: BitX(), 26: BitX(), 27: BitX(), 28: BitX(), 29: BitX(), 30: BitX(), 31: BitX(),
                    32: BitX(), 33: BitX(), 34: BitX(), 35: BitX(), 36: BitX(), 37: BitX(), 38: BitX(), 39: BitX(),
                    40: BitX(), 41: BitX(), 42: BitX(), 43: BitX(), 44: BitX(), 45: BitX(), 46: BitX(), 47: BitX(),
                    48: BitX(), 49: BitX(), 50: BitX(), 51: BitX(), 52: BitX(), 53: BitX(), 54: BitX(), 55: BitX(),
                    56: BitX(), 57: BitX(), 58: BitX(), 59: BitX(), 60: BitX(), 61: BitX(), 62: BitX(), 63: BitX()
                    }

    def bit_check(self, i):
        if 0 == int(self.Bit[i].value):
            return False
        else:
            return True

    def parse(self, mask_str):
        self.valid = True
        self.value = mask_str
        # get binary string
        bin_str = ''

        for d in mask_str:
            bin_str += '{:>04b}'.format(int(d, 16))
        bit_strlen = len(bin_str)
        if 0 < bit_strlen <= 64:
            self.BitCnt = bit_strlen
            self.Bits = bin_str
            i = 0
            for m in reversed(bin_str):
                self.Bit[i].valid = True
                if m == '1':
                    self.Bit[i].value = '1'
                else:
                    self.Bit[i].value = '0'
                i += 1
        else:
            self.BitCnt = 0
            self.Bits = ''

    def reset(self):
        self.valid = False
        self.value = ''
        self.BitCnt = 0
        self.Bits = ''
        for i in range(0, 64):
            self.Bit[i].valid = False
            self.Bit[i].value = '0'


class Valid:
    def __init__(self):
        self.valid = False


def is_hex_digit(s):
    pattern = re.compile(r'^[xXa-fA-F]+$')
    try:
        if pattern.match(s.strip()):
            return True
        else:
            return False
    except ValueError:
        print("regx no match")
        return False


# convert digital to string
def digi_2_str(n, is_hex):
    if is_hex:
        return str(hex(n))[2:].upper()  # discard '0x'
    else:
        return str(n)


# parameter attribute: <name>, <Range>, <Default>, <Len>, <Item>, <Left>, <Right>, <LeftRight>
class _Param:
    class _Range:
        class _LeftRight:
            def __init__(self):
                self.l = 0
                self.r = 0

        def add_leftright(self, value):
            self.LeftRight.append(value)

        def get_leftright(self):
            out_str = ''
            if len(self.LeftRight) == 0:
                return out_str

            for lr in self.LeftRight:
                if lr.l == lr.r:
                    out_str += str(lr.l)
                else:
                    out_str += "{}-{}".format(lr.l, lr.r)
                out_str += '|'

            if out_str[-1] == '|':
                return out_str[:-1]
            else:
                return out_str

        def clear_leftright(self):
            self.LeftRight.clear()

        def add_item(self, value):
            self.items_list.append(value)

        def get_items_str(self):
            ret_str = ''
            tl = []
            print("items_list: {0}, {1}".format(self.items_list, self.rng_type))

            if len(self.items_list) == 0:
                return ret_str

            if self.rng_type == "special_str":
                for it in self.items_list:
                    ret_str += str(it)
                    ret_str += SEPARATE_FLAG
            else:
                if self.rng_type == "hexNumber":
                    is_hex = True
                else:
                    is_hex = False
                for it in self.items_list:
                    if is_hex:
                        v = int(it, 16)
                    else:
                        v = int(it)
                    if len(tl) == 0:
                        tl.append(v)
                    else:
                        if v - tl[-1] == 1:
                            tl.append(v)
                            continue
                        else:
                            if len(tl) >= 3:
                                ret_str += digi_2_str(tl[0], is_hex)
                                ret_str += '-'
                                ret_str += digi_2_str(tl[-1], is_hex)
                                ret_str += SEPARATE_FLAG
                            else:
                                for t in tl:
                                    ret_str += digi_2_str(t, is_hex)
                                    ret_str += SEPARATE_FLAG
                            tl.clear()
                            tl.append(v)
                if len(tl) >= 3:
                    ret_str += digi_2_str(tl[0], is_hex)
                    ret_str += '-'
                    ret_str += digi_2_str(tl[-1], is_hex)
                else:
                    for t in tl:
                        ret_str += digi_2_str(t, is_hex)
                        ret_str += SEPARATE_FLAG

            # discard the last '|' if it is existing.
            c = SEPARATE_FLAG.strip()
            ret_str = ret_str.strip()
            if ret_str.endswith(c):
                ret_str = ret_str[:-1]
            if ret_str.startswith(c):
                ret_str = ret_str[1:]

            print(f"return_str: {ret_str}")

            return ret_str

        def leftright_value_compare(self, vid, lr, flag, iv_s):
            # print(f"value_compare,id: {vid}, lr: {lr}, flag: {flag}, value: {iv_s}")
            if len(self.LeftRight) <= vid:
                return False

            if self.RangeType["hexNumber"] == "hexNumber" \
                    or is_hex_digit(self.LeftRight[vid].l) \
                    or is_hex_digit(self.LeftRight[vid].r) \
                    or is_hex_digit(iv_s):
                is_hex = True
            else:
                is_hex = False

            if lr == 'L':
                if is_hex:
                    v = int(self.LeftRight[vid].l, 16)
                    iv = int(iv_s, 16)
                else:
                    v = int(self.LeftRight[vid].l)
                    iv = int(iv_s)
            else:
                if is_hex:
                    v = int(self.LeftRight[vid].r, 16)
                    iv = int(iv_s, 16)
                else:
                    v = int(self.LeftRight[vid].r)
                    iv = int(iv_s)

            if flag == "gt" and v > iv:
                return True
            if flag == "ge" and v >= iv:
                return True
            if flag == "lt" and v < iv:
                return True
            if flag == "le" and v <= iv:
                return True

            return False

        def in_item(self, v):
            if v in self.items_list:
                return True
            else:
                return False

        def clear_items(self):
            self.items_list.clear()

        def reset(self):
            # self.clear_items()
            # self.clear_leftright()
            self.filter_mask.reset()
            for itm in self.Item.values():
                itm.reset()

        def __init__(self):
            self.Item = {0: IDc(), 1: IDc(), 2: IDc(), 3: IDc(), 4: IDc(), 5: IDc(), 6: IDc(), 7: IDc(), 8: IDc(),
                         9: IDc(), 10: IDc(), 11: IDc(), 12: IDc(), 13: IDc(), 14: IDc(), 15: IDc(), 16: IDc(),
                         17: IDc(),
                         18: IDc(), 19: IDc(), 20: IDc(), 21: IDc(), 22: IDc(), 23: IDc(), 24: IDc(), 25: IDc(),
                         26: IDc(), 27: IDc(),
                         28: IDc(), 29: IDc(), 30: IDc(), 31: IDc(), 32: IDc(), 33: IDc(), 34: IDc(), 35: IDc(),
                         36: IDc(), 37: IDc(),
                         38: IDc(), 39: IDc(), 40: IDc(), 43: IDc(), 47: IDc(), 48: IDc(), 49: IDc(), 50: IDc(),
                         56: IDc(), 58: IDc(),
                         60: IDc(), 100: IDc(), 120: IDc(), 180: IDc(), 200: IDc(), 240: IDc(), 300: IDc(), 360: IDc(),
                         400: IDc(),
                         480: IDc(), 600: IDc(), 720: IDc(), 1440: IDc(), 1800: IDc()}
            self.RangeType = {"ASCII0": "ASCII String",
                              "ASCII1": "ASCII (not including '=' and ',')",
                              "ASCII2": "ASCII",
                              "ASCII3": "ASCII (not including '=')",
                              "PlusSub": "+|-",
                              "FullDate": "YYYYMMDDHHMMSS",
                              "FullDate2": "YYYYMMDDHHMM",
                              "RngTime1": "00000:00:00-99999:00:00",
                              "RngTime2": "00000:00:00-1193000:00:00",
                              "Time1": "HHMM",
                              "Time2": "HHHHH:MM:SS",
                              "Time3": "+|-HHMM",
                              "Time4": "DYYYY/MM/DDTHH:MM:SS",
                              "Time5": "HHMMSS",
                              "Time6": "HHHHHHHHMMSS",
                              "URL": "Legal URL",
                              "URL1": "Complete URL",
                              "PVersion": "XX0000-XXFFFF,X∈{'A'-'Z','0'-'9'}",
                              "HEX": "HEX",
                              "Number": "'0'-'9'",
                              "AlphaNum1": "'0'-'9' 'A'-'F'",
                              "AlphaNum2": "'0'-'9' 'a'-'z' 'A'-'Z' '#'",
                              "AlphaNum3": "'0'-'9' 'a'-'z' 'A'-'Z' '-' '_' '%'",
                              "AlphaNum4": "'0'-'9' 'a'-'z' 'A'-'Z'",
                              "AlphaNum5": "'0'-'9' 'a'-'z' 'A'-'Z' '-' '_'",
                              "AlphaNum6": "'0'-'9' 'a'-'f' 'A'-'F'",
                              "AlphaNum7": "'0' - '9' 'a' - 'z'",
                              "AlphaNum8": "'0' - '9', 'a' - 'z', '.'",
                              "AlphaNum9": "'0' - '9' 'a' - 'z' '.' '()'",
                              "AlphaNum10": "'0' - '9' 'A' - 'F'",
                              "AlphaNum11": "'0' - '9' 'a' - 'z' 'A' - 'Z' '-' '_' '.'",
                              "AlphaNum12": "'0' - '9' 'A' - 'Z' except 'I', 'O', 'Q'",
                              "AlphaNum13": "'0' - '9', 'a' - 'z', 'A' - 'Z', '-', '_', ' '",
                              "AlphaNum14": "'0'-'9' 'a'-'f'",
                              "AlphaNum15": "'0'-'9' 'A'-'Z'",
                              "AlphaNum16": "'0'-'9' 'a'-'z' 'A'-'Z' ':' '/' '.'",
                              "AlphaNum17": "ASCII except ',' and '$'",
                              "IMEI": "IMEI",
                              "ICCID": "ICCID",
                              "google": "http://maps.google.com/maps?q=",
                              "UID": "IMEI/Device Name",
                              "ATCmd": "AT command",
                              "Alti": "(-)xxxxx.x m",
                              "Lng": "(-)xxx.xxxxxx",
                              "Lat": "(-)xx.xxxxxx",
                              "hexNumber": "hexNumber",
                              "cmdName": "cmdName"}
            self.Items = ''
            self.LR = self._LeftRight()
            self.LeftRight = []
            self.items_list = []
            self.ItemCnt = 0
            self.rng_type = ''
            self.filter_mask = _Mask()
            self.description = ''

    def get_random_value(self, hex_format, fix_len=0, float_number=False):
        if not self.valid:
            print(f"Invalid")
            return ""

        lr_len = len(self.Range.LeftRight)
        if lr_len != 0:
            lr = random.choice(self.Range.LeftRight)

            if float_number:
                fv = random.uniform(lr.l, lr.r)
                return '{:.1f}'.format(fv)
            else:
                if hex_format:
                    lv = int(lr.l, 16)
                    rv = int(lr.r, 16)
                    if fix_len != 0:
                        FORMAT_HEX = "{:0" + str(fix_len) + "x}"
                        print(FORMAT_HEX)
                    else:
                        FORMAT_HEX = "{:x}"
                    rdv = random.randint(lv, rv)
                    s_rdv = FORMAT_HEX.format(rdv)
                    return s_rdv
                else:
                    rdv = random.randint(int(lr.l), int(lr.r))
                    return str(rdv)

        item_len = len(self.Range.items_list)
        if item_len != 0:
            if hex_format:
                rdv = random.choice(self.Range.items_list)
                rdv = int(rdv, 16)
                if fix_len != 0:
                    FORMAT_HEX = "{:0" + str(fix_len) + "x}"
                    print(FORMAT_HEX)
                else:
                    FORMAT_HEX = "{:x}"
                    FORMAT_HEX.format(rdv)
                return rdv
            else:
                rdv = random.choice(self.Range.items_list)
                return rdv

    def reset(self):
        self.valid = False
        self.Range.reset()

    def reserved(self):
        if self.name.upper() == "RESERVED":
            return True
        else:
            return False

    def __init__(self):
        self.valid = False
        self.name = ''
        self.Len = '0'
        self.Default = '0'
        self.Range = self._Range()


# Command parameter Px
class CMDc:
    def reset(self):
        self.valid = False
        for i in range(1, self.para_number):
            s = "self.P" + str(i) + ".reset()"
            eval(s)

    def __init__(self):
        self.valid = False
        self.name = ''
        self.para_number = 200

        for i in range(1, self.para_number + 1):
            attr_name = f"P{i}"
            setattr(self, attr_name, _Param())

    def set_name(self, n):
        self.name = n


# Message Group, There are many parameters in a group
class _Group:
    def member_valid(self, m):
        if self.valid:
            return m.strip() in self.member_list
        else:
            return False

    def member_clear(self):
        self.member_list.clear()

    def member_get(self):
        if self.valid:
            return self.member
        else:
            return "no member"

    def reset(self):
        self.valid = False
        self.member = ''
        self.member_list = []
        self.id = 0
        for i in range(1, self.para_number):
            s = "self.P" + str(i) + ".reset()"
            eval(s)

    def __init__(self):
        self.valid = False
        self.member = ''
        self.member_list = []
        self.id = 0
        self.para_number = 180

        for i in range(1, self.para_number + 1):
            attr_name = f"P{i}"
            setattr(self, attr_name, _Param())


# base class of message type, there are many groups in a type of message
class _MessageType:
    def reset(self):
        for i in range(1, self.g_number + 1):
            s = "self.G" + str(i) + ".reset()"
            eval(s)

    def __init__(self, t, n, gn):
        self.valid = False
        self.type = t
        self.name = n
        self.g_number = gn


class _MessageTypePosi(_MessageType):
    def reset(self):
        _MessageType.reset(self)

    def __init__(self, t, n):
        _MessageType.__init__(self, t, n, 15)
        self.G1 = _Group()
        self.G2 = _Group()
        self.G3 = _Group()
        self.G4 = _Group()
        self.G5 = _Group()
        self.G6 = _Group()
        self.G7 = _Group()
        self.G8 = _Group()
        self.G9 = _Group()
        self.G10 = _Group()
        self.G11 = _Group()
        self.G12 = _Group()
        self.G13 = _Group()
        self.G14 = _Group()
        self.G15 = _Group()


class _MessageTypeDInf(_MessageType):
    def reset(self):
        _MessageType.reset(self)

    def __init__(self, t, n):
        _MessageType.__init__(self, t, n, 2)
        self.G1 = _Group()
        self.G2 = _Group()


class _MessageTypeRtrp(_MessageType):
    def reset(self):
        _MessageType.reset(self)

    def __init__(self, t, n):
        _MessageType.__init__(self, t, n, 27)
        self.G1 = _Group()
        self.G2 = _Group()
        self.G3 = _Group()
        self.G4 = _Group()
        self.G5 = _Group()
        self.G6 = _Group()
        self.G7 = _Group()
        self.G8 = _Group()
        self.G9 = _Group()
        self.G10 = _Group()
        self.G11 = _Group()
        self.G12 = _Group()
        self.G13 = _Group()
        self.G14 = _Group()
        self.G15 = _Group()
        self.G16 = _Group()
        self.G17 = _Group()
        self.G18 = _Group()
        self.G19 = _Group()
        self.G20 = _Group()
        self.G21 = _Group()
        self.G22 = _Group()
        self.G23 = _Group()
        self.G24 = _Group()
        self.G25 = _Group()
        self.G26 = _Group()
        self.G27 = _Group()


class _MessageTypeEvent(_MessageType):
    def reset(self):
        _MessageType.reset(self)

    def __init__(self, t, n):
        _MessageType.__init__(self, t, n, 60)
        self.G1 = _Group()
        self.G2 = _Group()
        self.G3 = _Group()
        self.G4 = _Group()
        self.G5 = _Group()
        self.G6 = _Group()
        self.G7 = _Group()
        self.G8 = _Group()
        self.G9 = _Group()
        self.G10 = _Group()
        self.G11 = _Group()
        self.G12 = _Group()
        self.G13 = _Group()
        self.G14 = _Group()
        self.G15 = _Group()
        self.G16 = _Group()
        self.G17 = _Group()
        self.G18 = _Group()
        self.G19 = _Group()
        self.G20 = _Group()
        self.G21 = _Group()
        self.G22 = _Group()
        self.G23 = _Group()
        self.G24 = _Group()
        self.G25 = _Group()
        self.G26 = _Group()
        self.G27 = _Group()
        self.G28 = _Group()
        self.G29 = _Group()
        self.G30 = _Group()
        self.G31 = _Group()
        self.G32 = _Group()
        self.G33 = _Group()
        self.G34 = _Group()
        self.G35 = _Group()
        self.G36 = _Group()
        self.G37 = _Group()
        self.G38 = _Group()
        self.G39 = _Group()
        self.G40 = _Group()
        self.G41 = _Group()
        self.G42 = _Group()
        self.G43 = _Group()
        self.G44 = _Group()
        self.G45 = _Group()
        self.G46 = _Group()
        self.G47 = _Group()
        self.G48 = _Group()
        self.G49 = _Group()
        self.G50 = _Group()
        self.G51 = _Group()
        self.G52 = _Group()
        self.G53 = _Group()
        self.G54 = _Group()
        self.G55 = _Group()
        self.G56 = _Group()
        self.G57 = _Group()
        self.G58 = _Group()
        self.G59 = _Group()
        self.G60 = _Group()


class _MessageTypeData(_MessageType):
    def reset(self):
        _MessageType.reset(self)

    def __init__(self, t, n):
        _MessageType.__init__(self, t, n, 11)
        self.G1 = _Group()
        self.G2 = _Group()
        self.G3 = _Group()
        self.G4 = _Group()
        self.G5 = _Group()
        self.G6 = _Group()
        self.G7 = _Group()
        self.G8 = _Group()
        self.G9 = _Group()
        self.G10 = _Group()
        self.G11 = _Group()


class _MessageTypeCrash(_MessageType):
    def reset(self):
        _MessageType.reset(self)

    def __init__(self, t, n):
        _MessageType.__init__(self, t, n, 5)
        self.G1 = _Group()
        self.G2 = _Group()
        self.G3 = _Group()
        self.G4 = _Group()
        self.G5 = _Group()


class _MessageTypeCInf(_MessageType):
    def reset(self):
        _MessageType.reset(self)

    def __init__(self, t, n):
        _MessageType.__init__(self, t, n, 5)
        self.G1 = _Group()
        self.G2 = _Group()
        self.G3 = _Group()
        self.G4 = _Group()
        self.G5 = _Group()


class _MessageTypeUpdate(_MessageType):
    def reset(self):
        _MessageType.reset(self)

    def __init__(self, t, n):
        _MessageType.__init__(self, t, n, 5)
        self.G1 = _Group()
        self.G2 = _Group()
        self.G3 = _Group()
        self.G4 = _Group()
        self.G5 = _Group()


class _MessageTypeConnective(_MessageType):
    def reset(self):
        _MessageType.reset(self)

    def __init__(self, t, n):
        _MessageType.__init__(self, t, n, 5)
        self.G1 = _Group()
        self.G2 = _Group()
        self.G3 = _Group()
        self.G4 = _Group()
        self.G5 = _Group()


class _Project:
    class _Support:
        class _IBattery:
            def __init__(self):
                self.valid = False
                self.charge = 'no'
                self.name = 'Internal Battery'

        class _Bluetooth:
            def __init__(self):
                self.valid = False
                self.name = 'Bluetooth'

        class _BLE:
            def __init__(self):
                self.valid = False
                self.name = 'BLE'

        class _IO:
            def __init__(self):
                self.valid = False
                self.name = 'IO'

        # RS232, RS485
        class _Serial:
            def __init__(self, name):
                self.valid = False
                self.name = name

        class _1wire:
            def __init__(self, _type):
                self.valid = False
                self.name = "1-wire"
                self.type = _type

        class _Call:
            def __init__(self):
                self.valid = False
                self.name = 'Call'

        class _SMS:
            def __init__(self):
                self.valid = False
                self.name = 'SMS'

        class _OBD:
            def __init__(self):
                self.valid = False
                self.name = 'OBD'

        class _CAN:
            def __init__(self):
                self.valid = False
                self.name = 'CAN'
                self.Mask = _Mask()

        class _Tachograph:
            def __init__(self):
                self.valid = False
                self.name = 'Tachograph'
                self.Mask = _Mask()

        class _Versions:
            def __init__(self):
                self.valid = False
                self.name = 'Versions'
                self.Mask = _Mask()

        class _Format:
            def __init__(self):
                self.valid = False
                self.name = 'Message Format'
                self.Mask = _Mask()

        class _MBattery:
            def __init__(self):
                self.valid = False
                self.charge = 'no'
                self.name = 'Main Battery'

        class _Hardwares:
            def __init__(self):
                self.valid = False
                self.name = 'Hardwares'
                self.Mask = _Mask()

        class _Updates:
            def __init__(self):
                self.valid = False
                self.name = 'Updates'
                self.Mask = _Mask()

        class _3G:
            def __init__(self, _type):
                self.valid = False
                self.name = "3G"
                self.type = _type

        class _2G:
            def __init__(self, _type):
                self.valid = False
                self.name = "2G"
                self.type = _type

        class _LTE:
            def __init__(self):
                self.valid = False
                self.name = "LTE"
                self.cat1_name = ""
                self.cat4_name = ""
                self.catM1_name = ""
                self.cat1 = False
                self.cat4 = False
                self.catM1 = False

        def reset(self):
            self.IBattery.valid = False  # 内电池
            self.LTE.cat1 = False
            self.LTE.cat4 = False  # 4G network
            self.LTE.catM1 = False
            self.S_2G.valid = False
            self.S_3G.valid = False
            self.Bluetooth.valid = False
            self.BLE.valid = False  # 省电蓝牙
            self.IO.valid = False  # 输入输出口功能
            self.RS232.valid = False  # 副串口
            self.RS485.valid = False
            self.oneWire.valid = False
            self.Call.valid = False
            self.SMS.valid = False
            self.OBD.valid = False
            self.CAN.valid = False
            self.CAN.Mask.reset()
            self.Tachograph.valid = False
            self.Versions.valid = False  # 版本号 其中mask用来制定项目中包含各模块的版本号 BB BLE MCU 等
            self.Format.valid = False  # 支持的报文格式 ASCII, HEX
            self.PowerButton.valid = False  # 电源按钮
            self.IP67.valid = False
            self.MBattery.valid = False  # 主电池
            self.Interfaces = ''
            self.Hardwares.valid = False
            self.Updates.valid = False

        def __init__(self):
            self.IBattery = self._IBattery()  # 内电池
            self.LTE = self._LTE()  # 4G network
            self.S_2G = self._2G("EGPRS/GSM")
            self.S_3G = self._3G("WCDMA")
            self.Bluetooth = self._Bluetooth()  # 经典蓝牙功能
            self.BLE = self._BLE()  # 省电蓝牙
            self.IO = self._IO()  # 输入输出口功能
            self.RS232 = self._Serial("RS232")  # 副串口
            self.RS485 = self._Serial("RS485")
            self.oneWire = self._Serial('')
            self.Call = self._Call()  # 语音通话功能
            self.SMS = self._SMS()  # SMS
            self.OBD = self._OBD()  # OBD 接口
            self.CAN = self._CAN()
            self.Tachograph = self._Tachograph()
            self.Versions = self._Versions()  # 版本号 其中mask用来制定项目中包含各模块的版本号 BB BLE MCU 等
            self.Format = self._Format()  # 支持的报文格式 ASCII, HEX
            self.PowerButton = Valid()  # 电源按钮
            self.IP67 = Valid()
            self.MBattery = self._MBattery()  # 主电池
            self.Interfaces = ''
            self.Hardwares = self._Hardwares()
            self.Updates = self._Updates()

        def show(self):
            show_string = self.IBattery.name + " " + str(self.IBattery.valid) + " " + self.IBattery.charge + "\n" \
                          + self.Bluetooth.name + " " + str(self.Bluetooth.valid) + "\n" \
                          + self.IO.name + " " + str(self.IO.valid) + "\n" \
                          + self.RS232.name + " " + str(self.RS232.valid) + "\n" \
                          + self.OBD.name + " " + str(self.OBD.valid) + "\n" \
                          + self.Format.name + " " + str(self.Format.valid) + " " + self.Format.Mask.Bits + "\n" \
                          + self.Versions.name + " " + str(self.Versions.valid) + " " + self.Versions.Mask.Bits + "\n"
            print(show_string)

    class _AirProtocol:  # 空中接口协议, 即通常说的 @Track 协议.
        class _Commands:
            def reset(self):
                self.valid = False
                self.cmd_count = 0
                self.param_list.clear()
                ms = vars(self)
                for k in ms.keys():
                    # command name must consist of three capital letters.
                    # that is what the regular expression means
                    if re.match(r"(?<![A-Z])[A-Z]{3}(?![A-Z])", k):
                        eval("self." + k + ".reset()")

            def __init__(self):
                self.valid = False
                self.cmd_count = 0
                self.param_list = []
                self.description_list = []
                self.BSI = CMDc()
                self.SRI = CMDc()
                self.QSS = CMDc()
                self.MQT = CMDc()
                self.OWL = CMDc()
                self.FTP = CMDc()
                self.MSI = CMDc()
                self.MSF = CMDc()
                self.TLS = CMDc()
                self.CFG = CMDc()
                self.DOG = CMDc()
                self.GAM = CMDc()
                self.HMC = CMDc()
                self.HRM = CMDc()
                self.OWH = CMDc()
                self.PDS = CMDc()
                self.PIN = CMDc()
                self.RCS = CMDc()
                self.RAS = CMDc()
                self.RTP = CMDc()
                self.LTP = CMDc()
                self.TMA = CMDc()
                self.WLT = CMDc()
                self.BTS = CMDc()
                self.BAS = CMDc()
                self.BID = CMDc()
                self.AEX = CMDc()
                self.SVR = CMDc()
                self.FRI = CMDc()
                self.FFC = CMDc()
                self.ASC = CMDc()
                self.CRA = CMDc()
                self.BZA = CMDc()
                self.DUC = CMDc()
                self.GEO = CMDc()
                self.PEO = CMDc()
                self.PEG = CMDc()
                self.HBM = CMDc()
                self.IDL = CMDc()
                self.JBS = CMDc()
                self.JDC = CMDc()
                self.MON = CMDc()
                self.RMD = CMDc()
                self.SIM = CMDc()
                self.SOS = CMDc()
                self.SPA = CMDc()
                self.SPD = CMDc()
                self.SSR = CMDc()
                self.TOW = CMDc()
                self.AIS = CMDc()
                self.DIS = CMDc()
                self.DOS = CMDc()
                self.OUT = CMDc()
                self.EPS = CMDc()
                self.GDO = CMDc()
                self.IOB = CMDc()
                self.ROS = CMDc()
                self.AUS = CMDc()
                self.CDA = CMDc()
                self.CMS = CMDc()
                self.TAP = CMDc()
                self.DAT = CMDc()
                self.TKS = CMDc()
                self.EFS = CMDc()
                self.FSC = CMDc()
                self.IDA = CMDc()
                self.IDC = CMDc()
                self.IDS = CMDc()
                self.TTR = CMDc()
                self.UDT = CMDc()
                self.UFS = CMDc()
                self.URT = CMDc()
                self.WRT = CMDc()
                self.ACD = CMDc()
                self.IEX = CMDc()
                self.OEX = CMDc()
                self.TMP = CMDc()
                self.CAN = CMDc()
                self.CLT = CMDc()
                self.CFU = CMDc()
                self.AVS = CMDc()
                self.VVS = CMDc()
                self.VMS = CMDc()
                self.FVR = CMDc()
                self.UPC = CMDc()
                self.CMD = CMDc()
                self.UDF = CMDc()
                self.RTO = CMDc()
                self.SMS = CMDc()
                self.SWL = CMDc()
                self.HUM = CMDc()
                self.SLM = CMDc()
                self.IGM = CMDc()
                self.EMG = CMDc()
                self.BTD = CMDc()
                self.ACJ = CMDc()
                self.LBC = CMDc()
                self.CDS = CMDc()
                self.UPD = CMDc()
                self.MCT = CMDc()
                self.GNA = CMDc()
                self.TEM = CMDc()
                self.NMD = CMDc()
                self.SFM = CMDc()
                self.FKS = CMDc()
                self.EMS = CMDc()
                self.CCL = CMDc()
                self.TPM = CMDc()
                self.ATC = CMDc()
                self.BLP = CMDc()
                self.GEJ = CMDc()
                self.TRI = CMDc()
                self.SNS = CMDc()
                self.DUE = CMDc()
                self.PSM = CMDc()
                self.COA = CMDc()

        class _ASCIIReport:
            def reset(self):
                self.valid = False
                self.posi.reset()
                self.dinf.reset()
                self.rtrp.reset()
                self.event.reset()
                self.data.reset()
                self.crash.reset()
                self.cinf.reset()
                self.updr.reset()
                self.conr.reset()

            def __init__(self):
                self.valid = False
                # position related
                self.posi = _MessageTypePosi(POSITION, 'posi')
                # device information
                self.dinf = _MessageTypeDInf(DEVICE_INFO, 'dinf')
                # real time report
                self.rtrp = _MessageTypeRtrp(REALTIME, 'rtrp')
                # event report
                self.event = _MessageTypeEvent(EVENT_REPORT, 'event')
                # data report(include transparent data transmission, UART Data Transfer)
                self.data = _MessageTypeData(DATA_REPORT, 'data')
                # crash data report (include crash data packet, acceleration data packet)
                self.crash = _MessageTypeCrash(CRASH_DATA, 'crash')
                # canbus information
                self.cinf = _MessageTypeCInf(CAN_INFO, 'cinf')
                # update report
                self.updr = _MessageTypeUpdate(UPDATE, 'updr')
                # connective report(heartbeat, server acknowledgement)
                self.conr = _MessageTypeConnective(CONNECTIVE, 'conr')

        class _HEXReport:
            def reset(self):
                self.valid = False
                self.posi.reset()
                self.dinf.reset()
                # self.rtrp.reset()
                self.event.reset()
                self.data.reset()
                self.crash.reset()
                self.cinf.reset()
                # self.updr.reset()
                self.conr.reset()

            def __init__(self):
                self.valid = False
                # position related
                self.posi = _MessageTypePosi(POSITION, 'posi')
                # device information
                self.dinf = _MessageTypeDInf(DEVICE_INFO, 'dinf')
                # real time report
                # self.rtrp = _MessageTypeRtrp(REALTIME, 'rtrp')
                # event report
                self.event = _MessageTypeEvent(EVENT_REPORT, 'event')
                # data report(include transparent data transmission, UART Data Transfer)
                self.data = _MessageTypeData(DATA_REPORT, 'data')
                # crash data report (include crash data packet, acceleration data packet)
                self.crash = _MessageTypeCrash(CRASH_DATA, 'crash')
                # canbus information
                self.cinf = _MessageTypeCInf(CAN_INFO, 'cinf')
                # update report
                # self.updr = _MessageTypeUpdate(UPDATE, 'updr')
                # connective report(heartbeat, server acknowledgement)
                self.conr = _MessageTypeConnective(CONNECTIVE, 'conr')

        def reset(self):
            self.valid = False
            self.Ascii.reset()
            self.Hex.reset()

        def __init__(self):
            self.valid = True
            self.ver = 1.00  # 当前协议版本
            self.Commands = self._Commands()
            self.Ascii = self._ASCIIReport()
            self.Hex = self._HEXReport()

    def __init__(self):
        self.root = '0100'  # ROOT 协议版本
        self.name = 'Project Name'  # Project name
        self.password = 'queclink'  # 默认密码
        self.device_type = 'Device Type'  # 设备类型
        self.sub_title = 'LTE Cat-1/LTE Cat-4/LTE/GNSS Tracker'  # 副标题
        self.customer = ''
        self.qldbg = ''
        self.qble = ''
        self.Support = self._Support()
        self.AirProtocol = self._AirProtocol()


Project = _Project()
