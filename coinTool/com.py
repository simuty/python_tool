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

# 超时时间s
REQ_TIMEOUT = 55
# 小数点长度
VALID_LENGTH = 3
# 日志路径
LOG_PATH = "logs/net.log"


def _get_price(url, key):
    # 随机从列表中选择IP、Header
    # proxy = random.choice(proxy_list)
    header = random.choice(my_headers)
    # msg = "URLError: {}-{}\n{}"

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
        return (key, round(lastPrice, VALID_LENGTH))
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

# value1 title
# content
# event 事件名称
def post_ifttt_webhook(value1, value2, event=EVENT_NAME):
    env = "🔱" if len(sys.argv) > 1 else "⚜"
    msg = env + value1 + datetime.now().strftime("%m-%d %H:%M:%S")
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


# def format_coin_history(coin_history):
#     rows = []
#     for item in coin_history:
#         rows.append(format_coin(item))
#     # Use a <br> (break) tag to create a new line
#     # Join the rows delimited by <br> tag: row1<br>row2<br>row3
#     return "\n".join(rows)


# def format_coin(args):
#     msg = "TBTC: {} / {} = {}\nt: {} / {} = {}\nBTCST: {}".format(args['TBTC'], args['BTC'], args['RATIO_BTC'],
#                                                                   args['PIT_COIN_T'], args['PIT_COIN'], args['RATIO_T'],
#                                                                   args['BTCST']
#                                                                   )
#     return msg


# 参数：
# {
#   "BTCST": "0x78650b139471520656b9e7aa7a5e9276814a38e9_USD"
# }
# 返回
# {
#   "BTCST": 25.433
# }
coinType = dict[str, str]
returnType = dict[str, float]
def get_coin_price(args: coinType) -> returnType:
    end = int(time.time())
    start = end - 441660
    req_list = []
    for key, value in args.items():
        item = gevent.spawn(_get_price,
                            BITCOIN_API_URL.format(value, start, end), key)
        req_list.append(item)
    result = gevent.joinall(req_list)
    response_list = [element.value for element in result]
    return dict(response_list)
    

def main():
    print('this is commont file')


if __name__ == '__main__':
    # main()
    logger = Logger(LOG_PATH, level="debug").logger
    get_coin_price({"BTCST": "0x78650b139471520656b9e7aa7a5e9276814a38e9_USD"})
