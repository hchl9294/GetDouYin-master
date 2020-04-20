#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/10/10 0010 10:16 
# @Author : HL 
# @Site :  
# @File : CrawlSecUid.py
# @Software: PyCharm
import re

import requests


class SpiderSecUid():

    def __init__(self):
        self.headers = {
            'accept-encoding': 'gzip',
            'accept-language': 'zh-CN,zh;q=0.9',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': "com.ss.android.ugc.aweme/800 (Linux; U; Android 5.1.1; zh_CN; ALP-AL00; Build/HUAWEIALP-AL00; Cronet/58.0.2991.0)",
        }

    def getShareUrls(self):
        f = open('share-auto-urls.txt', 'r')
        data = f.readlines()
        f.close()
        return data

    def crawl(self):
        data = self.getShareUrls()
        lst = []
        for d in data:
            url = d.replace('\n', '').replace('\\\'','')
            res = requests.get(url, headers=self.headers)
            href = res.url
            if 'sec_uid' in href:
                sec_uid = re.search('sec_uid=(.*?)&', href).group(1)
                lst.append(sec_uid)
                print(sec_uid)
        return lst


if __name__ == '__main__':
    SpiderSecUid().crawl()
