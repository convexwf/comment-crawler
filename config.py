# -*-coding:utf-8 -*-
import os
import random
import requests
import time
import chardet
import lxml

from bs4 import BeautifulSoup
from lxml import etree

class global_var:
    UserAgent_file = "variables/UserAgent.txt"
    user_agent_list = []

class Connection():
    @staticmethod
    def update_download(url):
        pass

    @staticmethod
    ### 建立连接，爬取网页
    def download(url):
        decay_time = 0.25
        while True:
            try:
                time.sleep(random.randint(0, 1))
                response = requests.get(url, timeout=5)
                encode_type = chardet.detect(response.content)['encoding']
                if encode_type == 'ISO-8859-2': encode_type = 'utf-8'
                response.encoding = encode_type
                if (not response.ok) or len(response.content) < 500:
                    raise ConnectionError
                else:
                    return response.text
            except Exception as e:
                print('decay_time', decay_time)
                print(e)
                print(url)
                time.sleep(decay_time)
                if decay_time >= 16:
                    return None
                if decay_time < 32:
                    decay_time *= 2

    @staticmethod
    def to_BS4(url):
        return BeautifulSoup(Connection.download(url), 'lxml')

    @staticmethod
    def bs4_parser(url, parser):
        item_list = []
        response = Connection.download(url)
        if response == None:
            return item_list
        soup = BeautifulSoup(response, 'lxml')
        items = soup.select(parser['pattern'])
        positions = eval(parser['position'])
        for item in items:
            unit = {}
            for key, value in positions.items():
                temp = item.select(value)
                if temp != None:
                    unit[key] = temp[0].text.strip()
            item_list.append(unit)
        return item_list


    @staticmethod
    def xpath_parser(url, parser):
        item_list = []
        response = Connection.download(url)
        if response == None:
            return item_list
        root = etree.HTML(response)
        items = root.xpath(parser['pattern'])
        positions = eval(parser['position'])
        for item in items:
            unit = {}
            for key, value in positions.items():
                if isinstance(item.xpath(value)[0], lxml.etree._ElementUnicodeResult):
                    unit[key] = item.xpath(value)[0].strip()
                else:
                    unit[key] = item.xpath(value)[0].text.strip()
            item_list.append(unit)
        return item_list

    @staticmethod
    def regex_parser(url, parser):
        item_list = []
        response = Connection.download(url)
        pattern = re.compile(parser['pattern'])
        matchs = pattern.findall(response)
        positions = eval(parser['position'])
        for match in matchs:
            unit = {}
            for key, value in positions.items():
                unit[key] = match[value]
            item_list.append(unit)
        return item_list

### 初始化全局变量
def init_var():
    global_var.user_agent_list = open(global_var.UserAgent_file).read().splitlines()

### 返回一个随机的请求头 headers
def get_random_headers():
    UserAgent = random.choice(global_var.user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers

if __name__ == '__main__':
    init_var()
    print(global_var.user_agent_list)
