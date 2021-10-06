'''
@Time   :  2021/10/6 5:09 下午 
@Author  :  pengdongen
@File    :  stock_test.py.py    
'''

import data.stock as st
from jqdatasdk import *

auth('18818795073', '795073')  # 账号是申请时所填写的手机号；密码为聚宽官网登录密码，新申请用户默认为手机号后6位

# 获取平安银行行情数据
# data = st.get_single_price('000001.XSHE', 'daily', '2021-09-01', '2021-09-30')
# print(data)

# 计算日K涨跌幅，验证准确性
# data = st.calculate_change_pct(data)
# print(data)

# 获取周K数据
# data = st.transfer_price_freq(data, 'W')
# print(data)

# 计算周k涨跌幅，验证准确性
# data = st.calculate_change_pct(data)
# print(data)

st.update_dailay_price('000001.XSHE')

