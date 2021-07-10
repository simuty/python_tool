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

BITCOIN_PRICE_THRESHOLD: int = 15000
PRICE_RATIO_DOWN = 0.5
PRICE_RATIO_UP = 0.92

REQ_TIMEOUT = 55
PRICE_BTCST = 22

TBTC = "0x2cd1075682b0fccaadd0ca629e138e64015ba11c-USD"
BTC = "0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c-USD"
# bnbtc !!!!【0.2 买入 0.1 继续买入】【0.3以上卖出】
BNBTC = "0xe7cb24f449973d5b3520e5b93d88b405903c75fb_USD"
# 挖矿
BUNNY = "0xc9849e6fdb743d08faee3e34dd2d1bc69ea11a51_USD"

def format_log(args):
    logger.info({
        "TIME": int(round(time.time()*1000)),
        "TBTC": args['TBTC'],
        "BTC": args['BTC'],
        "RATIO_BTC": args['RATIO_BTC'],
        "BUNNY": args['BUNNY'],
        "BNBTC": args['BNBTC'],
    })


def format_coin(args):
    return "TBTC: {} / {} = {}\n 🐰: {} \n BNBTC: {}".format(args['TBTC'], args['BTC'], args['RATIO_BTC'], args['BUNNY'], args['BNBTC'])


def start():
    while True:
        obj = get_coin_price({
            "TBTC": TBTC,
            "BTC": BTC,
            "BUNNY": BUNNY,
            "BNBTC": BNBTC,
        })
        if 0 in obj.values():
            continue

        obj['RATIO_BTC'] = round(obj['TBTC'] / obj['BTC'], 2)
        format_log(obj)

        # BTC
        if obj['TBTC'] < BITCOIN_PRICE_THRESHOLD or obj['RATIO_BTC'] < PRICE_RATIO_DOWN or obj['RATIO_BTC'] > PRICE_RATIO_UP:
            post_ifttt_webhook("©© TBTC ⚠️⚠️", format_coin(obj))

        # 挖矿
        if obj['BUNNY'] < 12:
            post_ifttt_webhook("©© BUNNY 🐰 ", format_coin(obj))

        # 做波段，争取搞到1w个
        if obj['BNBTC'] < 0.17 or obj['BNBTC'] > 0.4:
            post_ifttt_webhook("©© 🌊 BNBTC ", format_coin(obj))

        minute = datetime.now().minute
        if minute in [30, 31, 32]:
            post_ifttt_webhook(" ⏰Living ...", format_coin(obj))

        time.sleep(INTERVAL)


def main():
    try:
        msg = " 🚥 Luck..."
        post_ifttt_webhook(
            msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logger.info(msg)
        start()
    except Exception as error:
        time.sleep(20)
        main()
    finally:
        print('success')


if __name__ == "__main__":
    logger = Logger(LOG_PATH, level="debug").logger
    main()
