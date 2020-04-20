#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/10/12 0012 13:36 
# @Author : HL 
# @Site :  
# @File : crawl-douyin-download.py 
# @Software: PyCharm
import os
import time

import requests
from selenium import webdriver

from Database import database


class CrawlDouYinDownload():
    def __init__(self):
        self.db = database()
        # self.driver = webdriver.Chrome()
        self.HEADERS = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            # 'user-agent': "com.ss.android.ugc.aweme/800 (Linux; U; Android 5.1.1; zh_CN; SM-G955F; Build/JLS36C; Cronet/58.0.2991.0)",
            'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25",
        }

    def getVideoUrlByMysql(self):
        return self.db.getVideoIdIsD()

    def crawl(self):
        result = self.getVideoUrlByMysql()
        for rlt in result:
            id = rlt[0]
            playUrl = rlt[2]
            uri = rlt[3]
            desc = rlt[4]

            # path = 'D:\\A_ChanPin\\Video\\douyin\\{}.mp4'.format(uri)
            # if os.path.exists(path):
            #     print(str(id) + ' ' + uri + ' ' + desc + ' 视频已经存在！！！')
            #     continue
            # path = 'D:\\A_ChanPin\\Video\\qita\\{}.mp4'.format(uri)
            # if os.path.exists(path):
            #     print(str(id) + ' ' + uri + ' ' + desc + + ' 视频已经存在！！！')
            #     continue
            flag = self.downloadVideo(playUrl, uri)
            if not flag:
                print(str(id) + ' ' + uri + ' 视频下载完成！！  名称是：' + desc)
            else:
                self.db.updateVideo(id)
                print(str(id) + ' ' + uri + ' 视频下载失败！！！ 名称是：' + desc)

    def downloadVideo(self, url, uri):
        flag = False
        RETRY = 5
        TIMEOUT = 10
        retry_times = 0
        while retry_times < RETRY:
            try:
                # urls = self.getTrueUrl(url)
                resp = requests.get(url, headers=self.HEADERS, stream=True, timeout=TIMEOUT)
                time.sleep(1.5)
                resp = requests.get(resp.url, headers=self.HEADERS, stream=True, timeout=TIMEOUT)
                if resp.status_code == 403:
                    retry_times = RETRY
                    print("Access Denied when retrieve %s.\n" % resp.url)
                    raise Exception("Access Denied")
                with open('D:\\A_ChanPin\\Video\\DouYinBieke\\{}.mp4'.format(uri), 'wb') as fh:
                    for chunk in resp.iter_content(chunk_size=1024):
                        fh.write(chunk)
                break
            except:
                pass
            retry_times += 1
            if retry_times >= 5:
                flag = True
        return flag


if __name__ == '__main__':
    CrawlDouYinDownload().crawl()
