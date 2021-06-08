# coding=UTF-8
import gevent
import time
from urllib.request import urlopen
from gevent import monkey;

monkey.patch_all()

urls=[
    'https://www.baidu.com/',
    'https://github.com/'
]

def f(url, key="1"):
    print('GET: ', url)
    resp = urlopen(url)          #1.打开一个url
    data = resp.read()           #2.请求结果 此data就是下载的网页
    print('%d bytes received from %s.' % (len(data), url))
    return {key: url}


#同步代码
time_start=time.time()
for url in urls:
    f(url)
print("===同步cost--->",time.time()-time_start)

#异步代码
async_time_start=time.time()
result = gevent.joinall([
    gevent.spawn(f, 'https://www.baidu.com/', 'key1'),
    gevent.spawn(f, 'https://github.com/', 'key3'),
])

response_list = [element.value for element in result]  #从result中获取每个请求的Response
print(response_list)
print("===异步cost--->",time.time()-async_time_start)