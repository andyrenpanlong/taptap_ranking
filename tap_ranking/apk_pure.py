# -*- coding: utf-8 -*-
import xlrd
from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
import wget
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

http_headers = {
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
}

def search_game_url(packagename):
    if packagename == "":
        return
    package_type = 1  # 1-表示url(googleplayid)  2-表是游戏名称
    if re.match(r'^https?:/{2}\w.+$', packagename):
        packagename = packagename.split("=")[1]
        package_type = 1
    else:
        packagename = packagename
        package_type = 2
    url = "https://apkpure.com/cn/search?q=" + packagename + "&region="
    r = requests.get(url)
    if r.status_code == 200:
        bs = BeautifulSoup(r.text, 'html5lib')
        list = bs.select("#search-res .search-dl")
        if len(list) > 0:
            game_name = list[0].select("a")[0].get("href")
            game_icon = list[0].select("a")[0].select("img")[0].get("src")
            down_url = "https://apkpure.com" + game_name
            gameObj = {}
            gameObj["down_url"] = down_url
            if package_type == 1:
                gameObj["game_name"] = list[0].select("a")[0].get("title")
            elif package_type == 2:
                gameObj["game_name"] = packagename
            gameObj["game_icon"] = game_icon
            return get_content_and_downloadurl(gameObj)
        else:
            return []

def get_content_and_downloadurl(gameObj):
    r = requests.get(gameObj["down_url"])
    if r.status_code == 200:
        bs = BeautifulSoup(r.text, 'html5lib')
        gameObj["jump_url"] = "https://apkpure.com" + bs.select(".ny-down .da")[0].get("href")
        if len(bs.select(".version-ul li")) > 2:
            gameObj["game_version"] = bs.select(".version-ul li")[1].select("p")[1].text
            gameObj["game_update"] = bs.select(".version-ul li")[2].select("p")[1].text
        else:
            gameObj["game_version"] = bs.select(".additional li")[1].select("p")[1].text
            gameObj["game_update"] = bs.select(".additional li")[2].select("p")[1].text
        gameObj["game_size"] = bs.select(".ny-down .fsize")[0].select("span")[0].text
        return game_down_load(gameObj)

def game_down_load(gameObj):
    r = requests.get(gameObj["jump_url"])
    if r.status_code == 200:
        bs = BeautifulSoup(r.text, 'html5lib')
        gameObj["game_down_url"] = bs.select("#download_link")[0].get("href")
        data = {}
        data["game_down_true_url"] = yunsite(gameObj["game_down_url"])
        data["game_size"] = gameObj["game_size"]
        data["game_name"] = gameObj["game_name"]
        data["game_icon"] = gameObj["game_icon"]
        data["game_version"] = gameObj["game_version"]
        return data

def yunsite(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    html = requests.get(url, headers=headers, allow_redirects=False)
    return html.headers["Location"]




