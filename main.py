# -*- coding: utf-8 -*-
# Time       : 2023/6/12 3:48
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
from pathlib import Path

from src.scaffold import start_service, stop_service, alist_manage

# ↓ Modify here ↓
PATH_TO_ALIST = Path("D:\\path_to_alist\\alist.exe")
PATH_TO_RAIDRIVE = Path("D:\\path_to_RaiDrive\\RaiDrive.exe")
# ↑ Modify here ↑

if __name__ == "__main__":
    start_service(PATH_TO_ALIST, PATH_TO_RAIDRIVE)
    # stop_service(PATH_TO_ALIST, PATH_TO_RAIDRIVE)
    # alist_manage(PATH_TO_ALIST)
