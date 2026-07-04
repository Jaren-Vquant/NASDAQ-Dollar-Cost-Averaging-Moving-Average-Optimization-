import pandas as pd
import numpy as np


"""
计算定投策略绩效指标,回测纳指30年(1990-2020)的定投策略，计算收益、最大回撤、夏普比率，并需计入交易成本
引入MA200均线择时：以日线收盘价计算MA200，每月定投日价格在MA200上方才定投，否则暂停
"""
# 读取数据
nasdaq = pd.read_csv("nasdaq_1990_2020.csv", index_col=0, parse_dates=True)

# 只取收盘价，同时转化为Series
close = nasdaq["Close"].squeeze()

# 定投策略初始设置
monthly_invest = 10000  # 每月定投金额
transaction_cost = 0.001  # 交易成本0.1%
risk_free = 0.02  # 以2%无风险国债利率为基准

# 用日线数据计算MA200
ma200 = close.rolling(200).mean()

# 取每月第一个交易日的价格和对应的MA200
monthly_close = close.groupby(close.index.to_period("M")).first()
monthly_ma200 = ma200.groupby(ma200.index.to_period("M")).first()

# 择时：每月定投日价格在MA200上方才买入，否则份额为0
shares = monthly_invest / monthly_close
shares[monthly_close < monthly_ma200] = 0

# 累计持有的股票数量+定投花费的所有成本+最终市值
total_shares = shares.cumsum()
actual_months = (shares > 0).sum() #得出实际投资的月总数
total_cost = monthly_invest * (1 + transaction_cost) * actual_months
final_value = total_shares.iloc[-1] * monthly_close.iloc[-1]

# 绩效指标
years = len(monthly_close) / 12
total_return = (final_value - total_cost) / total_cost * 100
annual_return = ((final_value / total_cost) ** (1 / years) - 1) * 100

# 计算最大回撤
portfolio_value = total_shares * monthly_close
rolling_max = portfolio_value.cummax()
max_drawdown = ((portfolio_value - rolling_max) / rolling_max).min() * 100

# 计算夏普比率
monthly_returns = portfolio_value.pct_change().dropna()
sharpe = (monthly_returns.mean() - risk_free/12) / monthly_returns.std() * np.sqrt(12)

# 输出
print("===== MA200均线择时定投 (1990-2020) =====")
print(f"实际投入月数: {actual_months} / {len(monthly_close)} 个月")
print(f"总投入:     ${total_cost:,.2f}")
print(f"最终市值:   ${final_value:,.2f}")
print(f"总收益率:   {total_return:.2f}%")
print(f"年化收益率: {annual_return:.2f}%")
print(f"最大回撤:   {max_drawdown:.2f}%")
print(f"夏普比率:   {sharpe:.2f}")