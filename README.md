# Notes on elementary algorithmic trading using statistical modelling
This is a collection of IPython notebooks that cover introductory material on aspects of algorithmic trading. A mathematical approach is offered with some prior knowledge of basic probability and statistics assumed. The examples use real historical data pulled from Quandl and Yahoo Finance. This is done with help of the `finance` library included.

All information is sourced from Quantopian and Wikipedia. 

## Setup
In addition to the standard packages `numpy`, `scipy`, `matplotlib` and `jupyter-notebook` (to run the notebooks), you will need `pandas`, `statsmodels` and `seaborn`. Copy the `finance` folder into the same folder as the notebooks for the data-sourcing scripts to run. Alternatively there are PDFs of the notebooks in the `export` folder (might not be up to date).

## Outline
Topics are split into various themes of risk and statistical analysis.

### Introduction to the `pandas` time-series library
### Statistical analysis I
- Mean and variance
- Linear regression
- Linear correlation
- Residual analysis | *Breusch-Pagan and Ljung-Box tests*
- Statistical moments | *Jarque-Bera test*
- Confidence intervals | *Multiple comparisons bias*

### Statistical analysis II
- Autocorrelation and autoregressive (AR) models | *Information criterion on model parameter selection*
- Estimation of covariance matrices | *Ledoit-Wolf estimator*
- Stationarity | *Augmented Dickey-Fuller test, Wold's Theorem*
- Order of integration
- Cointegration

### Risk and strategy I
- Beta hedging | *Regression alpha and beta*
- Pairs trading | *Cointegration test on similar industry stocks*
    - Engle-Granger method
    - $z$-score normalisation and construction of an indicator
    - Out-of-sample test
- Position concentration risk | *Portfolio variance as a risk*

### Risk and strategy II
- Long short equity | *Equity ranking and further considerations*
- Portfolio Value-at-Risk
    - Historical (non-parametric) VaR
    - Real data example
- Conditional VaR | *CVaR as a better metric than VaR*
- ARCH and GARCH models
    - Simulation
    - Testing for ARCH behaviour
    - Fitting with MLE
    - Parameter estimation with GMM

---    
## Incomplete
Incomplete sets of notes due to lack of content or other limitations
### Statistical financial models
- Capital Asset Pricing Model (CAPM) | *The efficient frontier*
- Arbitrage Pricing Theory (APT) | *Risk factors using fundamental data* **(lack of fundamentals data source)**
