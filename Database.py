#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/10/10 0010 9:06 
# @Author : HL 
# @Site :  
# @File : Database.py 
# @Software: PyCharm
import time

import pymysql


class database():
    host = '192.168.0.210'
    user = 'search_user'
    password = 'search_user'
    database = 'gmcms2_dev_statistic'
    port = 3306
    charset = 'utf8'
    cursor = ''
    connet = ''

    def __init__(self):
        # 连接数据库
        self.connet = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                      port=self.port, charset=self.charset)
        self.cursor = self.connet.cursor()

    # 保存数据
    def saveShiPin(self, dict):
        try:
            self.cursor.execute(
                "insert into t_douyin_video(description,author,sec_uid,aweme_id,playUrl,uri,digg_count,crawl_time) values (%s,%s,%s,%s,%s,%s,%s,%s)",
                (str(dict.get('desc')), str(dict.get('sec_uid')), str(dict.get('author')), str(dict.get('aweme_id')),
                 str(dict.get('playUrl')), str(dict.get('uri')), str(dict.get('digg_count')),
                 str(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())))))
            self.connet.commit()
            print(u'保存完一条数据！标题是：' + str(dict.get('desc')))
        except Exception:
            # 连接数据库
            self.connet = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                          database=self.database,
                                          port=self.port, charset=self.charset)
            self.cursor = self.connet.cursor()
            self.cursor.execute(
                "insert into t_douyin_video(description,author,sec_uid,aweme_id,playUrl,uri,digg_count,crawl_time) values (%s,%s,%s,%s,%s,%s,%s,%s)",
                (str(dict.get('desc')), str(dict.get('sec_uid')), str(dict.get('author')), str(dict.get('aweme_id')),
                 str(dict.get('playUrl')), str(dict.get('uri')), str(dict.get('digg_count')),
                 str(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())))))
            self.connet.commit()
            print(u'保存完一条数据！标题是：' + str(dict.get('desc')))

    # 判断元素是否已经在数据库里，在就返回true，不在就返回false
    def is_exists_ShiPin(self, uri):
        try:
            self.cursor.execute("select * from t_douyin_video where uri = %s", str(uri))
            if self.cursor.fetchone() is None:
                return False
            return True
        except Exception:
            self.connet = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                          database=self.database,
                                          port=self.port, charset=self.charset)
            self.cursor = self.connet.cursor()
            self.cursor.execute("select * from t_douyin_video where uri = %s", str(uri))
            if self.cursor.fetchone() is None:
                return False
            return True

    def getVideoId(self):
        self.cursor.execute("select id,aweme_id,playUrl,uri from t_douyin_video where id > 18")
        result = self.cursor.fetchall()
        return result

    def getVideoIdIsD(self):
        self.cursor.execute(
            "select id,aweme_id,playUrl,uri,description from t_douyin_video where (isErrDownload is null or isErrDownload = 1) and id >= 2698 and digg_count > 9999")
        result = self.cursor.fetchall()
        return result

    def updateVideo(self, id):
        try:
            self.cursor.execute("update t_douyin_video set isErrDownload = 1 where id = %s" % str(id))
            self.connet.commit()
        except:
            # 连接数据库
            self.connet = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                          database=self.database,
                                          port=self.port, charset=self.charset)
            self.cursor = self.connet.cursor()
            self.cursor.execute("update t_douyin_video set isErrDownload = 1 where id = %s" % str(id))
            self.connet.commit()

    # 保存数据
    def saveComment(self, dict):
        try:
            self.cursor.execute(
                "insert into t_douyin_comment(video_id,replyer,reply_num,digg,cdate,cid,text,crawl_time) values (%s,%s,%s,%s,%s,%s,%s,%s)",
                (str(dict.get('video_id')), str(dict.get('replyer')), str(dict.get('reply_num')), str(dict.get('digg')),
                 str(dict.get('cdate')), str(dict.get('cid')), str(dict.get('text')),
                 str(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())))))
            self.connet.commit()
            print(u'保存完一条数据！标题是：' + str(dict.get('text')))
        except Exception:
            # 连接数据库
            self.connet = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                          database=self.database,
                                          port=self.port, charset=self.charset)
            self.cursor = self.connet.cursor()
            self.cursor.execute(
                "insert into t_douyin_comment(video_id,replyer,reply_num,digg,cdate,cid,text,crawl_time) values (%s,%s,%s,%s,%s,%s,%s,%s)",
                (str(dict.get('video_id')), str(dict.get('replyer')), str(dict.get('reply_num')), str(dict.get('digg')),
                 str(dict.get('cdate')), str(dict.get('cid')), str(dict.get('text')),
                 str(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())))))
            self.connet.commit()
            print(u'保存完一条数据！标题是：' + str(dict.get('text')))

    # 判断元素是否已经在数据库里，在就返回true，不在就返回false
    def is_exists_Comment(self, cid):
        try:
            self.cursor.execute("select * from t_douyin_comment where cid = %s", str(cid))
            if self.cursor.fetchone() is None:
                return False
            return True
        except Exception:
            self.connet = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                          database=self.database,
                                          port=self.port, charset=self.charset)
            self.cursor = self.connet.cursor()
            self.cursor.execute("select * from t_douyin_comment where cid = %s", str(cid))
            if self.cursor.fetchone() is None:
                return False
            return True
