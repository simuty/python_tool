import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
# post的数据
# data = {"info": "biu~~~ send post request"}

# 代理信息,由快代理赞助
proxy = "127.0.0.1:10087"
proxies = {
    "http": "http://%(proxy)s/" % {'proxy': proxy}
    # "https": "http://%(proxy)s/" % {'proxy': proxy}
}
url = "https://api.dex.guru/v1/tradingview/history?symbol=0xe550a593d09fbc8dcd557b5c88cea6946a8b404a_USD&resolution=10&from=1622195175&to=1623078436&currencyCode=USD"
r = requests.get(url, headers=headers, proxies=proxies) #加一个proxies参数
print(r)
print(r.status_code)
print(r.text)