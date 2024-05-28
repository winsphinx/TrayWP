#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile
from datetime import datetime, timedelta, timezone

import requests
import win32api
import win32con
import win32gui
from PIL import Image


class Wallpaper:
    def __init__(self):
        self.image = os.path.join(tempfile.gettempdir(), "wallpaper.jpg")

    def crawl(self):
        now = datetime.now()
        utc_now = now.astimezone(timezone.utc) - timedelta(minutes=30)  # 卫星云图约滞后半小时

        year = utc_now.year
        month = "{:02d}".format(utc_now.month)
        day = "{:02d}".format(utc_now.day)
        hour = "{:02d}".format(utc_now.hour)
        picture = f"https://img.nsmc.org.cn/CLOUDIMAGE/GEOS/MOS/IRX/PIC/GBAL/{year}{month}{day}/GEOS_IMAGR_GBAL_L2_MOS_IRX_GLL_{year}{month}{day}_{hour}00_10KM_MS.jpg"
        res = requests.get(picture)
        with open(self.image, "wb") as f:
            f.write(res.content)
        return self

    def zoom(self):
        w = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        h = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        Image.open(self.image).resize((w, h), Image.Resampling.LANCZOS).save(self.image)
        return self

    def setup(self):
        keyex = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(keyex, "WallpaperStyle", 0, win32con.REG_SZ, "2")
        win32api.RegSetValueEx(keyex, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, self.image, win32con.SPIF_SENDWININICHANGE)
        """
        | WallpaperStyle | TileWallpaper | style     |
        |----------------+---------------+-----------|
        |             10 |             0 | filled    |
        |              6 |             0 | fitted    |
        |              2 |             0 | stretched |
        |              0 |             0 | centered  |
        |              0 |             1 | tiled     |
        """


if __name__ == "__main__":
    wallpaper = Wallpaper()
    wallpaper.crawl().zoom().setup()
