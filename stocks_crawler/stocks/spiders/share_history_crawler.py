#!/usr/bin python
# coding=utf-8

"""
@version: v1.0 
@author: zhangyihong 
@contact: zhangyihong@kingsoft.com 
@file: share_history_crawler.py 
@time: 2018/4/20 15:12 
@description:
"""
import sys
import tushare as ts


class ShareHistory(object):
    def __init__(self, share_code, start_date, end_date):
        self.share_code = share_code
        self.start = start_date
        self.end = end_date

    """return
    -------
    DataFrame
    属性:日期 ，开盘价， 最高价， 收盘价， 最低价， 成交量， 价格变动 ，涨跌幅，5日均价，10日均价，20日均价，5日均量，10日均量，20日均量，换手率"""

    def get_hist_data(self):
        '''
        return
        -------
          DataFrame
              date 交易日期 (index)
              open 开盘价
              high  最高价
              close 收盘价
              low 最低价
              volume 成交量
              amount 成交金额
        '''
        df = ts.get_h_data(self.share_code, self.start, self.end, pause=1)
        ts.get_hist_data(self.share_code, self.start, self.end, pause=1)
        # df = ts.get_stock_basics() 股票基本信息，date=None,默认为上一个交易日
        ts.get_today_all()
        ts.get_k_data()
        ts.get_concept_classified()

        return None

    def get_classified(self):
        industry_df = ts.get_industry_classified()
        concept_df = ts.get_concept_classified()
        ts.inst_tops()
        ts.get_k_data()
        return None


if __name__ == "__main__":
    pass
