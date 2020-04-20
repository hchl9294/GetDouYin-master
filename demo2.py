#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 2019/9/19 0019 11:24 
# @Author : HL 
# @Site :  
# @File : demo.py 
# @Software: PyCharm
import json
import random
import time
import requests

HEADERS = {
    'Host': 'aweme.snssdk.com',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip',
    'sdk-version': '1',
    'accept-language': 'zh-CN,zh;q=0.9',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'User-Agent': "com.ss.android.ugc.aweme/800 (Linux; U; Android 5.1.1; zh_CN; ALP-AL00; Build/HUAWEIALP-AL00; Cronet/58.0.2991.0)",
}

ts = int(time.time())
ss2 = int(time.time() * 1000)
_rticket = int(ss2 - 57000)

user_video_params = {
    'max_cursor': 0,
    'sec_user_id': 'MS4wLjABAAAAQEz_scsICUFGfJnBpg5qav7tH3Vx7f1RJklH1aTyNXM',
    'count': 20,
    'retry_type': 'retry_type',
    'iid': 86658687962,
    'device_id': 68798464502,
    'ac': 'wifi',
    'channel': 'tengxun_new',
    'aid': 1128,
    'app_name': 'aweme',
    'version_code': 800,
    'version_name': '8.0.0',
    'device_platform': 'android',
    'ssmix': 'a',
    'device_type': 'M-G955F',
    'device_brand': 'samsung',
    'language': 'zh',
    'os_api': 22,
    'os_version': '5.1.1',
    'uuid': '355757010244107',
    'openudid': 'f46d0495fe505041',
    'manifest_version_code': 800,
    'resolution': '1080*1920',
    'dpi': 320,
    'update_version_code': 8002,
    '_rticket': _rticket,
    'mcc_mnc': '46007',
    'ts': ts,
    'app_type': 'normal',
    'js_sdk_version': '1.25.0.1'
}
time1 = time.time()
while True:
    res = requests.get('https://aweme.snssdk.com/aweme/v1/aweme/post/',
                       headers=HEADERS, params=user_video_params)

    contentJson = json.loads(res.content.decode('utf-8'))
    time2 = 0
    aweme_list = contentJson.get('aweme_list', [])
    for aweme in aweme_list:
        if time2 == 0:
            time2 = time.time()
            print("用时 " + str(time2 - time1))
        else:
            pass
        print("number: 有值")
    if contentJson.get('has_more'):
        max_cursor = contentJson.get('max_cursor')
        break
    else:
        # time.sleep(round(random.uniform(1, 3), 1))
        pass
