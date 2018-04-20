#!/usr/bin python
# coding=utf-8

"""
@version: v1.0 
@author: zhangyihong 
@contact: zhangyihong@kingsoft.com 
@file: industry_share_crawler.py 
@time: 2018/4/20 10:11 
@description:crawle tonghuashun industry section data
"""
import scrapy


class IndustryShareCrawler(scrapy.Spider):
    name = "industry_share_crawler"
    start_urls = [
        "http://q.10jqka.com.cn/thshy/"
    ]

    def parse(self, response):
        pass

