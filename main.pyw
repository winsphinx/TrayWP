#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
from time import sleep

from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem

import modules.bing
import modules.chinamap
import modules.earthmap
import modules.netbian
import modules.toopic
import modules.youwu


def create_icon(width, height):
    image = Image.new("RGB", (width, height), "white")
    dc = ImageDraw.Draw(image)
    dc.rectangle((1, 1, width // 2 - 1, height // 2 - 1), fill="orange")
    dc.rectangle((width // 2 + 1, 1, width - 1, height // 2 - 1), fill="green")
    dc.rectangle((1, height // 2 + 1, width // 2 - 1, height - 1), fill="blue")
    dc.rectangle((width // 2 + 1, height // 2 + 1, width - 1, height - 1), fill="yellow")
    return image


def on_exit():
    global exited_flag
    exited_flag = True
    tray.stop()


exited_flag = False
icon = create_icon(64, 64)

submenu = Menu(
    MenuItem("地球气象", lambda: modules.earthmap.Wallpaper().crawl().zoom().setup()),
    MenuItem("中国气象", lambda: modules.chinamap.Wallpaper().crawl().zoom().setup()),
    MenuItem("必应风景", lambda: modules.bing.Wallpaper().crawl().setup()),
    MenuItem("尤物网", lambda: modules.youwu.Wallpaper().crawl().setup()),
    MenuItem("彼岸网", lambda: modules.netbian.Wallpaper().crawl().setup()),
    MenuItem("壁纸社", lambda: modules.toopic.Wallpaper().crawl().setup()),
)
menu = Menu(
    MenuItem("换壁纸", submenu),
    Menu.SEPARATOR,
    MenuItem("退出", on_exit),
)

tray = Icon("Wallpaper", icon=icon, menu=menu)
Thread(target=tray.run).start()

while True:
    if exited_flag:
        break
    sleep(1)
