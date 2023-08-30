#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile

import requests
import win32api
import win32con
import win32gui
from PIL import Image


class Wallpaper:
    def __init__(self):
        self.image = os.path.join(tempfile.gettempdir(), "wallpaper.jpg")

    def crawl(self):
        picture = "https://img.nsmc.org.cn/CLOUDIMAGE/FY4A/MTCC/FY4A_CHINA.JPG"
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
        win32api.RegSetValueEx(keyex, "WallpaperStyle", 0, win32con.REG_SZ, "10")
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
