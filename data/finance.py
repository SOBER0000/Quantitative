import jqdatasdk
from jqdatasdk import *
import time
import pandas as pd

""" 获取财务指标数据 """
jqdatasdk.auth('18818795073', '795073')  # 账号是申请时所填写的手机号；密码为聚宽官网登录密码，新申请用户默认为手机号后6位
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 100)


df_indicator = get_fundamentals(query(indicator), statDate='2020')
# print(df_indicator.head())
# df_indicator.to_csv('/Users/pengde/Desktop/Quant_Study/lessons/lesson_01/Quant/data/finance.csv')
# 基于盈利指标选股
# eps	每股收益EPS(元)	每股收益(摊薄)＝净利润/期末股本；分子从单季利润表取值，分母取季度末报告期股本值；净利润指归属于母公司股东的净利润(元)
# operating_profit	经营活动净收益(元)	营业总收入-营业总成本
# roe	净资产收益率ROE(%)	归属于母公司股东的净利润*2/（期初归属于母公司股东的净资产+期末归属于母公司股东的净资产）
# inc_operation_profit_year_on_year	营业利润同比增长率(%)	同比增长率就是指公司当年期的营业利润和上月同期、上年同期的营业利润比较。（当期的营业利润-上月（上年）当期的营业利润）/上月（上年）当期的营业利润绝对值=利润同比增长率。
df_indicator = df_indicator[(df_indicator['eps'] > 0) & (df_indicator['operating_profit'] > 214406045.46) & (df_indicator['roe'] > 10) & (df_indicator['inc_operation_profit_year_on_year'] > 10)]
df_indicator.index = df_indicator['code']   # 将股票代码设置为索引
# print(df_indicator.head())

''' 查询估值指标 '''
df_valuation = get_fundamentals(query(valuation), statDate='2020')
df_valuation.index = df_valuation['code']   # 将股票代码设置为索引
# print(df_valuation.head())

# 将估值指标加入财务指标数据中
df_indicator['pe_ratio'] = df_valuation['pe_ratio']  # 两个Dataframe数据将股票代码设置为索引后自动会匹配相应的市盈率到该股票
# 基于市盈率选股
df_indicator = df_indicator[df_indicator['pe_ratio'] < 30]
df_indicator.to_csv('/Users/pengde/Desktop/Quant_Study/lessons/lesson_01/Quant/data/select.csv')
print(df_indicator.head())
