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
        base_url = "https://pic.netbian.com"  # 基础页
        sub_url = random.choice(
            [
                # "4kdongman",
                "4kfengjing",
                # "4kmeinv",
                # "4kyouxi",
                # "4kyingshi",
                # "4kqiche",
                # "4kdongwu",
                # "4krenwu",
                # "4kzongjiao",
                # "4kbeijing",
            ]
        )
        page_url = f"{base_url}/{sub_url}"  # 分栏页
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"}
        page = requests.get(url=page_url, headers=headers)
        tree = etree.HTML(page.text)
        max_page = int(tree.xpath('//div[@class="page"]/a[last() - 1]/text()')[0])

        i = random.randint(1, max_page)  # 随机进入页面
        page_url = page_url if i == 1 else page_url + f"/index_{i}.html"

        page = requests.get(url=page_url, headers=headers)  # 获取此页面元素列表
        tree = etree.HTML(page.text)

        new_url = base_url + random.choice(tree.xpath('//*[@id="main"]/div[4]/ul//a/@href'))
        new_page = requests.get(url=new_url, headers=headers)
        new_tree = etree.HTML(new_page.text)
        new_img = new_tree.xpath('//*[@id="img"]/img/@src')[0]  # 获取此图像地址

        image_url = base_url + new_img
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
