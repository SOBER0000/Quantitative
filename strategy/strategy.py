'''
@Time   :  2021/10/7 11:01 上午 
@Author  :  pengdongen
@File    :  strategy.py    
'''

from jqdatasdk import *
import numpy as np
import data.stock as st
import matplotlib.pyplot as plt


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
    data['weekday'] = data.index.weekday
    # 周四买入
    data['buy_signal'] = np.where(data['weekday'] == 3, 1, 0)
    # 模拟周四周五重复买入
    data['buy_signal'] = np.where((data['weekday'] == 3) | (data['weekday'] == 4), 1, 0)
    # 周一卖出
    data['sell_signal'] = np.where(data['weekday'] == 0, -1, 0)
    # 模拟周一周二重复卖出
    data['sell_signal'] = np.where((data['weekday'] == 0) | (data['weekday'] == 1), -1, 0)
    # 整合信号
    data = compose_signal(data)
    # 计算收益率
    data = calculate_prof_pct(data)

    return data


if __name__ == '__main__':
    print('main')
    auth('18818795073', '795073')  # 账号是申请时所填写的手机号；密码为聚宽官网登录密码，新申请用户默认为手机号后6位
    df = week_period_strategy('000001.XSHE', 'daily', '2021-01-07', '2021-09-30')
    # print(df[['close', 'buy_signal', 'sell_signal', 'signal', 'profile_pct']])
    print(df.describe())
    df['profile_pct'].plot()
    plt.show()