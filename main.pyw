#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pystray
from PIL import Image, ImageDraw

import modules.bing
import modules.chinamap
import modules.earthmap
import modules.youwu
import modules.netbian
import modules.toopic


def create_icon(width, height):
    image = Image.new("RGB", (width, height), "white")
    dc = ImageDraw.Draw(image)
    dc.rectangle((1, 1, width // 2 - 1, height // 2 - 1), fill="orange")
    dc.rectangle((width // 2 + 1, 1, width - 1, height // 2 - 1), fill="green")
    dc.rectangle((1, height // 2 + 1, width // 2 - 1, height - 1), fill="blue")
    dc.rectangle((width // 2 + 1, height // 2 + 1, width - 1, height - 1), fill="yellow")
    return image


icon = create_icon(64, 64)
submenu = pystray.Menu(
    pystray.MenuItem("地球气象", lambda: modules.earthmap.Wallpaper().crawl().zoom().setup()),
    pystray.MenuItem("中国气象", lambda: modules.chinamap.Wallpaper().crawl().zoom().setup()),
    pystray.MenuItem("必应风景", lambda: modules.bing.Wallpaper().crawl().setup()),
    pystray.MenuItem("尤物网", lambda: modules.youwu.Wallpaper().crawl().setup()),
    pystray.MenuItem("彼岸网", lambda: modules.netbian.Wallpaper().crawl().setup()),
    pystray.MenuItem("壁纸社", lambda: modules.toopic.Wallpaper().crawl().setup()),
)
menu = pystray.Menu(
    pystray.MenuItem("换壁纸", submenu),
    pystray.Menu.SEPARATOR,
    pystray.MenuItem("退出", lambda: tray.stop()),
)
tray = pystray.Icon("Wallpaper", icon=icon, menu=menu)
tray.run()
