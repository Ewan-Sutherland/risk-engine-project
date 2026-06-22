# Importing libraries
import numpy as np
from InverseNormal import inverseNormal
from scipy.stats import t
from data_utils import get_returns

# Creating Variables
returns = get_returns("AAPL")
rolling_mu = returns.rolling(250).mean()
rolling_sigma = returns.rolling(250).std()

# VaR calculation
def VaR_Calc(confidence):
    z = inverseNormal(1 - confidence)
    VaR = -(rolling_mu+rolling_sigma*z)
    return VaR

# Calculate breach rate
def breach_rate(p):
    predicted_VaR = VaR_Calc(p)
    breaches = returns.shift(-1) < -predicted_VaR
    breach_rate = breaches.sum() / breaches.count()
    return breach_rate

print(breach_rate(0.95))
print(breach_rate(0.99))



df, loc, scale = t.fit(returns)

z_t = t.ppf(0.01, df) * np.sqrt((df - 2) / df)
predicted_VaR_t = -(rolling_mu + rolling_sigma * z_t)

breaches_t = returns.shift(-1) < -predicted_VaR_t
breach_rate_t = breaches_t.sum() / breaches_t.count()

print(breach_rate_t)