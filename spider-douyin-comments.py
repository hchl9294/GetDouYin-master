#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/9/26 0026 13:58 
# @Author : HL 
# @Site :  
# @File : spider-douyin-comments.py 
# @Software: PyCharm
import json
import random
import time

import requests


class SpiderDouYinComment():
    def __init__(self):
        self.headers = {
            'Host': 'aweme.snssdk.com',
            'accept-encoding': 'gzip',
            'accept-language': 'zh-CN,zh;q=0.9',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': "com.ss.android.ugc.aweme/800 (Linux; U; Android 5.1.1; zh_CN; ALP-AL00; Build/HUAWEIALP-AL00; Cronet/58.0.2991.0)",
        }

        # 代理服务器
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"

        # 代理隧道验证信息
        proxyUser = "H9XK0330X97147TD"
        proxyPass = "3280B770F047D45B"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }

        self.proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }

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

    def reply_comment_params(self, ts, _rticket, aweme_id, cursor):
        reply_comment_params = {
            'comment_id': 6737463306216570888,
            'item_id': 6737461298134617351,
            'cursor': cursor,
            'address_book_access': 1,
            'gps_access': 1,
            'forward_page_type': 1,
            '_rticket': _rticket,
            'count': 10,
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
        return reply_comment_params

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
                aweme_id = aweme['aweme_id']
                desc = aweme['desc']
                uri = aweme['video']['download_addr']['uri']
                playUrl = 'https://aweme.snssdk.com/aweme/v1/play/?video_id=' + uri
                dics['author'] = author
                dics['aweme_id'] = aweme_id
                dics['desc'] = desc
                dics['uri'] = uri
                dics['playUrl'] = playUrl
                j = json.dumps(dics, ensure_ascii=False)
                print(desc)
                self.crawlComment(j, aweme_id)
            if contentJson.get('has_more'):
                max_cursor = contentJson.get('max_cursor')
            else:
                time.sleep(round(random.uniform(1, 3), 1))
                # break

    def crawlComment(self, jsonMessage, aweme_id):
        print(jsonMessage)
        time1 = time.time()
        cursor = 0
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
                reply_num = aweme['reply_comment_total']
                replyer = aweme['user']['nickname']
                dics['replyer'] = replyer
                dics['text'] = text
                dics['cid'] = cid
                dics['digg'] = digg
                dics['cdate'] = cdate
                dics['reply_num'] = reply_num
                cjson = json.dumps(dics, ensure_ascii=False)
                print(cjson)
            if contentJson.get('has_more'):
                max_cursor = contentJson.get('max_cursor')
                cursor += 20
                # break
            else:
                time.sleep(round(random.uniform(1, 3), 1))
                # break

    # 待定
    def reply_comment(self):
        time1 = time.time()
        cursor = 0
        while True:
            ts = int(time.time())
            ss2 = int(time.time() * 1000)
            _rticket = int(ss2 - 57000)
            res = requests.get('https://aweme.snssdk.com/aweme/v1/comment/list/reply/',
                               headers=self.headers,
                               params=self.reply_comment_params(ts, _rticket, 0, cursor))
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
                replyer = aweme['user']['nickname']
                dics['replyer'] = replyer
                dics['text'] = text
                dics[digg] = digg
                dics['cdate'] = cdate
                cjson = json.dumps(dics, ensure_ascii=False)
                print(cjson)
            if contentJson.get('has_more'):
                max_cursor = contentJson.get('max_cursor')
                cursor += 1
                # break
            else:
                time.sleep(round(random.uniform(1, 3), 1))
                break


if __name__ == '__main__':
    SpiderDouYinComment().crawl('MS4wLjABAAAAQEz_scsICUFGfJnBpg5qav7tH3Vx7f1RJklH1aTyNXM')
