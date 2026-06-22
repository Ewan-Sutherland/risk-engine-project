# Importing libraries
import yfinance as yf
import pandas as pd
import numpy as np
from InverseNormal import inverseNormal

# Creating Variables
data = yf.download(["AAPL", "JPM", "XOM"], start="2018-01-01", end="2025-12-31")
close = data["Close"]
returns = close.pct_change().dropna()

# Portfolio weightings
w = np.array([1/3, 1/3, 1/3])

mu = returns.mean()
Sigma = returns.cov()

mu_p = w @ mu
var_p = w @ Sigma @ w
sigma_p = np.sqrt(var_p)

# VaR calculation
def VaR_Calc(confidence):
    z = inverseNormal(1 - confidence)
    VaR_p = -(mu_p + sigma_p * z)
    return VaR_p

print(VaR_Calc(0.95))
print(VaR_Calc(0.99))

sigma_individual = np.sqrt(np.diag(Sigma))

z = inverseNormal(1 - 0.95)
individual_VaRs = -(mu + sigma_individual * z)

undiversified = w @ individual_VaRs
print(undiversified)