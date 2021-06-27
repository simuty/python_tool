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


LOG_PATH = "logs/pitman.log"
# 间隔
INTERVAL = 50

BITCOIN_PRICE_THRESHOLD: int = 15000
PRICE_RATIO_DOWN = 0.4
PRICE_RATIO_UP = 0.92

REQ_TIMEOUT = 55
PRICE_BTCST_UP = 70
PRICE_BTCST_DOWN = 14

# dog
DOG = "0xba2ae424d960c26247dd6c32edc70b295c744c43_USD"
# tdog
TDOG = "0xe550a593d09fbc8dcd557b5c88cea6946a8b404a_USD"
TBTC = "0x2cd1075682b0fccaadd0ca629e138e64015ba11c-USD"
BTC = "0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c-USD"
# btcst
BTCST = "0x78650b139471520656b9e7aa7a5e9276814a38e9_USD"


def format_loger(args):
    info = {
        "TIME": int(round(time.time()*1000)),
        "TDOG": args['TDOG'],
        "DOG": args['DOG'],
        "RATIO_DOG": args['RATIO_DOG'],
        "BTCST": args['BTCST'],
    }  
    logger.info(info)

def format_coin(args):
    return "DOG: {} / {} = {}\nBTCST: {}".format(args['TDOG'], args['DOG'], args['RATIO_DOG'], args['BTCST'])


def start():
    # coin_history = []
    while True:
        obj = get_coin_price({
            "DOG": DOG,
            "TDOG": TDOG,
            "BTCST": BTCST
        })
        if 0 in obj.values():
            continue
        obj['RATIO_DOG'] = round(obj['TDOG'] / obj['DOG'], 2)
        format_loger(obj)

        # # btcst
        if obj['BTCST'] < PRICE_BTCST_DOWN or obj['BTCST'] > PRICE_BTCST_UP:
            post_ifttt_webhook("©© BTCST ⚒⚒ ", format_coin(obj))

        # 狗 溢价
        # if obj['RATIO_DOG'] > PRICE_RATIO_UP or obj['RATIO_DOG'] < PRICE_RATIO_DOWN:
        if obj['RATIO_DOG'] > PRICE_RATIO_UP: 
            post_ifttt_webhook("©© 🐶 💎", format_coin(obj))
        # Once we have 5 items in our coin_history send an update
        # if len(coin_history) == 4:
        #     post_ifttt_webhook("©© Last",
        #                        format_coin_history(coin_history))
        #     coin_history = []

        # hour = datetime.now().hour
        minute = datetime.now().minute
        if minute in [30, 31, 32]:
            post_ifttt_webhook("⏰ ⏰Living ...", format_coin(obj))

        # if (hour > 18 or hour < 10) and len(coin_history) > 0:
            # 午夜多提醒⏰

        time.sleep(INTERVAL)


def main():
    try:
        msg = " 🚥  ⚒⚒   "
        post_ifttt_webhook(
            msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logger.info(msg)
        start()
    except Exception as error:
        logger.info("重启中...")
        time.sleep(20)
        main()
    finally:
        print('end')


if __name__ == "__main__":
    logger = Logger(LOG_PATH, level="debug").logger
    main()
