#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import tempfile

import requests
import win32api
import win32con
import win32gui


class Wallpaper:
    def __init__(self):
        self.image = os.path.join(tempfile.gettempdir(), "wallpaper.jpg")

    def crawl(self):
        url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=8"
        image = random.choice(requests.get(url).json()["images"])["urlbase"]
        imageURL = f"https://www.bing.com{image}_UHD.jpg"
        with open(self.image, "wb") as f:
            f.write(requests.get(imageURL).content)
        return self

    def setup(self):
        keyex = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(keyex, "WallpaperStyle", 0, win32con.REG_SZ, "10")
        win32api.RegSetValueEx(keyex, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, self.image, win32con.SPIF_SENDWININICHANGE)
        """
        WallpaperStyle = 10 and TileWallpaper = 0 make wallpaper filled
        WallpaperStyle = 6  and TileWallpaper = 0 make wallpaper fitted
        WallpaperStyle = 2  and TileWallpaper = 0 make wallpaper stretched
        WallpaperStyle = 0  and TileWallpaper = 0 make wallpaper centered
        WallpaperStyle = 0  and TileWallpaper = 1 make wallpaper tiled
        """


if __name__ == "__main__":
    wallpaper = Wallpaper()
    wallpaper.crawl().setup()
