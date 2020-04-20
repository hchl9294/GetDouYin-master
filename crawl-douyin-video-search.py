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
from urllib.parse import quote
from Database import database
from CrawlSecUid import SpiderSecUid


class CrawlDouyinVideo():
    def __init__(self):
        self.db = database()

    def getHeader(self):
        ts = int(time.time())
        ss2 = int(time.time() * 1000)
        _rticket = int(ss2 - 57000)
        headers = {
            'Host': 'api.amemv.com',
            'Connection': 'keep-alive',
            'accept-encoding': 'gzip',
            'accept-language': 'zh-CN,zh;q=0.9',
            'pragma': 'no-cache',
            'sdk-version': '1',
            'X-SS-DP': '1128',
            'cache-control': 'no-cache',
            'Cookie': 'install_id=86658687962; ttreq=1$81a11eb0423f772c6350c193f483aab91717bca1;',
            'odin_tt': 'fd7716c94fde70926ee34081f1fda9ad499571e9e6aa7a60bcea823d5871e60f1e358d6b57076eff17ec9ba6d6f99b19e0b6ad6f44e0494b2f601ecac591836f',
            'upgrade-insecure-requests': '1',
            'user-agent': "com.ss.android.ugc.aweme/800 (Linux; U; Android 5.1.1; zh_CN; ALP-AL00; Build/HUAWEIALP-AL00; Cronet/58.0.2991.0)",
            'X-Khronos': str(ts),
            'X-SS-REQ-TICKET': str(_rticket)
        }
        return headers

    def getUser_Video_Params(self, hotword, max_cursor):
        ts = int(time.time())
        ss2 = int(time.time() * 1000)
        _rticket = int(ss2 - 57000)

        user_video_params = {
            'hotword': hotword,
            'offset': max_cursor,
            'count': 10,
            'source': 'trending_page',
            'is_ad': 0,
            'os_api': 22,
            'device_type': 'M-G955F',
            'ssmix': 'a',
            'manifest_version_code': 800,
            'dpi': 320,
            'js_sdk_version': '1.25.4.1',
            'uuid': '355757010244107',
            'app_name': 'aweme',
            'version_name': '8.0.0',
            'ts': ts,
            'app_type': 'normal',
            'ac': 'wifi',
            'update_version_code': 8002,
            'channel': 'tengxun_new',
            '_rticket': _rticket,
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
            'mcc_mnc': 46007
        }
        return user_video_params

    def crawl(self, sec_user_id):
        print('进入 ' + sec_user_id + ' 线程')
        keywords = quote(sec_user_id)
        time1 = time.time()
        offset = 0
        while True:
            res = requests.get('https://api.amemv.com/aweme/v1/hot/search/video/list/',
                               headers=self.getHeader(), params=self.getUser_Video_Params(keywords, offset))
            contentJson = json.loads(res.content.decode('utf-8'))
            time2 = 0
            aweme_list = contentJson.get('aweme_list')
            if aweme_list != None:
                for aweme in aweme_list:
                    dics = {}
                    if time2 == 0:
                        time2 = time.time()
                        print("用时 " + str(time2 - time1))
                    else:
                        pass
                    authorMessage = aweme['author']
                    author = authorMessage['nickname']
                    sec_uid = authorMessage['sec_uid']
                    aweme_id = aweme['aweme_id']
                    desc = aweme['desc']
                    uri = aweme['video']['download_addr']['uri']
                    playUrl = 'https://aweme.snssdk.com/aweme/v1/play/?video_id=' + uri
                    dics['author'] = author
                    dics['sec_uid'] = sec_uid
                    dics['aweme_id'] = aweme_id
                    dics['desc'] = desc
                    dics['uri'] = uri
                    dics['playUrl'] = playUrl
                    if self.db.is_exists_ShiPin(uri):
                        print(desc + ' 已经抓取！！！！')
                        continue
                    self.db.saveShiPin(dics)
            if contentJson.get('has_more'):
                max_cursor = contentJson.get('max_cursor')
                offset += 10
            else:
                time.sleep(round(random.uniform(1, 3), 1))
                # break


if __name__ == '__main__':
    '''
    http://v.douyin.com/9J5nrc/
       http://v.douyin.com/HuLDBV/
       http://v.douyin.com/HuR8D6/
       http://v.douyin.com/Hujphm/
       http://v.douyin.com/HuPXPf/
       http://v.douyin.com/HuReAL/
       http://v.douyin.com/HgfRXv/
       http://v.douyin.com/HgyJg7/
       http://v.douyin.com/Hg5DoH/
       http://v.douyin.com/Hg5HmB/
    '''
    lst = ['脚脖子到底有多重要', '王丽坤回应结婚', '曝王丽坤领证结婚', '大田后生仔舞', '八一女排3比0美国队']
    # lst = SpiderSecUid().crawl()
    # for secUid in lst:
    #     CrawlDouyinVideo().crawl(secUid)
    thread = 1
    print("主程序开始运行！ 时间： %s" % time.strftime('%H:%M:%S', time.localtime()))
    for secUid in lst:
        t = threading.Thread(target=CrawlDouyinVideo().crawl, args=(secUid,))
        t.start()
    t.join()
    print("主程序运行结束！ 时间： %s" % time.strftime('%H:%M:%S', time.localtime()))
