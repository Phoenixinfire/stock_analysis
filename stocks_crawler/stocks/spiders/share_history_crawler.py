#!/usr/bin python
# coding=utf-8

"""
@version: v1.0 
@author: zhangyihong 
@contact: zhangyihong@kingsoft.com 
@file: share_history_crawler.py 
@time: 2018/4/20 15:12 
@description:download share history data using tuhsare api,note:all tushare api return pandas dataframe
"""

import sys
import tushare as ts
import codecs
import os
import time
from datetime import datetime, timedelta

current_path = os.getcwd()
data_path = os.path.abspath(os.path.dirname(os.getcwd()) + "/../../data")
if not os.path.exists(data_path):
    os.makedirs(data_path)
print(data_path)


class ShareHistory(object):
    def __init__(self, start_date, end_date):
        self.start = start_date
        self.end = end_date
        self.today = time.strftime("%Y-%m-%d", time.localtime())

    def get_top_inst_list(self, task=None):
        """
        获取每日龙虎榜列表(龙虎榜上榜是根据上榜原因定的，因此有的股票可能会有多个原因，存在多条记录)，并保存到文件中
        获取当日机构购买详情，不能赋值日期，默认只能获取最近一天的交易详情
        Parameters
        ----------
        task:指定任意参数表示获取某一天的龙虎榜，否则为获取当日的龙虎榜

        """
        d = self.today if task is None else self.end
        top_list_df = ts.top_list(d)
        inst_detail_df = ts.inst_detail() if task is None else None

        if os.path.exists(u"{}/top_list_data.csv".format(data_path)):
            with codecs.open(u"{}/top_list_data.csv".format(data_path), "a+", "utf-8") as f:
                top_list_df.to_csv(f, header=False, sep="\t", index=True)
        else:
            with codecs.open(u"{}/top_list_data.csv".format(data_path), "a+", "utf-8") as f:
                top_list_df.to_csv(f, header=True, sep="\t", index=True)

        if inst_detail_df is not None:
            if os.path.exists(u"{}/inst_detail_data.csv".format(data_path)):
                with codecs.open(u"{}/inst_detail_data.csv".format(data_path), "a+", "utf-8") as f:
                    top_list_df.to_csv(f, header=False, sep="\t", index=True)
            else:
                with codecs.open(u"{}/inst_detail_data.csv".format(data_path), "a+", "utf-8") as f:
                    top_list_df.to_csv(f, header=True, sep="\t", index=True)

    def get_top_inst_count(self, days=5):
        """
        获取个股在近5、10、30、60日的龙虎榜上榜次数、累积购买额、累积卖出额、净额、买入席位数和卖出席位数。
        获取机构的近5、10、30、60日累积买入次数
        具体返回参数参考tushare.cap_tops和tushare.inst_tops
        Parameters：
        ----------
        days:5、10、30、60,表示统计周期
        """
        top_count_df = ts.cap_tops(days=days, retry_count=5, pause=1)
        with codecs.open(u"{}/cap_tops_count_{}_{}.csv".format(data_path, days, self.today), 'w+', "utf-8") as f:
            top_count_df.to_csv(f, header=True, sep="\t", index=True)

        inst_tops_df = ts.inst_tops(days=days, retry_count=5, pause=1)
        with codecs.open(u"{}/inst_tops_count_{}_{}.csv".format(data_path, days, self.today), 'w+', "utf-8") as f:
            top_count_df.to_csv(f, header=True, sep="\t", index=True)

    def batch_get_top_inst_count(self):
        """
        获取5、10、30、60天周期的所有上榜数据
        """
        self.get_top_inst_count(days=5)
        self.get_top_inst_count(days=10)
        self.get_top_inst_count(days=30)
        self.get_top_inst_count(days=60)

    def get_history_data(self, share_code, share_name, time_to_market_str, task=None, to_market_days=90):
        """
        调用tushare.get_k_data,获得股票的历史数据
        Parameters
        ----------
        share_code:股票代码
        task:用于指定日期任务，None默认今天，非None则使用指定日期
        to_market_days:上市日期距今多少天，默认90天
        """
        # share_info_df = ts.get_stock_basics()
        # time_to_market = str(share_info_df.loc[share_code]['timeToMarket'])  # 上市日期YYYYMMDD
        # time_to_market_str = time_to_market[:4] + "-" + time_to_market[4:6] + "-" + time_to_market[6:]  # YYYY-MM-DD
        print(share_code)
        time_to_market_dateformat = datetime.strptime(time_to_market_str, "%Y-%m-%d")
        time_to_get_data_base = self.today if task is None else self.end
        time_to_get_data_base_dateformat = datetime.strptime(time_to_get_data_base, "%Y-%m-%d")
        day_delta = (time_to_get_data_base_dateformat - time_to_market_dateformat).days
        if day_delta > to_market_days:
            share_k_day_data_df = ts.get_k_data(share_code, start=self.start, end=time_to_get_data_base, retry_count=5,
                                                pause=1)
            share_k_day_data_df["name"] = share_name
            share_k_week_data_df = ts.get_k_data(share_code, start=self.start, end=time_to_get_data_base, ktype="W",
                                                 retry_count=5, pause=1)
            share_k_day_data_df["name"] = share_name
            if os.path.exists(u"{}/share_k_day_data.csv".format(data_path)):
                with codecs.open(u"{}/share_k_day_data.csv".format(data_path), "a+", "utf-8") as f:
                    share_k_day_data_df.to_csv(f, header=False, sep="\t", index=True)
            else:
                with codecs.open(u"{}/share_k_day_data.csv".format(data_path), "a+", "utf-8") as f:
                    share_k_day_data_df.to_csv(f, header=True, sep="\t", index=True)

            if os.path.exists(u"{}/share_k_week_data.csv".format(data_path)):
                with codecs.open(u"{}/share_k_week_data.csv".format(data_path), "a+", "utf-8") as f:
                    share_k_week_data_df.to_csv(f, header=False, sep="\t", index=True)
            else:
                with codecs.open(u"{}/share_k_week_data.csv".format(data_path), "a+", "utf-8") as f:
                    share_k_week_data_df.to_csv(f, header=True, sep="\t", index=True)
        else:
            # raise Exception("{}，该股票上市日期距离查询起始日期不足{}天！".format(share_code, to_market_days))
            print("{}，该股票上市日期距离查询起始日期不足三个月！".format(share_code))

    def get_share_basics(self):
        """
        获取股票的基本信息
        Parameters
        ----------
        无参数，全部导出所有股票信息
        """
        share_bascis_info_df = ts.get_stock_basics()
        share_bascis_info_df.to_csv(u"{}/share_basics_info.csv".format(data_path), header=True, sep="\t", index=False)

    def get_sina_dd_ticks(self, share_code, share_name, time_to_market_str, task, vol=1, to_market_days=90):
        """
        获取交易数据
        Parameters
        ----------
        share_code:股票代码
        task:用于指定日期任务，None默认今天，非None则使用指定日期
        vol:自定义交易的手数，默认全部交易数据，可以提高这么值对交易数据进行筛选
        """
        # share_info_df = ts.get_stock_basics()
        # time_to_market = str(share_info_df.loc[share_code]['timeToMarket'])  # 上市日期YYYYMMDD
        # share_name = str(share_info_df.loc[share_code]['name'])  # 上市日期YYYYMMDD
        # time_to_market_str = time_to_market[:4] + "-" + time_to_market[4:6] + "-" + time_to_market[6:]  # YYYY-MM-DD
        time_to_market_dateformat = datetime.strptime(time_to_market_str, "%Y-%m-%d")
        time_to_get_data_base = self.today if task is None else self.end
        time_to_get_data_start = datetime.strptime(self.start, "%Y-%m-%d")
        time_to_get_data_base_dateformat = datetime.strptime(time_to_get_data_base, "%Y-%m-%d")
        day_delta = (time_to_get_data_base_dateformat - time_to_market_dateformat).days
        if day_delta > to_market_days:
            print("you come in if")
            for i in range((time_to_get_data_base_dateformat - time_to_get_data_start).days + 1):
                day = time_to_get_data_start + timedelta(days=i)

                print(datetime.strftime(day, "%Y-%m-%d"))
                try:
                    sina_dd_ticks_df = ts.get_tick_data(code=share_code, date=datetime.strftime(day, "%Y-%m-%d"),
                                                        retry_count=5, pause=1, src='tt')
                except:
                    sina_dd_ticks_df = ts.get_tick_data(code=share_code, date=datetime.strftime(day, "%Y-%m-%d"),
                                                        retry_count=5, pause=1, src='sn')
                if sina_dd_ticks_df is not None:
                    sina_dd_ticks_df["date"] = datetime.strftime(day, "%Y-%m-%d")
                    sina_dd_ticks_df['code'] = share_code
                    sina_dd_ticks_df['name'] = share_name
                    if os.path.exists(u"{}/share_sina_dd_ticks.csv".format(data_path)):
                        with codecs.open(u"{}/share_sina_dd_ticks.csv".format(data_path), "a+", "utf-8") as f:
                            sina_dd_ticks_df.to_csv(f, header=False, sep="\t", index=True)
                    else:
                        with codecs.open(u"{}/share_sina_dd_ticks.csv".format(data_path), "a+", "utf-8") as f:
                            sina_dd_ticks_df.to_csv(f, header=True, sep="\t", index=True)
        else:
            print("{}，该股票上市日期距离查询起始日期不足三个月！".format(share_code))


if __name__ == "__main__":
    share_data_object = ShareHistory("2017-10-09", "2018-04-20")
    share_info_df = ts.get_stock_basics()
    share_info_df = share_info_df[share_info_df.index.map(lambda idx: not idx.startswith("300")).values].head(20)
    for share_code in share_info_df.index.values:
        time_to_market = str(share_info_df.loc[share_code]['timeToMarket'])  # 上市日期YYYYMMDD
        share_name = str(share_info_df.loc[share_code]['name'])  # 上市股票名称
        time_to_market_str = time_to_market[:4] + "-" + time_to_market[4:6] + "-" + time_to_market[6:]  # YYYY-MM-DD
        share_data_object.get_sina_dd_ticks(share_code, share_name, time_to_market_str, task=5, to_market_days=250)
        share_data_object.get_history_data(share_code, share_name, time_to_market_str, task=5, to_market_days=250)
