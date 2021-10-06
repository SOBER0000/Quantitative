from jqdatasdk import *
import time
import pandas as pd

auth('18818795073', '795073')  # 账号是申请时所填写的手机号；密码为聚宽官网登录密码，新申请用户默认为手机号后6位

# # 获取A股所有股票代号
# stocks = list(get_all_securities(['stock']).index)
# print(len(stocks))
#
# # 获取A股所有股票行情
# # panel = get_price(stocks, "2021-09-01", "2021-09-10")
# # print(panel)
#
# for stock_code in stocks:
#     print("正在获取股票行情数据，股票代码：", stock_code)
#     df = get_price(stock_code, count=10, end_date='2021-09-10', frequency='daily')
#     print(df)
#     time.sleep(3)

# 设置行列不忽略
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 10)

# 获取平安银行2020年日k数据
df = get_price('000001.XSHG', start_date='2020-01-01', end_date='2020-12-31', frequency='daily')

# 转换为周K数据 开盘价、收盘价、最高价、最低价
df['weekday'] = df.index.weekday
print(df)
df_week = pd.DataFrame()
df_week['open'] = pd.to_numeric(df['open']).resample('W').first()
df_week['close'] = pd.to_numeric(df['close']).resample('W').last()
df_week['high'] = pd.to_numeric(df['high']).resample('W').max()
df_week['low'] = pd.to_numeric(df['low']).resample('W').min()
# 统计周成交量、成交额
df_week['volume'] = pd.to_numeric(df['volume']).resample('W').sum()
df_week['money'] = pd.to_numeric(df['money']).resample('W').sum()
# print("week K:", df_week)

# 转换为月K数据 开盘价、收盘价、最高价、最低价
df_month = pd.DataFrame()
df_month['open'] = pd.to_numeric(df['open']).resample('M').first()
df_month['close'] = pd.to_numeric(df['close']).resample('M').last()
df_month['high'] = pd.to_numeric(df['high']).resample('M').max()
df_month['low'] = pd.to_numeric(df['low']).resample('M').min()
# 统计月成交量、成交额
df_month['volume'] = pd.to_numeric(df['volume']).resample('M').sum()
df_month['money'] = pd.to_numeric(df['money']).resample('M').sum()
print("month K:", df_month)



