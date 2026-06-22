# Importing libraries
import yfinance as yf
import pandas as pd
import numpy as np
from InverseNormal import inverseNormal
from scipy.stats import t
from data_utils import get_returns

# Creating Variables
returns = get_returns("AAPL")
mu = returns.mean()
sigma = returns.std()

# VaR calculation
def VaR_Calc(confidence):
    z = inverseNormal(1 - confidence)
    VaR = -(mu+sigma*z)
    return VaR

print(VaR_Calc(0.95))
print(VaR_Calc(0.99))

# Monte Carlo simulation
def monte_carlo(N):
    rng = np.random.default_rng()
    sims = rng.normal(mu, sigma, N)
    VaR_95 = -np.percentile(sims, 5)
    VaR_99 = -np.percentile(sims, 1)
    return VaR_95, VaR_99

print(monte_carlo(100_000))
print(monte_carlo(1_000_000))

df, loc, scale = t.fit(returns)
sims_t = t.rvs(df, loc=loc, scale=scale, size=1_000_000)
VaR_95_t = -np.percentile(sims_t, 5)
VaR_99_t = -np.percentile(sims_t, 1)

print(VaR_95_t, VaR_99_t)