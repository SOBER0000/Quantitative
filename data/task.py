from jqdatasdk import *
import pandas as pd
import time
import datetime
from jqdatasdk import finance

auth('18818795073', '795073')  # 账号是申请时所填写的手机号；密码为聚宽官网登录密码，新申请用户默认为手机号后6位

# 设置行列不忽略
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 20)

'''计算贵州茅台最新市值数据'''

# 获取贵州茅台日k数据 600519.XSHG  贵州茅台酒股份有限公司
# df = get_price('600519.XSHG', end_date=datetime.date.today(), count=1, frequency='daily')
df = get_price('600519.XSHG', end_date=datetime.date.today(), count=1, frequency='daily')
print("=== datetime.date.today():", datetime.date.today())
df_valutation = get_fundamentals(query(valuation).filter(valuation.code == '600519.XSHG'), date=datetime.date.today())
close_price = df['close'][0]
print(df_valutation)
total_stock_count = df_valutation['capitalization'][0]  # 万股
print("茅台最新总股本（万股）", total_stock_count)
valuation = close_price * total_stock_count*10000/100000000
print("贵州茅台最新市值（亿）", valuation)

'''计算贵州茅台市盈率（静态）'''
df_indicator = get_fundamentals(query(indicator).filter(indicator.code == '600519.XSHG'), date=datetime.date.today())
df_income = get_fundamentals(query(income).filter(income.code == '600519.XSHG'), date=datetime.date.today())
print(df_indicator)
print(df_income)
eps = df_indicator['eps'][0]
print("close_price:", close_price)
print('eps:', eps)
pe = close_price/eps
# pe = df_valutation['market_cap'][0]*100000000 / df_income['np_parent_company_owners'][0]
print("贵州茅台最新市盈率(静态)：", pe)

