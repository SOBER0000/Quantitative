'''
@Time   :  2021/10/6 3:52 下午 
@Author  :  pengdongen
@File    :  stock.py.py    
'''

from jqdatasdk import *
import pandas as pd
import datetime
import os

data_root = '/Users/pengde/Desktop/Quant/data'


def get_stock_list():
    """
    获取A股所有股票代码列表
    :return:A股所有股票代码列表
    """
    stocks = list(get_all_securities(['stock']).index)
    return stocks


def get_index_list(index_symbol='000300.XSHG'):
    """
    获取指数成分股
    :param index_symbol: 指数的代码，默认沪深300
    :return:
    """
    stocks = get_index_stocks(index_symbol)
    return stocks


def get_single_price(code, time_fre, start_date=None, end_date=None):
    """
    获取单个股票的行情数据
    :param code:       股票代码
    :param time_fre:   指定获取的时间频级为分钟级（minute）或日级（daily）
    :param start_date: 开始时间
    :param end_date:   结束时间
    :return:
    """
    if start_date is None:
        start_date = get_security_info(code).start_date
    if end_date is None:
        end_date = datetime.date.today()
    data = get_price(code, frequency=time_fre, start_date=start_date, end_date=end_date)
    return data


def export_data(data, type, filename, mode=None):
    """
    导出股票数据
    :param data:     需要导出的数据
    :param type:     数据类型（行情数据、财务指标等）
    :param filename: 导出的文件名
    :param mode:     存储模式（a:追加 None：默认写入）
    :return:
    """
    file_root = data_root + '/' + type + '/' + filename + '.csv'
    data.index.names = ['date']
    if mode == 'a':
        data.to_csv(file_root, mode=mode, header=False)
        # 删除重复值
        data = pd.read_csv(file_root)  # 读取数据
        data = data.drop_duplicates(subset=['date'])  # 以日期列为准
        data.to_csv(file_root, index=False)  # 重新写入
    else:
        data.to_csv(file_root)

    print("已保存数据到", file_root)


def get_csv_data(code, type):
    """
    从csv文件中获取股票数据
    :param code: 股票代码
    :param type: 数据类型（行情数据、财务指标等）
    :return:
    """
    file_root = data_root + '/' + type + '/' + code + '.csv'
    data = pd.read_csv(file_root)
    return data


def transfer_price_freq(data, time_freq='W'):
    """
    转换数据转换为指定周期
    :param data:        需转换的数据
    :param time_freq:   指定转换周期
    :return:
    """
    data_trans = pd.DataFrame()
    data_trans['open'] = pd.to_numeric(data['open']).resample(time_freq).first()
    data_trans['close'] = pd.to_numeric(data['close']).resample(time_freq).last()
    data_trans['high'] = pd.to_numeric(data['high']).resample(time_freq).max()
    data_trans['low'] = pd.to_numeric(data['low']).resample(time_freq).min()

    return data_trans


def get_single_finance(code, date, start_date):
    """
    获取单个股票财务指标
    :param code:        股票代码
    :param date:        查询日期
    :param start_date:  查询年份（季度）
    :return:
    """
    data = get_fundamentals(query(indicator).filter(indicator.code == code), date=date, statDate=start_date)
    return data


def get_single_valuation(code, date, start_date):
    """
    获取单个股票估值指标
    :param code:        股票代码
    :param date:        查询日期
    :param start_date:  查询年份（季度）
    :return:
    """
    data = get_fundamentals(query(valuation).filter(valuation.code == code), date=date, statDate=start_date)
    return data


def calculate_change_pct(data):
    """
    计算股票数据的涨跌幅：（当期收盘价-前期收盘价）/前期收盘价
    :param data: dataframe，带有收盘价
    :return: dataframe，带有涨跌幅
    """
    data['close_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    return data


def update_dailay_price(code, type='price'):
    """
    更新指定股票数据
    :param code: 股票代码
    :param type: 默认行情数据
    :return:
    """
    file_root = data_root + '/' + type + '/' + code + '.csv'
    if os.path.exists(file_root):
        start_date = pd.read_csv(file_root, usecols=['date'])['date'].iloc[-1]
        data = get_single_price(code, 'daily', start_date, datetime.date.today())
        export_data(data, type, code, 'a')
    else:
        data = get_single_price(code, 'daily')
        export_data(data, type, code)


if __name__ == '__main__':
    print('main')
