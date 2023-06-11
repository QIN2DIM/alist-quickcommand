# -*- coding: utf-8 -*-
# Time       : 2023/6/12 3:49
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
import os
import subprocess
import sys
import time
import typing
import webbrowser
from abc import ABC, abstractmethod
from pathlib import Path

from utils import logger, redirect_mounted_drive

__all__ = ["Alist", "RaiDrive", "start_service", "stop_service", "alist_manage"]


class Service(ABC):
    _INIT_CWD = os.getcwd()

    def __init__(self, path: typing.Union[str, Path]):
        if isinstance(path, str):
            path = Path(path)
        self._path = path
        if sys.platform != "win32":
            logger.critical(
                f"[CRITICAL] only supports running under Windows operating systems"
            )
            sys.exit(0)
        if not self._path.exists() or not self._path.suffix == ".exe":
            logger.critical(f"[CRITICAL] DriveNotFound - path={self._path}")
            sys.exit(0)

        # [executor].exe
        self._exe = self._path.name

    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def stop(self):
        ...

    def _executor(self, command):
        os.chdir(self._path.parent)
        logger.debug(f"{command=}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        logger.info(result.stdout if result.returncode == 0 else result.stderr)
        os.chdir(self._INIT_CWD)


class Alist(Service):
    _START = "start"
    _STOP = "stop"
    _SERVER = "server"
    _ADMIN = "admin"

    def start(self):
        return self._executor(f"{self._exe} {self._START}")

    def stop(self):
        return self._executor(f"{self._exe} {self._STOP}")


class RaiDrive(Service):
    def start(self):
        os.startfile(self._path)
        logger.info("Started RaiDrive service")

        times = 8
        for i in range(times):
            time.sleep(1)
            mounted_drive = redirect_mounted_drive()
            if not mounted_drive:
                logger.info(f"[{i + 1}/{times}]retry to start CloudDrive")
                continue
            fp_drive = Path(mounted_drive)
            if fp_drive.exists():
                os.startfile(fp_drive)
                logger.info("Started RaiDrive Local Mount Disk")
                break

    def stop(self):
        return self._executor(f"taskkill -im {self._exe} -t -f >nul")


def start_service(
        path_to_alist: typing.Union[str, Path], path_to_raidrive: typing.Union[str, Path]
):
    Alist(path_to_alist).start()
    RaiDrive(path_to_raidrive).start()


def stop_service(
        path_to_alist: typing.Union[str, Path], path_to_raidrive: typing.Union[str, Path]
):
    Alist(path_to_alist).stop()
    RaiDrive(path_to_raidrive).stop()


def alist_manage(path_to_alist: typing.Union[str, Path]):
    Alist(path_to_alist).start()
    webbrowser.open("http://127.0.0.1:5244/@manage")
