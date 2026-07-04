import yfinance as yf
import pandas as pd

# 获取纳斯达克指数日线数据 (^IXIC 是纳斯达克综合指数)
nasdaq = yf.download("^IXIC", start="1990-01-01", end="2020-12-31")

#保存到csv
nasdaq.to_csv("nasdaq_1990_2020.csv")
print("数据已保存到 nasdaq_1990_2020.csv")