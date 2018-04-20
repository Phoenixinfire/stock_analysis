#!/usr/bin python
# coding=utf-8

"""
@version: v1.0 
@author: zhangyihong 
@contact: zhangyihong@kingsoft.com 
@file: all_share_crawler.py 
@time: 2018/4/20 10:11 
@description:crawle all shanghai/shenzhen stocks data,use tushare daily
"""
import scrapy
from urllib import parse, request
import tushare as ts

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class AllShareCrawler():
    def __init__(self):
        pass
        # name = "all_share_crawler"
        # start_urls = [
        #     'http://q.10jqka.com.cn/'
        # ]
        #
        # def parse(self, response):
        #     count = 0 #var in crawle
        #     share_request_url = "http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{}/ajax/1/".format(
        #         count)
