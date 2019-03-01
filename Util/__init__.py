import re
from enum import IntEnum

DevMdl = IntEnum('DevMdl', ["LWT", "TOPIC", "FULL_TOPIC", "FRIENDLY_NAME", "MODULE", "FIRMWARE", "CORE", "MAC", "IP", "SSID", "BSSID", "CHANNEL", "RSSI", "LINKCOUNT", "DOWNTIME", "UPTIME", "RESTART_REASON", "POWER", "LOADAVG", "TELEPERIOD", "MODULE_ID", "OTA_URL"], start=0)
CnsMdl = IntEnum('CnsMdl', ["TIMESTAMP", "TOPIC", "FRIENDLY_NAME", "DESCRIPTION", "PAYLOAD", "KNOWN"], start=0)

initial_queries = [None, 1, 2, 3, 5, 8, 11]

modules = {
    1: 'Sonoff Basic (01)',
    2: 'Sonoff RF (02)',
    4: 'Sonoff TH (04)',
    5: 'Sonoff Dual (05)',
    39: 'Sonoff Dual R2 (39)',
    6: 'Sonoff Pow (06)',
    43: 'Sonoff Pow R2 (43)',
    7: 'Sonoff 4CH (07)',
    23: 'Sonoff 4CH Pro (23)',
    41: 'Sonoff S31 (41)',
    8: 'Sonoff S2X (08)',
    10: 'Sonoff Touch (10)',
    28: 'Sonoff T1 1CH (28)',
    29: 'Sonoff T1 2CH (29)',
    30: 'Sonoff T1 3CH (30)',
    11: 'Sonoff LED (11)',
    22: 'Sonoff BN-SZ (22)',
    26: 'Sonoff B1 (26)',
    9: 'Slampher (09)',
    21: 'Sonoff SC (21)',
    44: 'Sonoff iFan02 (44)',
    25: 'Sonoff Bridge (25)',
    3: 'Sonoff SV (03)',
    19: 'Sonoff Dev (19)',
    12: '1 Channel (12)',
    13: '4 Channel (13)',
    14: 'Motor C/AC (14)',
    15: 'ElectroDragon (15)',
    16: 'EXS Relay(s) (16)',
    31: 'Supla Espablo (31)',
    35: 'Luani HVIO (35)',
    33: 'Yunshan Relay (33)',
    17: 'WiOn (17)',
    46: 'Shelly 1 (46)',
    47: 'Shelly 2 (47)',
    45: 'BlitzWolf SHP (45)',
    52: 'Teckin (52)',
    59: 'Teckin US (59)',
    53: 'AplicWDP303075 (53)',
    55: 'Gosund SP1 v23 (55)',
    57: 'SK03 Outdoor (57)',
    49: 'Neo Coolcam (49)',
    51: 'OBI Socket (51)',
    60: 'Manzoku strip (60)',
    50: 'ESP Switch (50)',
    54: 'Tuya Dimmer (54)',
    56: 'ARMTR Dimmer (56)',
    58: 'PS-16-DZ (58)',
    20: 'H801 (20)',
    34: 'MagicHome (34)',
    37: 'Arilux LC01 (37)',
    40: 'Arilux LC06 (40)',
    38: 'Arilux LC11 (38)',
    42: 'Zengge WF017 (42)',
    24: 'Huafan SS (24)',
    36: 'KMC 70011 (36)',
    27: 'AiLight (27)',
    48: 'Xiaomi Philips (48)',
    32: 'Witty Cloud (32)',
    18: 'Generic (18)',
}
gpio = {
    "0": "None (0)",
    "17": "Button1 (17)",
    "90": "Button1n (90)",
    "122": "Button1i (122)",
    "126": "Button1in (126)",
    "18": "Button2 (18)",
    "91": "Button2n (91)",
    "123": "Button2i (123)",
    "127": "Button2in (127)",
    "19": "Button3 (19)",
    "92": "Button3n (92)",
    "124": "Button3i (124)",
    "128": "Button3in (128)",
    "20": "Button4 (20)",
    "93": "Button4n (93)",
    "125": "Button4i (125)",
    "129": "Button4in (129)",
    "9": "Switch1 (9)",
    "82": "Switch1n (82)",
    "10": "Switch2 (10)",
    "83": "Switch2n (83)",
    "11": "Switch3 (11)",
    "84": "Switch3n (84)",
    "12": "Switch4 (12)",
    "85": "Switch4n (85)",
    "13": "Switch5 (13)",
    "86": "Switch5n (86)",
    "14": "Switch6 (14)",
    "87": "Switch6n (87)",
    "15": "Switch7 (15)",
    "88": "Switch7n (88)",
    "16": "Switch8 (16)",
    "89": "Switch8n (89)",
    "21": "Relay1 (21)",
    "29": "Relay1i (29)",
    "22": "Relay2 (22)",
    "30": "Relay2i (30)",
    "23": "Relay3 (23)",
    "31": "Relay3i (31)",
    "24": "Relay4 (24)",
    "32": "Relay4i (32)",
    "25": "Relay5 (25)",
    "33": "Relay5i (33)",
    "26": "Relay6 (26)",
    "34": "Relay6i (34)",
    "27": "Relay7 (27)",
    "35": "Relay7i (35)",
    "28": "Relay8 (28)",
    "36": "Relay8i (36)",
    "54": "Led3 (54)",
    "58": "Led3i (58)",
    "55": "Led4 (55)",
    "59": "Led4i (59)",
    "42": "Counter1 (42)",
    "94": "Counter1n (94)",
    "43": "Counter2 (43)",
    "95": "Counter2n (95)",
    "44": "Counter3 (44)",
    "96": "Counter3n (96)",
    "45": "Counter4 (45)",
    "97": "Counter4n (97)",
    "5": "I2C SCL (5)",
    "6": "I2C SDA (6)",
    "1": "DHT11 (1)",
    "2": "AM2301 (2)",
    "3": "SI7021 (3)",
    "4": "DS18x20 (4)",
    "7": "WS2812 (7)",
    "8": "IRsend (8)",
    "51": "IRrecv (51)",
    "105": "RFSend (105)",
    "106": "RFrecv (106)",
    "73": "SR04 Tri (73)",
    "74": "SR04 Ech (74)",
    "102": "HX711 SCK (102)",
    "103": "HX711 DAT (103)",
    "71": "SerBr Tx (71)",
    "72": "SerBr Rx (72)",
    "60": "MHZ Tx (60)",
    "61": "MHZ Rx (61)",
    "64": "SAir Tx (64)",
    "65": "SAir Rx (65)",
    "101": "SDS0X1 Tx (101)",
    "70": "SDS0X1 Rx (70)",
    "62": "PZEM0XX Tx (62)",
    "63": "PZEM004 Rx (63)",
    "98": "PZEM016 Rx (98)",
    "99": "PZEM017 Rx (99)",
    "69": "PMS5003 (69)",
    "104": "TX20 (104)",
    "107": "Tuya Tx (107)",
    "108": "Tuya Rx (108)"
    }

class found_obj(object):
    def __init__(self, d):
        self.__dict__ = d

    def __repr__(self):
        return "PREFIX={},TOPIC={},REPLY={}".format(self.__dict__.get('prefix'), self.__dict__.get('topic'), self.__dict__.get('reply'))


def match_topic(full_topic, topic):
    full_topic = full_topic + "(?P<reply>.*)"
    full_topic = full_topic.replace("%topic%", "(?P<topic>.*?)")
    full_topic = full_topic.replace("%prefix%", "(?P<prefix>.*?)")
    return re.fullmatch(full_topic, topic)