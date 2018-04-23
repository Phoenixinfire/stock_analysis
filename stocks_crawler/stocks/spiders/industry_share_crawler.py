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
import os
import scrapy
import time
import codecs

current_path = os.getcwd()
data_path = os.path.abspath(os.path.dirname(os.getcwd())+"/../../data")
print(data_path)

if not os.path.exists(data_path):
    os.makedirs(data_path)

today_date_str = time.strftime("%Y-%m-%d", time.localtime())


class IndustryShareCrawler(scrapy.Spider):
    name = "industry_share_crawler"
    start_urls = [
        "http://q.10jqka.com.cn/thshy/"
    ]

    def parse(self, response):
        for industry_selector in response.css("div.cate_group a::attr(href)"):
            yield response.follow(industry_selector, self.parse_industry)

    def parse_industry(self, response):
        industry_name = response.css("div.heading div.board-hq h3::text").extract_first()
        industry_code = response.css("div.heading div.board-hq h3 span::text").extract_first()

        industry_info = response.css("div.heading div.board-infos dl")

        data_header = ["industry_name", "industry_code", "date"]  # 概念板块数据抬头
        one_row_data_value = [industry_name, industry_code, today_date_str]  # 每个概念的数据

        for index in industry_info:
            index_name = index.css("dt::text").extract_first()
            if index_name == "涨跌家数":
                data_header.append("上涨家数")
                data_header.append("下跌家数")
                index_data = index.css("dd span::text").extract()
                if len(index_data) == 0:
                    one_row_data_value.extend(["", ""])
                else:
                    one_row_data_value.extend(index_data)
            else:
                index_data = index.css("dd::text").extract_first()
                data_header.append(index_name)
                one_row_data_value.append(index_data)

        if os.path.exists(u"{}/industry_share_data.csv".format(data_path)):
            with codecs.open(u"{}/industry_share_data.csv".format(data_path), 'a+', 'utf-8') as f:
                f.write("\t".join(one_row_data_value) + "\n")
        else:
            with codecs.open(u"{}/industry_share_data.csv".format(data_path), 'a+', 'utf-8') as f:
                f.write("\t".join(data_header) + "\n")
                f.write("\t".join(one_row_data_value) + "\n")
