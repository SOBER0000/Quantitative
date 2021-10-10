'''
@Time   :  2021/10/7 11:01 上午 
@Author  :  pengdongen
@File    :  strategy.py    
'''

from jqdatasdk import *
import numpy as np
import data.stock as st
import matplotlib.pyplot as plt
import pandas as pd


def compose_signal(data):
    """
    整合买入、卖出信号
    :param data:
    :return:
    """
    data['buy_signal'] = np.where((data['buy_signal'] == 1) & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1) & (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])
    data['signal'] = data['buy_signal'] + data['sell_signal']

    return data


def calculate_prof_pct(data):
    """
    计算单次收益率：开仓、平仓
    :param data:
    :return:
    """
    data.loc[data['signal'] != 0, 'profile_pct'] = data['close'].pct_change()  # 筛选信号不为0的，并计算涨跌幅
    data = data[data['signal'] == -1]   # 筛选平仓时的收益率

    return data


def calculate_total_pct(data):
    """
    计算累计收益率
    :param data: Dataframe
    :return:
    """
    data['total_pct'] = pd.DataFrame(1 + data['profile_pct']).cumprod() - 1

    return data


def calculate_max_drawdown(data):
    """
    计算最大回撤
    :param data:
    :return:
    """
    # 计算时间周期内最大净值
    data['roll_max'] = data['close'].rolling(window=7, min_periods=1).max()
    # 计算当天回撤比：（谷值-峰值）/峰值 = 谷值/峰值-1
    data['daily_dd'] = data['close'] / data['roll_max'] - 1
    # 选取时间周期内最大回撤比，即最大回撤
    data['max_dd'] = data['daily_dd'].rolling(window=7, min_periods=1).min()

    return data


def calculate_sharpe(data):
    """
    计算夏普比率：（回报率的均值 - 无风险利率）/ 回报率的标准差
    :param data:
    :return:日夏普比率和年化夏普比率
    """
    # 回报率均值 == 日涨跌幅均值（股票）
    daily_pct = data['close'].pct_change()
    return_avg = daily_pct.mean()
    # 无风险利率近似于0
    # 回报率标准差 == 日涨跌幅标准差
    return_std = pd.DataFrame(daily_pct).std()
    # 计算夏普比率
    sharpe = return_avg / return_std
    # 计算年化夏普比率(一年有252个交易日): 回报率的均值*252 - 无风险利率）/ 回报率的标准差*根号252
    sharpe_year = sharpe * np.sqrt(252)

    return sharpe, sharpe_year


def week_period_strategy(code, time_fre, start_date=None, end_date=None):
    """
    模拟买入、卖出信号
    :param code:
    :param time_fre:
    :param start_date:
    :param end_date:
    :return:
    """
    data = st.get_single_price(code, time_fre, start_date, end_date)
    print(data)
    data['weekday'] = data.index.weekday
    # 周四买入
    data['buy_signal'] = np.where(data['weekday'] == 3, 1, 0)
    # # 模拟周四周五重复买入
    # data['buy_signal'] = np.where((data['weekday'] == 3) | (data['weekday'] == 4), 1, 0)
    # 周一卖出
    data['sell_signal'] = np.where(data['weekday'] == 0, -1, 0)
    # # 模拟周一周二重复卖出
    # data['sell_signal'] = np.where((data['weekday'] == 0) | (data['weekday'] == 1), -1, 0)
    # 整合信号
    data = compose_signal(data)
    # # 计算收益率
    data = calculate_prof_pct(data)
    # # 计算累计收益率
    data = calculate_total_pct(data)

    return data


if __name__ == '__main__':
    print('main')
    # df_pct = pd.DataFrame()
    start_date = '2006-01-01'
    end_date = '2021-01-01'
    auth('18818795073', '795073')  # 账号是申请时所填写的手机号；密码为聚宽官网登录密码，新申请用户默认为手机号后6位
    # shuanghui = week_period_strategy('000895.XSHE', 'daily', start_date, end_date)
    # mairui = week_period_strategy('300760.XSHE', 'daily', start_date, end_date)
    # maotai = week_period_strategy('600519.XSHG', 'daily', start_date, end_date)
    # df_pct['shuanghui_total_pct'] = shuanghui['total_pct']
    # df_pct['mairui_total_pct'] = mairui['total_pct']
    # df_pct['maotai_total_pct'] = maotai['total_pct']

    # df = st.get_single_price('600519.XSHG', 'daily', start_date, end_date)
    # # print(df)
    # df = calculate_max_drawdown(df)
    # print(df[['close', 'roll_max', 'daily_dd', 'max_dd']])
    # df[['daily_dd', 'max_dd']].plot()
    # plt.show()

    df = st.get_single_price('000001.XSHE', 'daily', start_date, end_date)
    sharpe = calculate_sharpe(df)
    print(sharpe)

