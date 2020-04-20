#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/10/10 0010 9:48 
# @Author : HL 
# @Site :  
# @File : crawl-douyin-video.py 
# @Software: PyCharm
import json
import random
import threading
import time

import requests

from Database import database
from CrawlSecUid import SpiderSecUid


class CrawlDouyinVideo():
    def __init__(self):
        self.db = database()
        self.headers = {
            'Host': 'aweme.snssdk.com',
            'accept-encoding': 'gzip',
            'accept-language': 'zh-CN,zh;q=0.9',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': "com.ss.android.ugc.aweme/800 (Linux; U; Android 5.1.1; zh_CN; ALP-AL00; Build/HUAWEIALP-AL00; Cronet/58.0.2991.0)",
        }

    def getUser_Video_Params(self, sec_user_id, max_cursor):
        ts = int(time.time())
        ss2 = int(time.time() * 1000)
        _rticket = int(ss2 - 57000)

        user_video_params = {
            'max_cursor': max_cursor,
            'sec_user_id': sec_user_id,
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
            'js_sdk_version': '1.25.4.1'
        }
        return user_video_params

    def crawl(self, sec_user_id):
        print('进入 ' + sec_user_id + ' 线程')
        time1 = time.time()
        max_cursor = 0
        while True:
            res = requests.get('https://aweme.snssdk.com/aweme/v1/aweme/post/',
                               headers=self.headers, params=self.getUser_Video_Params(sec_user_id, max_cursor))
            contentJson = json.loads(res.content.decode('utf-8'))
            time2 = 0
            aweme_list = contentJson.get('aweme_list', [])
            for aweme in aweme_list:
                dics = {}
                if time2 == 0:
                    time2 = time.time()
                    print("用时 " + str(time2 - time1))
                else:
                    pass
                authorMessage = aweme['author']
                author = authorMessage['nickname']
                desc = aweme['desc']
                try:
                    dcount = aweme['statistics']['digg_count']
                except:
                    print(author+' '+desc+'  没有找到评论数！！！！！')
                    dcount = -1

                aweme_id = aweme['aweme_id']
                # desc = aweme['desc']
                uri = aweme['video']['download_addr']['uri']
                playUrl = 'https://aweme.snssdk.com/aweme/v1/play/?video_id=' + uri
                dics['author'] = author
                dics['sec_uid'] = sec_user_id
                dics['aweme_id'] = aweme_id
                dics['desc'] = desc
                dics['uri'] = uri
                dics['playUrl'] = playUrl
                dics['digg_count'] = dcount
                if self.db.is_exists_ShiPin(uri):
                    print(desc + ' 已经抓取！！！！')
                    continue
                self.db.saveShiPin(dics)
            if contentJson.get('has_more'):
                max_cursor = contentJson.get('max_cursor')
            else:
                time.sleep(round(random.uniform(1, 3), 1))
                # break


if __name__ == '__main__':
    lst = SpiderSecUid().crawl()
    # for secUid in lst:
    #     CrawlDouyinVideo().crawl(secUid)
    thread = 5
    print("主程序开始运行！ 时间： %s" % time.strftime('%H:%M:%S', time.localtime()))
    for secUid in lst:
        t = threading.Thread(target=CrawlDouyinVideo().crawl, args=(secUid,))
        t.start()
    t.join()
    print("主程序运行结束！ 时间： %s" % time.strftime('%H:%M:%S', time.localtime()))
