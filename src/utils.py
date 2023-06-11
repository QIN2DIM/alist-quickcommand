# -*- coding: utf-8 -*-
# Time       : 2023/6/12 3:48
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
import ctypes
import logging

__all__ = ["logger", "redirect_mounted_drive"]
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s::%(funcName)s::%(lineno)d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def get_drives():
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    drives = [
        chr(letter) + ":\\" for letter in range(65, 91) if bitmask & 1 << (letter - 65)
    ]
    return drives


def redirect_mounted_drive() -> str:
    # Get Windows all available drive letters
    drives = get_drives()

    # Drives and their free capacity
    default_mounted_drive = ""
    fgb_drive = [1024**2, default_mounted_drive]

    # By default, RaiDrive displays a capacity of up to 8PB for the mounted drive,
    # which far exceeds the capacity of consumer-grade hard drives.
    # Therefore, it can be assumed that the mounted drive
    # is the one with the highest remaining capacity among all host drives.
    for drive in drives:
        free_bytes = ctypes.c_ulonglong(0)
        total_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(
            ctypes.c_wchar_p(drive),
            None,
            ctypes.pointer(total_bytes),
            ctypes.pointer(free_bytes),
        )
        free_gb = free_bytes.value / (1024**3)

        # Filter out the drives with the highest free capacity
        if free_gb > fgb_drive[0]:
            fgb_drive = [free_gb, drive]

    return fgb_drive[-1]
