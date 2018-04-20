#!/usr/bin python
# coding=utf-8

"""
@version: v1.0 
@author: zhangyihong 
@contact: zhangyihong@kingsoft.com 
@file: simulate_request.py 
@time: 2018/4/20 11:19 
@description:
"""
from urllib import request, parse
import json

if __name__ == "__main__":
    count = 8  # var in crawle
    share_request_url = "http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{}/ajax/1/".format(
        count)
    industry="http://q.10jqka.com.cn/thshy/"
    baidu = "http://www.baidu.com"
    sina="http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssl_bkzj_bk?pa" \
         "ge=9&num=20&sort=netamount&asc=0&fenlei=1"

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/65.0.3325.181 Safari/537.36"

    headers = {'User-Agent': user_agent}

    #print(user_agent)
    #print(headers)

    req = request.Request(sina, headers=headers)
    response = request.urlopen(req)

    print(response.read().decode('gbk'))

    # f = request.urlopen(share_request_url)
    # print(share_request_url)
    # f_data = f.read()
    # print(f_data.decode("utf-8"))
    # print(f.status)
