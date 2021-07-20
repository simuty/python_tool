# coding=UTF-8
from com import get_coin_price, post_ifttt_webhook
import sys
import time
from datetime import date, datetime
import random
import urllib.request
import socket
import json
from urllib import error
from utils.log import Logger
import gevent
# RecursionError:maximum recursion depth exceeded while calling a python object
# 导入顺序改了，就好了。
from gevent import monkey
monkey.patch_all()


LOG_PATH = "logs/luck.log"
# 间隔
INTERVAL = 50

BITCOIN_PRICE_THRESHOLD = 15000
PRICE_RATIO_DOWN = 0.5
PRICE_RATIO_UP = 0.92

REQ_TIMEOUT = 55
PRICE_BTCST = 22

QBT = "0x17B7163cf1Dbd286E262ddc68b553D899B93f526"



# 免费代理IP不能保证永久有效，如果不能用可以更新
# http://www.goubanjia.com/
proxy_list = [
    # '183.95.80.102:8080',
    # "123.160.31.71:8080",
    # "115.231.128.79:8080",
    # "166.111.77.32:80",
    # '43.240.138.31:8080',
    # "218.201.98.196:3128",
    # "127.0.0.1:10087"
]

# 收集到的常用Header
my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11",
    "Opera/9.25 (Windows NT 5.1; U; en)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12",
    "Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9",
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
]



def format_log(args):
    logger.info(args)


def _get_price(url, key):
    # 随机从列表中选择IP、Header
    # print("url--->", url)
    # proxy = random.choice(proxy_list)
    header = random.choice(my_headers)
    # msg = "URLError: {}-{}\n{}"
    # print("url--->++++==== ", url)
    try:
        # 基于选择的IP构建连接
        urlhandle = urllib.request.ProxyHandler()
        # urlhandle = urllib.request.ProxyHandler({"http": proxy})
        opener = urllib.request.build_opener(urlhandle)
        urllib.request.install_opener(opener)
        # 用urllib2库链接网络图像
        req = urllib.request.Request(url)
        # 增加Header伪装成浏览器
        req.add_header("User-Agent", header)

        # 打开网络图像文件句柄
        # res = urllib.request.urlopen(req, timeout=REQ_TIMEOUT)
        res = urllib.request.urlopen(req)
        data = res.read()
        encoding = res.info().get_content_charset("utf-8")
        result = json.loads(data.decode(encoding))
        # print(result)
        return result
        # lastPrice = result.get("c")[-1]
        # return (key, round(lastPrice, VALID_LENGTH))
    except socket.timeout as err:
        logger.warning("=============================")
        logger.warning("URL: {}".format(url))
        logger.warning("❌ Error description: {}".format(err))
        # post_ifttt_webhook(EVENT_NAME, "❌", "超时--")
        logger.warning("=============================")
        return (key, 0)
    except ConnectionError:
        logger.warning("=============================")
        logger.warning("URL: {}".format(url))
        logger.warning("❌❌ Error description: ConnectionError")
        # post_ifttt_webhook(EVENT_NAME, "❌❌", "异常--")
        logger.warning("=============================")
        return (key, 0)



def start():
    while True:
        url = "https://api.dex.guru/v2/tokens/search/0x17b7163cf1dbd286e262ddc68b553d899b93f526"
        result = _get_price(url, "QBT")
        format_log(result)
        print(result['total'])
        # # 挖矿
        if result['total'] == 1:
            post_ifttt_webhook("©© QBT 🐰 ", "买买买买买买买买")

        time.sleep(2)


def main():
    try:
        msg = " 🚥 丘比特 "
        post_ifttt_webhook(
            msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logger.info(msg)
        start()
    except Exception as error:
        time.sleep(2)
        main()
    finally:
        print('success')


if __name__ == "__main__":
    logger = Logger(LOG_PATH, level="debug").logger
    main()
