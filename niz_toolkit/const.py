VID = 0x0483  # 1155
PID_COLLECTION = {
    0x512A: "atom66",
    0x5129: "micro84",
    0x5235: "mini84",
}


class Command:
    READ_SERIAL = 0x10
    READ_VERSION = 0xF9
    READ_COUNTER = 0xE3

    KEY_LOCK = 0xD9  # 0xd9 0x00 lock / 0xd9 0x01 unlock
    CALIB = 0xDA  # ?
    CALIB_INIT = 0xDB
    CALIB_PRESS = 0xDD
    CALIB_PRESS_DONE = 0xDE

    KEYMAP_DATA = 0xF0
    KEYMAP_WRITE = 0xF1
    KEYMAP_READ = 0xF2
    KEYMAP_DATA_END = 0xF6

    # -- unknown --
    # XXX_DATA = 0xe0  # maybe macro
    # READ_XXX = 0xe2  # maybe macro
    # XXX_END = 0xe6
