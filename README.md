**Value-at-Risk (VaR) Engine**

The goal of this project was to create a market risk engine that estimates the Value at Risk (VaR) for single assets and portfolios.
I did this using four individual methods, and then backtested those methods against real price history to verify they held up as expected.

This project was built from the ground up, including creating an inverse normal quantile function by hand to have a closer look and develop a greater understanding of the statistic behind it and how we can actually compute it. SciPy and known results are used to verify my own computations.

**The four methods**

1. Parametric (variance-covariance) VaR - this method assumes normally distributed returns: VaR = -(μ + σ · z), with our value of z supplied by the custom inverse-normal CDF computation.
2. Monte Carlo VaR - this method simulates returns and reads VaR off the simulated loss distribution. I was able to validate this by showing its convergence to the parametric figure as the number of simulations was increased.
3. Fat-tailed (Student-t) Monte Carlo - this method fits a Student-t to the return data and simulates from it which catches the heavy tails real returns exhibit.
4. Portfolio VaR - this method extends the parametric method to a weighted basket via the covariance matrix, σ_p = √(wᵀΣw) and quantifies the benefit from diversification.

All the figures and data used are measured on AAPL daily returns 2018 - 2025 (plus JPM and XOM for the portfolio).

**The key results**

Real returns are fat-tailed, and a normal model understates extreme risk. This is demonstrated by the following:

1. The Distribution test: Jarque-Bera firmly rejects normality, by looking at the data we can see that excess kurtosis ≈ +6.43 (which means heavily weighted tails), and a fitted Student-t has only ≈ 3.3 degrees of freedom. This evidence suggests that it is strongly fat-tailed.
2. Simulation: the Student-t 99% VaR (≈ 5.25%) comes out ~19% higher than the normal 99% VaR (≈ 4.40%). The normal model underestimates the outer tails whilst at 95% the two are close. 
3. Backtest (out-of-sample): by walking forward through history and counting the breaches, the 95% VaR is well calibrated (4.63% breach rate vs a 5% target), but the 99% VaR over breaches its target (1.59% vs a 1% target) - this helps us by confirming the tail underestimate on the real data. Switching the 99% model to the fat-tailed version (using Student-t) improves the breach rate to 1.19% which is much closer to the target.

**Looking at a diversified portfolio**

I was able to quantify the benefits of portfolio diversification by looking at an equally weighted portfolio of AAPL/JPM/XOM which had a 95% VaR of ≈ 2.36%, versus ≈ 3.03% if the three assets moved in lockstep. This is a diversification benefit of ≈ 0.66 percentage points (≈ 22%) arising entirely from the off-diagonal covariances.

**The Files:**

VaRCalculator.py - parametric VaR plus both Monte Carlo methods (single asset).

InverseNormal.py - from-scratch inverse normal CDF: Acklam's rational approximation refined by one step of Halley's method. Matches SciPy's norm.ppf to ~15 significant figures, with no SciPy in the computation.

NormalityTest.py - normality diagnostics (Jarque–Bera, skewness, kurtosis) and plots (histogram, Q - Q).

PortfolioLevelVaR.py - portfolio VaR via the covariance matrix; diversified vs undiversified comparison.

BacktestVaR.py - walk forward backtest of the 95% / 99% VaR (normal and Student-t) followed by the breach-rate calculation.

data_utils.py - shared data loading helper.

**Running it**

Requires Python 3 with numpy, pandas, scipy, matplotlib, statsmodels, and yfinance

**The limitations and extra notes**

1. The backtests rolling window adapts to changing volatility, but there is no explicit volatility clustering model, (e.g. GARCH). This could be a suitable next expansion of this project.
2. The Student-t backtest uses a single whole sample degrees of freedom estimate, which means the breach rate improves but does not exactly hit 1%.
3. The diversification figure depends on historical correlations, which tends to rise toward 1 in a crisis which will reduce the benefit of this in the times when it would be most effective.
