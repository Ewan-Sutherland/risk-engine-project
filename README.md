**Projects**

A collection of my quantitative finance projects. Each one has its own folder with its own write-up and code.

**Value-at-Risk Engine** (in [`risk-engine/`](risk-engine/))

A market risk engine that estimates Value at Risk for single assets and portfolios using four methods (parametric variance-covariance, Monte Carlo, fat-tailed Student-t Monte Carlo, and a covariance-matrix portfolio extension), then backtests them against real price history to check they hold up. It is built from the ground up, including an inverse-normal quantile function written by hand - Acklam's rational approximation refined with one step of Halley's method, which matches SciPy's norm.ppf to about 15 significant figures with no SciPy in the actual computation.

The main result is that real returns are fat-tailed and a normal model understates extreme risk. On AAPL daily returns from 2018 to 2025, Jarque-Bera firmly rejects normality (excess kurtosis around 6.43, and a fitted Student-t has only about 3.3 degrees of freedom). Walking the VaR forward through history, the 99% normal model over-breaches its target (1.59% against a 1% target), and switching to the Student-t model pulls that back to 1.19%.

The full write-up, results and code are in [`risk-engine/`](risk-engine/).
