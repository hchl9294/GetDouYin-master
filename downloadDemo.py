#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/9/19 0019 16:06 
# @Author : HL 
# @Site :  
# @File : downloadDemo.py 
# @Software: PyCharm
import requests

HEADERS = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': "com.ss.android.ugc.aweme/800 (Linux; U; Android 5.1.1; zh_CN; SM-G955F; Build/JLS36C; Cronet/58.0.2991.0)",
}
RETRY = 5
TIMEOUT = 10
retry_times = 0
while retry_times < RETRY:
    try:
        resp = requests.get('https://api.amemv.com/aweme/v1/play/?video_id=v0300fc60000bm1ek8d4j4o8jisccaig',
                            headers=HEADERS, stream=True, timeout=TIMEOUT)
        if resp.status_code == 403:
            retry_times = RETRY
            print("Access Denied when retrieve %s.\n" % resp.url)
            raise Exception("Access Denied")
        with open('D:\\video\\3.mp4', 'wb') as fh:
            for chunk in resp.iter_content(chunk_size=1024):
                fh.write(chunk)
        break
    except:
        pass
    retry_times += 1
