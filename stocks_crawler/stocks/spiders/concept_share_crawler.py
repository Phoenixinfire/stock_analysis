#!/usr/bin python
# coding=utf-8

"""
@version: v1.0 
@author: zhangyihong 
@contact: zhangyihong@kingsoft.com 
@file: concept_share_crawler.py 
@time: 2018/4/20 10:10 
@description:crawle tonghuashun concept section data
"""
import os
import scrapy
import time
import codecs

current_path=os.path.abspath(".")
data_path=os.path.join(current_path,"../data")

if !os.path.exists(data_path):
    os.makedirs(data_path)

today_date_str=time.strftime("%Y-%m-%d",time.localtime())

class ConceptShareCrawler(scrapy.Spider):
    
    name = "concept_share_crawler"
    start_urls = [
        "http://q.10jqka.com.cn/gn/"
    ]

    def parse(self, response):
        for concept_selector in response.css("div.cate_group a::attr(href)"):
            yield response.follow(concept_selector,self.parse_concept)
    
    def parse_concept(self,response):
        concept_name = response.css("div.heading div.board-hq h3::text").extract_first()
        concept_code = response.css("div.heading div.board-hq h3 span::text").extract_first()

        concept_info = response.css("div.heading div.board-infos dl")
        
        data_header=["concept_name","concept_code","date"] #概念板块数据抬头
        one_row_data_value=[concept_name,concept_code,today_date_str] #每个概念的数据

        for index in concept_info:
            index_name=index.css("dt::text").extract_first()
            index_data=index.css("dd::text").extract_first()
            data_header.append(index_name)
            one_row_data_value.append(index_data)

        if os.path.exists(u"{}/concept_share_data.csv".format(data_path)):
            with codecs.open(u"{}/concept_share_data.csv".format(data_path),'a+','utf-8') as f:
                f.write("\t".join(one_row_data_value)+"\n")
        else:
            with codecs.open(u"{}/concept_share_data.csv".format(data_path),'a+','utf-8') as f:
                f.write("\t".join(data_header)+"\n")
                f.write("\t".join(one_row_data_value)+"\n")