#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/10/10 0010 10:03 
# @Author : HL 
# @Site :  
# @File : crawl-douyin-comment.py 
# @Software: PyCharm
import json
import random
import time

import requests

from Database import database


class CrawlDouyinComment():
    def __init__(self):
        self.db = database()

    def getAweme_id(self):
        return self.db.getVideoId()

    def commentHeaders(self, _rticket, ss2):
        commentHeaders = {
            # 'Host': 'api.amemv.com',
            'Host': 'aweme.snssdk.com',
            'Connection': 'keep-alive',
            'accept-encoding': 'gzip',
            'X-SS-REQ-TICKET': str(_rticket),
            'sdk-version': '1',
            'X-SS-DP': '1128',
            'X-Khronos': str(int((str(int(ss2)))[:-3])),
            'User-Agent': "com.ss.android.ugc.aweme/800 (Linux; U; Android 5.1.1; zh_CN; SM-G955F; Build/JLS36C; Cronet/58.0.2991.0)"
        }
        return commentHeaders

    def user_video_params(self, ts, _rticket, aweme_id, cursor):
        user_video_params = {
            'aweme_id': aweme_id,
            'cursor': cursor,
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
        }
        return user_video_params

    def crawl(self):
        result = self.getAweme_id()
        for c in range(0, 220, 20):
            for rlt in result:
                videoId = rlt[0]
                aweme_id = rlt[1]
                time1 = time.time()
                cursor = c
                while True:
                    ts = int(time.time())
                    ss2 = int(time.time() * 1000)
                    _rticket = int(ss2 - 57000)
                    res = requests.get('https://aweme.snssdk.com/aweme/v2/comment/list/',
                                       headers=self.commentHeaders(_rticket, ss2),
                                       params=self.user_video_params(ts, _rticket, aweme_id, cursor))
                    contentJson = json.loads(res.content.decode('utf-8'))
                    time2 = 0
                    aweme_list = contentJson.get('comments', [])
                    for aweme in aweme_list:
                        dics = {}
                        if time2 == 0:
                            time2 = time.time()
                            print("用时 " + str(time2 - time1))
                        else:
                            pass
                        timeStamp = aweme['create_time']
                        timeArray = time.localtime(timeStamp)
                        cdate = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                        digg = aweme['digg_count']
                        text = aweme['text']
                        cid = aweme['cid']
                        try:
                            reply_num = aweme['reply_comment_total']
                        except Exception as e:
                            print(e)
                        replyer = aweme['user']['nickname']
                        dics['replyer'] = replyer
                        dics['text'] = text
                        dics['cid'] = cid
                        dics['digg'] = digg
                        dics['cdate'] = cdate
                        dics['reply_num'] = reply_num
                        dics['video_id'] = videoId
                        if self.db.is_exists_Comment(cid):
                            print(str(videoId) + ' ' + text + ' 已经抓取！！！！')
                            continue
                        self.db.saveComment(dics)
                    if contentJson.get('has_more'):
                        max_cursor = contentJson.get('max_cursor')
                        cursor += 20
                        time.sleep(round(random.uniform(1, 3), 1))
                        # break
                    else:
                        time.sleep(round(random.uniform(1, 3), 1))
                        break


if __name__ == '__main__':
    CrawlDouyinComment().crawl()
