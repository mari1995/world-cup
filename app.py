import json
import logging
import time

import requests as requests
from bs4 import BeautifulSoup
from flask import Flask
from gevent import pywsgi

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/world_cup')
def world_cup():
    """
    获取世界杯赛程
    :return:
    """
    t = int(round(time.time() * 1000))
    url = "https://cbs-i.sports.cctv.com/cache/0fe461738f548ffb6227a83776895fad?ran={}".format(str(t))
    logging.info(url)
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    # logging.info(response.text)
    text = json.loads(response.text)
    # logging.info(type(text))
    # type is list
    results = text["results"]
    logging.info(len(results))
    world_cup_item = None
    for item in results:
        if "世界杯" == item["league"]:
            world_cup_item = item

    return world_cup_item


@app.route('/world_cup_person')
def world_cup_person():
    """
    获取人物介绍
    :return:
    """
    url = "https://worldcup.cctv.com/2022/"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response.encoding = 'utf-8'
    html = response.text
    html_div = BeautifulSoup(html, "html.parser")
    banner_slides = html_div.find('div', id='kataer20104_ind04').find_all('li', class_='banner_slide')
    # logging.info(banner_slides)

    res = []
    for item in banner_slides:
        item_div = BeautifulSoup(str(item), "html.parser")
        img = item_div.find('div', class_='img').get('data-img')
        text = item_div.find('span', class_='txt_shadow').find('a').text
        value = {'img': img, 'title': text}
        res.append(value)
        logging.info("img:{},text:{}".format(img, text))

    return res


@app.route('/world_cup_info')
def world_cup_info():
    """
    获取人物介绍
    :return:
    """
    url = "https://worldcup.cctv.com/2022/"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response.encoding = 'utf-8'
    html = response.text
    html_div = BeautifulSoup(html, "html.parser")
    banner_slides = html_div.find('div', id='kataer20104_ind04').find_all('li', class_='banner_slide')
    # logging.info(banner_slides)

    res = []
    for item in banner_slides:
        item_div = BeautifulSoup(str(item), "html.parser")
        img = item_div.find('div', class_='img').get('data-img')
        text = item_div.find('span', class_='txt_shadow').find('a').text
        value = {'img': img, 'title': text}
        res.append(value)
        logging.info("img:{},text:{}".format(img, text))

    return res

if __name__ == '__main__':
    # pywsgi.WSGIServer(('0.0.0.0', 5000), app).serve_forever()
    app.run(host='0.0.0.0')
