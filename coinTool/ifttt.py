# coding=UTF-8
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
# import requests


# 免费代理IP不能保证永久有效，如果不能用可以更新
# http://www.goubanjia.com/
proxy_list = [
    # '183.95.80.102:8080',
    # "123.160.31.71:8080",
    # "115.231.128.79:8080",
    # "166.111.77.32:80",
    # '43.240.138.31:8080',
    # "218.201.98.196:3128",
    "127.0.0.1:10087"
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


BITCOIN_API_URL = "https://api.dex.guru/v1/tradingview/history?symbol={}&resolution=1&from={}&to={}&currencyCode=USD"
IFTTT_WEBHOOKS_URL = "https://maker.ifttt.com/trigger/{}/with/key/oJPBHriGv3c5Gh9iCZvop"
EVENT_NAME = "buy_coin"
# 间隔
INTERVAL = 50

BITCOIN_PRICE_THRESHOLD: int = 15000
PRICE_RATIO_DOWN = 0.6
PRICE_RATIO_UP = 0.92

REQ_TIMEOUT = 50
PRICE_BTCST = 24
# BNBTC 波段
PRICE_BNBTC_DOWN = 0.20
PRICE_BNBTC_UP = 0.22

# dog
PIT_COIN = "0xba2ae424d960c26247dd6c32edc70b295c744c43_USD"
# tdog
PIT_COIN_T = "0xe550a593d09fbc8dcd557b5c88cea6946a8b404a_USD"
TBTC = "0x2cd1075682b0fccaadd0ca629e138e64015ba11c-USD"
BTC = "0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c-USD"
# btcst
BTCST = "0x78650b139471520656b9e7aa7a5e9276814a38e9_USD"
# bnbtc
BNBTC = "0xe7cb24f449973d5b3520e5b93d88b405903c75fb_USD"



def get_latest_coin_price(url, key):

    # 随机从列表中选择IP、Header
    proxy = random.choice(proxy_list)
    header = random.choice(my_headers)
    msg = "URLError: {}-{}\n{}"

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
        res = urllib.request.urlopen(req, timeout=REQ_TIMEOUT)
        data = res.read()
        encoding = res.info().get_content_charset("utf-8")
        result = json.loads(data.decode(encoding))
        lastPrice = result.get("c")[-1]
        return (key, round(lastPrice, 3))
    # except error.URLError as err:
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

# event 事件名称
# value1 title
# content
def post_ifttt_webhook(event, value1, value2):
    env =  "M-" if len(sys.argv) > 1 else "H-"
    msg = env + value1 + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {"value1": msg, "value2": value2}
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    # Sends a HTTP POST request to the webhook URL
    # res = requests.post(ifttt_event_url, json=data)
    # values = urllib.parse.urlencode(data).encode(encoding='UTF8')
    headers = {'Content-Type': 'application/json'}
    # print(data)
    # print(values)
    # print(json.dumps(data))
    # print(json.dumps(data).encode())
    request = urllib.request.Request(
        url=ifttt_event_url, headers=headers, data=json.dumps(data).encode())
    urllib.request.urlopen(request)


def format_coin_history(coin_history):
    rows = []
    for item in coin_history:
        rows.append(format_coin(item))
    # Use a <br> (break) tag to create a new line
    # Join the rows delimited by <br> tag: row1<br>row2<br>row3
    return "\n".join(rows)


def format_coin(args):
    msg = "TBTC: {} / {} = {}\nt: {} / {} = {}\nBTCST: {} \nBNBTC: {}".format(args['TBTC'], args['BTC'], args['RATIO_BTC'],
                                                                        args['PIT_COIN_T'], args['PIT_COIN'], args['RATIO_T'],
                                                                        args['BTCST'], args['BNBTC'],
                                                                        )
    return msg


def format_loger(args):
    info = {
        "TBTC": args['TBTC'],
        "BTC": args['BTC'],
        "RATIO_BTC": args['RATIO_BTC'],
        "PIT_COIN_T": args['PIT_COIN_T'],
        "PIT_COIN": args['PIT_COIN'],
        "RATIO_T": args['RATIO_T'],
        "BTCST": args['BTCST'],
        "BNBTC": args['BNBTC']
    }
    logger.info(info)


def ifttt():
    coin_history = []
    num = 441660

    while True:
        end = int(time.time())
        start = end - num

        result = gevent.joinall([
            gevent.spawn(get_latest_coin_price, BITCOIN_API_URL.format(PIT_COIN, start, end), 'PIT_COIN'),
            gevent.spawn(get_latest_coin_price, BITCOIN_API_URL.format(PIT_COIN_T, start, end), 'PIT_COIN_T'),
            gevent.spawn(get_latest_coin_price, BITCOIN_API_URL.format(BTC, start, end), 'BTC'),
            gevent.spawn(get_latest_coin_price, BITCOIN_API_URL.format(TBTC, start, end), 'TBTC'),
            gevent.spawn(get_latest_coin_price, BITCOIN_API_URL.format(BTCST, start, end), 'BTCST'),
            gevent.spawn(get_latest_coin_price, BITCOIN_API_URL.format(BNBTC, start, end), 'BNBTC'),
        ])
        # 从result中获取每个请求的Response
        response_list = [element.value for element in result]

        obj = dict(response_list)
        if 0 in obj.values():
            continue

        obj['RATIO_BTC'] = round(obj['TBTC'] / obj['BTC'], 2)
        obj['RATIO_T'] = round(obj['PIT_COIN_T'] / obj['PIT_COIN'], 2)
        format_loger(obj)
        
        # # btcst
        if obj['BTCST'] < PRICE_BTCST:
            post_ifttt_webhook(EVENT_NAME, "©© BTCST ⛏️⛏️ ", format_coin(obj))

        # BTC
        if obj['TBTC'] < BITCOIN_PRICE_THRESHOLD or obj['RATIO_BTC'] < PRICE_RATIO_DOWN or obj['RATIO_BTC'] > PRICE_RATIO_UP:
            post_ifttt_webhook(EVENT_NAME, "©© TBTC ⚠️⚠️", format_coin(obj))
            # coin_history.append(obj)
        
        # τ 挖矿浮出水面
        if obj['RATIO_T'] > PRICE_RATIO_UP or obj['RATIO_T'] < PRICE_RATIO_DOWN:
            post_ifttt_webhook(EVENT_NAME, "©© τ 💎💎", format_coin(obj))

        # 波段
        if obj['BNBTC'] < PRICE_BNBTC_DOWN or obj['BNBTC'] > PRICE_BNBTC_UP:
            post_ifttt_webhook(EVENT_NAME, "©© BNBTC 🌊🌊", format_coin(obj))


        # Once we have 5 items in our coin_history send an update
        if len(coin_history) == 4:
            post_ifttt_webhook(EVENT_NAME, "©© Last",
                               format_coin_history(coin_history))
            coin_history = []

        # hour = datetime.now().hour
        minute = datetime.now().minute
        if minute in [50, 51, 52]:
            post_ifttt_webhook(EVENT_NAME, "⏰ ⏰Living ...", format_coin(obj))

        # if (hour > 18 or hour < 10) and len(coin_history) > 0:
            # 午夜多提醒⏰

        # Sleep for 5 minutes
        # (For testing purposes you can set it to a lower number)
        # interval = random.randint(10,40)
        time.sleep(INTERVAL)


def main():
    try:
        msg = " 🚥 🚥 启动中。。。"
        post_ifttt_webhook(
            EVENT_NAME, msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logger.info(msg)
        ifttt()
    except Exception as error:
        logger.warning("重启中... {}".format(error))
        main()
    finally:
        print('success')


if __name__ == "__main__":
    logger = Logger("ifttt-mw.log", level="debug").logger
    main()
