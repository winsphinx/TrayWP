#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import tempfile

import requests
import win32api
import win32con
import win32gui
from lxml import etree


class Wallpaper:
    def __init__(self):
        self.image = os.path.join(tempfile.gettempdir(), "wallpaper.jpg")

    def crawl(self):
        base_url = "https://www.toopic.cn"  # 基础页
        page_url = f"{base_url}/dnbz/?q=--{random.choice([65, 70, 74, 78, 79, 86])}--.html"  # 分栏页
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"}
        page = requests.get(url=page_url, headers=headers)
        tree = etree.HTML(page.text)
        max_page = int(tree.xpath("//ul[@class='pagination']//a[last()-1]/text()")[0])  # 获取分栏页最大页数

        i = random.randint(1, max_page)  # 随机进入页面
        page_url = page_url if i == 1 else page_url + f"&page={i}"

        page = requests.get(url=page_url, headers=headers)  # 获取此页面元素列表
        tree = etree.HTML(page.text)

        image_url = base_url + random.choice(tree.xpath("//ul//div/a/img/@data-original"))
        with open(self.image, "wb") as f:
            f.write(requests.get(image_url, headers=headers).content)
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
