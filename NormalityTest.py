# Importing libraries
from scipy.stats import skew, kurtosis, jarque_bera, probplot
import matplotlib.pyplot as plt
from data_utils import get_returns

# Creating Variables
returns = get_returns("AAPL")

# Histogram of AAPL daily returns
plt.figure()
plt.hist(returns, bins=50)
plt.title("AAPL daily returns")
plt.xlabel("daily return")
plt.ylabel("frequency")
plt.show()

# Q-Q plot
plt.figure()
probplot(returns, dist="norm", plot=plt)
plt.show()

# Statistical tests
print(jarque_bera(returns))
print(skew(returns))
print(kurtosis(returns))
