#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/9/20 0020 10:07 
# @Author : HL 
# @Site :  
# @File : commentDemo.py 
# @Software: PyCharm

import json
import random
import time

import requests

ts = int(time.time())
ss2 = int(time.time() * 1000)
_rticket = int(ss2 - 57000)

HEADERS = {
    'Host': 'aweme.snssdk.com',
    'Connection': 'keep-alive',
    'Cookie': 'install_id=86658687962; ttreq=1$81a11eb0423f772c6350c193f483aab91717bca1,odin_tt=fd7716c94fde70926ee34081f1fda9ad499571e9e6aa7a60bcea823d5871e60f1e358d6b57076eff17ec9ba6d6f99b19e0b6ad6f44e0494b2f601ecac591836f',
    'accept-encoding': 'gzip',
    'X-SS-REQ-TICKET': str(_rticket),
    'sdk-version': '1',
    # 'X-SS-DP': '1128',
    # 'x-tt-trace-id': '00-176cbf30125891be8c81e01d1033183e-176cbf30125891be-01',
    # 'X-Gorgon': '0300633040017539fb2a561eaadbf5bf67ac9dd33d4eb474ba2a',
    'X-Khronos': str(int((str(int(ss2)))[:-3])),
    # 'accept-language': 'zh-CN,zh;q=0.9',
    # 'pragma': 'no-cache',
    # 'cache-control': 'no-cache',
    # 'upgrade-insecure-requests': '1',
    'User-Agent': "com.ss.android.ugc.aweme/800 (Linux; U; Android 5.1.1; zh_CN; ALP-AL00; Build/HUAWEIALP-AL00; Cronet/58.0.2991.0)"
}

user_video_params = {
    'aweme_id': 6737461298134617351,
    'cursor': 0,
    'address_book_access': 1,
    'gps_access': 1,
    'forward_page_type': 1,
    '_rticket': _rticket,

    'count': 20,
    'os_api': 22,
    'device_type': 'M-G955F',
    'ssmix': 'a',
    'manifest_version_code': 800,
    'dpi': 320,
    'js_sdk_version': '1.25.0.1',
    'app_name': 'aweme',
    'version_name': '8.0.0',
    'ts': ts,
    'app_type': 'normal',
    'ac': 'wifi',
    'update_version_code': 8002,
    'channel': 'tengxun_new',
    'device_platform': 'android',
    'iid': 86658687962,
    'version_code': 800,
    'openudid': 'f46d0495fe505041',
    'device_id': 68798464502,
    'resolution': '1080*1920',
    'os_version': '5.1.1',
    'language': 'zh',
    'device_brand': 'samsung',
    'aid': 1128,
    'mcc_mnc': '46007',
    'uuid': 355757010244107,

    # 'max': 0,
    #     # 'sec_user_id': 'MS4wLjABAAAAQEz_scsICUFGfJnBpg5qav7tH3Vx7f1RJklH1aTyNXM',
    #     # 'retry_type': 'retry_type',
    #     # 'uuid': '355757010244107',_cursor
}
time1 = time.time()
while True:
    res = requests.get('https://api.amemv.com/aweme/v2/comment/list/',
                       headers=HEADERS, params=user_video_params)

    contentJson = json.loads(res.content.decode('utf-8'))
    time2 = 0
    aweme_list = contentJson.get('comments', [])
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
        time.sleep(round(random.uniform(1, 3), 1))
        pass
