#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile
from datetime import datetime, timezone

import requests
import win32api
import win32con
import win32gui
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def get_time_interval(hour, minute):
    hour = int(hour) - 1
    minute = (((int(minute) - 30) % 60) // 15) * 15
    start_time = hour * 10000 + minute * 100
    end_time = start_time + 1459
    return (f"{start_time:06d}", f"{end_time:06d}")


class Wallpaper:
    def __init__(self):
        self.image = os.path.join(tempfile.gettempdir(), "wallpaper.jpg")

    def crawl(self):
        now = datetime.now()
        utc_now = now.astimezone(timezone.utc)

        year = utc_now.year
        month = "{:02d}".format(utc_now.month)
        day = "{:02d}".format(utc_now.day)
        hour = "{:02d}".format(utc_now.hour)
        minute = "{:02d}".format(utc_now.minute)
        start_time, end_time = get_time_interval(hour, minute)
        timestamp = f"{year}{month}{day}{start_time}_{year}{month}{day}{end_time}"

        picture = f"http://img.nsmc.org.cn/CLOUDIMAGE/FY4B/AGRI/GCLR/DISK/FY4B-_AGRI--_N_DISK_1050E_L2-_GCLR_MULT_NOM_{timestamp}_1000M_V0001.JPG"
        res = requests.get(picture)
        with open(self.image, "wb") as f:
            f.write(res.content)
        return self

    def zoom(self):
        h = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        Image.open(self.image).resize((h - 100, h - 100), Image.Resampling.LANCZOS).save(self.image)
        return self

    def setup(self):
        keyex = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(keyex, "WallpaperStyle", 0, win32con.REG_SZ, "0")
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
    wallpaper.crawl().zoom().setup()
