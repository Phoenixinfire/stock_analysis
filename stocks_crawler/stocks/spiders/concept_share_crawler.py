#!/usr/bin python
# coding=utf-8

"""
@version: v1.0 
@author: zhangyihong 
@contact: zhangyihong@kingsoft.com 
@file: concept_share_crawler.py 
@time: 2018/4/20 10:10 
@description:crawle tonghuashun concetp section data
"""
import scrapy

class ConceptShareCrawler(scrapy.Spider):
    name = "concept_share_crawler"
    start_urls = [
        "http://q.10jqka.com.cn/gn/"
    ]

    def parse(self, response):
        pass
