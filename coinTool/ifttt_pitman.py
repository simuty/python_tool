import requests
import time
from datetime import date, datetime
import random
import urllib.request
import json
from urllib import error
from utils.log import Logger


# 免费代理IP不能保证永久有效，如果不能用可以更新
# http://www.goubanjia.com/
proxy_list = [
    # '183.95.80.102:8080', 20
    "123.160.31.71:8080",
    "115.231.128.79:8080",
    "166.111.77.32:80",
    # '43.240.138.31:8080', 25
    "218.201.98.196:3128",
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
INTERVAL = 5

BITCOIN_PRICE_THRESHOLD: int = 15000  # Set this to whatever you like
BITCOIN_PRICE_RATIO = 0.5  # Set this to whatever you like
# dog
coin_dog = "0xba2ae424d960c26247dd6c32edc70b295c744c43_USD"
# tdog
coin_tdog = "0xe550a593d09fbc8dcd557b5c88cea6946a8b404a_USD"
coin_tbtc = "0x2cd1075682b0fccaadd0ca629e138e64015ba11c-USD"
coin_btc = "0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c-USD"


def get_latest_coin_price(url) -> int:

    # 随机从列表中选择IP、Header
    proxy = random.choice(proxy_list)
    header = random.choice(my_headers)
    msg = "URLError: {}-{}\n{}"

    try:
        # print(datetime.now().strftime('%Y.%m.%d %H:%M:%S'), "---->111")
        # print(proxy, header)

        # 基于选择的IP构建连接
        urlhandle = urllib.request.ProxyHandler({"http": proxy})
        opener = urllib.request.build_opener(urlhandle)
        urllib.request.install_opener(opener)

        # 用urllib2库链接网络图像
        req = urllib.request.Request(url)
        # 增加Header伪装成浏览器
        req.add_header("User-Agent", header)

        # 打开网络图像文件句柄
        res = urllib.request.urlopen(req)
        data = res.read()

        encoding = res.info().get_content_charset("utf-8")
        result = json.loads(data.decode(encoding))
        lastPrice = result.get("c")[-1]
        return round(lastPrice, 2)
    except error.URLError as e:
        if hasattr(e, "code"):
            msg = msg.format(proxy, header, e)
        elif hasattr(e, "reason"):
            msg = msg.format(proxy, header, e.reason)

        post_ifttt_webhook(EVENT_NAME, "❌", msg)
        return 0


def post_ifttt_webhook(event, value1, value2):
    # The payload that will be sent to IFTTT service
    data = {"value1": value1, "value2": value2}
    # inserts our desired event
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    # Sends a HTTP POST request to the webhook URL
    res = requests.post(ifttt_event_url, json=data)
    # print(res, ifttt_event_url)


def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string: '24.02.2018 15:09'
        date = bitcoin_price["date"].strftime("%d.%m.%Y %H:%M")
        price = bitcoin_price["price"]
        tPrice = bitcoin_price["tPrice"]
        ratio = bitcoin_price["ratio"]
        # <b> (bold) tag creates bolded text
        # 24.02.2018 15:09: $<b>10123.4</b>
        row = "{}: $<b>{}</b>{}-{}".format(date, price, tPrice, ratio)
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    # Join the rows delimited by <br> tag: row1<br>row2<br>row3
    return "<br>".join(rows)



def main():
    bitcoin_history = []
    num = 441660

    while True:

        end = int(time.time())
        start = end - num

        url_base = BITCOIN_API_URL.format(coin_dog, start, end)
        url_t = BITCOIN_API_URL.format(coin_tdog, start, end)

        url_btc = BITCOIN_API_URL.format(coin_btc, start, end)
        url_tbtc = BITCOIN_API_URL.format(coin_tbtc, start, end)

        date = datetime.now().strftime("%Y.%m.%d %H:%M:%S")

        price_base = get_latest_coin_price(url_base)
        price_t = get_latest_coin_price(url_t)
        price_btc = get_latest_coin_price(url_btc)
        price_tbtc = get_latest_coin_price(url_tbtc)

        if price_base == 0 or price_t == 0 or price_btc == 0 or price_tbtc == 0:
            continue

        ratio_t = round(price_t / price_base, 2)
        ratio_btc = round(price_tbtc / price_btc, 2)

        obj = {"date": date, "price": price_base, "tPrice": price_t, "ratio": ratio_t}
        logger.info(obj)

        msg = "{} btc:{}-{}-{} t: {}-{}-{}".format(
            date, price_btc, price_tbtc, ratio_btc, price_base, price_t, ratio_t
        )

        bitcoin_history.append(
            {"date": date, "price": price_base, "tPrice": price_t, "ratio": ratio_t}
        )

        # Send an emergency notification
        if price_btc < BITCOIN_PRICE_THRESHOLD or ratio_btc < BITCOIN_PRICE_RATIO:
            post_ifttt_webhook(EVENT_NAME, "✅✅✅", msg)
        # Send a Telegram notification
        # Once we have 5 items in our bitcoin_history send an update
        # if len(bitcoin_history) == 5:
        #     post_ifttt_webhook('bitcoin_price_update',
        #                        format_bitcoin_history(bitcoin_history))
        # Reset the history
        # bitcoin_history = []

        # Sleep for 5 minutes
        # (For testing purposes you can set it to a lower number)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    logger = Logger("all.log", level="debug").logger
    main()
