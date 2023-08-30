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
from PIL import Image
from urllib.parse import urljoin


class Wallpaper:
    def __init__(self):
        self.image = os.path.join(tempfile.gettempdir(), "wallpaper.jpg")
        self.style = (0, 0)
        self.session = requests.Session()
        self.session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"}

    def crawl(self):
        base_url = f"https://www.youwu.cc/{random.choice(['xiuren', 'imiss', 'xiaoyu', 'mygirl'])}/"
        base_page = self.session.get(url=base_url)
        base_tree = etree.HTML(base_page.text)
        max_page = int(base_tree.xpath("//div[@class='wrap page clearfix']/a[1]/text()")[0][2:])

        i = random.choice(range(1, max_page + 1))
        page_url = base_url if i == 1 else f"{base_url}index_{i}.html"

        page = self.session.get(url=page_url)
        tree = etree.HTML(page.text)
        img = random.choice(tree.xpath("//div[@class='photo']//a/@href"))

        image_url = urljoin(base_url, img)
        image_page = self.session.get(url=image_url)
        tree = etree.HTML(image_page.text)
        max_page = int(tree.xpath("//div[@class='page']//a[1]/text()")[0][2:])

        j = random.choice(range(1, max_page + 1))
        album_url = image_url if j == 1 else f"{image_url[:-5]}_{j}.html"

        image_page = self.session.get(url=album_url)
        tree = etree.HTML(image_page.text)
        img_url = random.choice(tree.xpath("//div[@class='photo']/a/img/@src"))

        with open(self.image, "wb") as f:
            f.write(self.session.get(img_url).content)

        with Image.open(self.image) as img:
            if img.width > img.height:
                self.style = (6, 0)

        return self

    def setup(self):
        keyex = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(keyex, "WallpaperStyle", 0, win32con.REG_SZ, str(self.style[0]))
        win32api.RegSetValueEx(keyex, "TileWallpaper", 0, win32con.REG_SZ, str(self.style[1]))
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
