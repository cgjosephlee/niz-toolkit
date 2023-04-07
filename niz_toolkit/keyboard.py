import logging
import struct
from typing import Optional

import hid

from . import const

logger = logging.getLogger(__name__)


def find_device():
    path, PID, PNAME = None, None, None
    for device_dict in hid.enumerate(vendor_id=const.VID):
        if device_dict["interface_number"] == 1:
            logger.debug(device_dict)
            path = device_dict["path"]
            PID = device_dict["product_id"]
            PNAME = device_dict["product_string"]
            # assume only one
            break
    if not PID:
        logger.error(
            "No device with Niz vendor_id (1155) is found. Make sure your keyboard is on Win mode."
        )
    return path, PID, PNAME


class Keyboard:
    def __init__(self, path: bytes, PID: Optional[int]=None, PNAME: Optional[str]=None) -> None:
        self.device = hid.device()
        try:
            self.device.open_path(path)
        except OSError:
            logger.fatal(f"Failed to open device ({path.decode()}).")
            self.device.close()
            raise
        # self.device.set_nonblocking(True)
        self.PID = PID
        self.PNAME = PNAME
        self.locked = False

    @property
    def model(self):
        if self.PNAME:
            return self.PNAME
        else:
            return const.PID_COLLECTION.get(self.PID, f"{self.PID}")

    @property
    def version(self):
        return self.read_version()

    def read_version(self) -> Optional[str]:
        """Read firmware version."""
        self.send(const.Command.READ_VERSION)
        data = self.read(64)
        ver_str = None
        if data:
            # 2 bytes command, 62 bytes string
            _, ver = struct.unpack("H62s", bytes(data))
            ver_str = ver.decode()
        return ver_str

    def lock(self):
        self.send(const.Command.KEY_LOCK)
        self.locked = True
        logger.info("Keyboard locked.")

    def unlock(self):
        self.send(const.Command.KEY_LOCK, "/x01")
        self.locked = False
        logger.info("Keyboard unlocked.")

    def calib_init(self):
        if self.locked:
            self.send(const.Command.CALIB_INIT)
            logger.info("Calibrate init done.")
        else:
            logger.error("Keyboard is not locked!")

    def calib_press(self):
        if self.locked:
            self.send(const.Command.CALIB_PRESS)
            data = self.read()
            logger.info("Calibrate one done.")
        else:
            logger.error("Keyboard is not locked!")

    def send(self, cmd: int, data: str="") -> int:
        """
        Send command to keyboard.
        Format: 1 byte 0, 2 bytes command, 62 bytes data
        """
        logger.debug(f"send: 0x{cmd:02X}, {data}")
        buf = struct.pack("!bH62s", 0, cmd, data.encode())
        result = self.device.write(buf)
        logger.debug(f"write ({result}): {buf.hex(':')}")
        return result

    def read(self, num=64, timeout=100) -> Optional[list[int]]:
        """
        Read data from hid device.
        Format: 2 bytes command, 62 bytes data
        """
        data = None
        try:
            data = self.device.read(num, timeout)
            logger.debug(f"read ({len(data)}): {bytes(data).hex(':')}")
        except IOError as e:
            logger.error(e)
        return data

    def close(self):
        self.device.close()
        logger.debug("Device closed.")
