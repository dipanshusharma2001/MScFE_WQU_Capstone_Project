# DYNOTEARS PoC Development Summary
Logs, notes & ideas related to: https://github.com/dipanshusharma2001/MScFE_WQU_Capstone_Project/blob/main/notebooks/02_DYNOTEARS_PoC.ipynb


---
Note added on 6 Nov 2025
## TO DO 
Elaborate on the changes below.

### Changes made since M4 submission & following M5 peer review:

- Regime labels from EDA have been incorporated
- Code has been refactored & reusable functions were made
- Commments & docstrings have been added & expanded
- Corrected a calculation error in DBN parameter learning code in the previous version
- Model quality from a single train-test split was evaluated
- Portfolio optimization now utilizes ```cvxpy``` to incorporate constraints (total weights = 1, max weight per factor = 30 %). The optimization function also includes an adjustable risk-aversion coefficient.
- S&P 500 benchmark, equal-weight (1/N), and rolling MVO portfolios were added for comparisons
- Implemented walk-forward backtest with error handling for long only & long-short portfolios
---


## 1. Data Preparation
### 1.1 Data Processing
- Loaded factor returns data, which have been previously processed (https://raw.githubusercontent.com/dipanshusharma2001/MScFE_WQU_Capstone_Project/main/inputs/clean/osap_factor_returns.csv) & formatted values & datetime index.
- Index & macroeconomic data variables were arbitrarily selected & downloaded.
- Retrieved index levels & bond yield data from Yahoo Finance:
    - `^GSPC`: The S&P 500 index (renamed as `SP500`)
    - `^RUT`: The Russell 2000 index (renamed as `RSSL2K`)
    - `DX-Y.NYB`: US Dollar index (renamed as `USDIDX`)
    - `^IRX`: 13-week Treasury Bill yield (renamed as `TBILL13WK`)
- Retrieved macroeconomic indicator data from FRED:
    - `GDP`: Gross Domestic Product (GDP)
    - `UNRATE`: unemployment rate
    - `CPIAUCSL`: Consumer Price Index for All Urban Consumers: All Items in U.S. City Average (renamed as `INFLATION`)
    - `USEPUINDXD`: Economic Policy Uncertainty Index for United States (renamed as `POLICY`)
    - `TRESEGUSM052N`: Total Reserves excluding Gold for United States (renamed as `GLDRSRV`)
    - `WTISPLC`: Spot Crude Oil Price: West Texas Intermediate (WTI) (renamed as `CRUDOIL`)
### 1.2 Data Aggregation
- Factor, indices, and macroeconomic data were concatenated into a single dataframe using `outer` join.
- Factor returns were converted to cumulative return series for downstream trend-scanning labelling (next section).
- Data were padded using `ffill` and resampled monthly to produce the cleaned dataset.
### 1.3 Data Discretization with Trend Scanning
- Given that many of the variables are not stationary, trend scanning was used for data discretization.
- This method was taken from Lopez de Prado, *Machine Learning for Asset Managers*, pp. 67-72. The Python implementation below was modified from code adaptations by Endre Moen (https://github.com/emoen/Machine-Learning-for-Asset-Managers/blob/master/Machine_Learning_for_Asset_Managers/ch5_financial_labels.py).
- The labels were derived from the t-value $\hat{t}_{\hat{\beta_1}}$ associated with an estimated regressor coefficient $\hat{\beta_1}$ in a linear time model. Assuming we have a price / level series $\{x_t\}_{t=1,...,T}$, a regression model can be estimated:
$$x_{t+l} = \beta_0 + \beta_1 l + \varepsilon_{t+l}$$
$$\hat{t}_{\hat{\beta_1}} = \frac{\hat{\beta_1}}{\hat{\sigma}_{\hat{\beta_1}}}$$
where $\hat{\sigma}_{\hat{\beta_1}}$ is the standard error of $\hat{\beta_1}$, and $l = 0, ..., L-1$ and $L$ is the look-forward period.
- The result is a dataframe containing all variables with 3-state labels `[0, 1, 2]` indicating down-trend, no-trend, and up-trend.
### 1.4 Train-Test Dataset Split
- Trend label dataframe were split into 80:20 training:testing datasets.

---

## 2. Bayesian Network
### 2.1 Dynamic BN (DYNOTEARS) Structure Learning
- DYNOTEARS (Pamfil et al, 2020, https://proceedings.mlr.press/v108/pamfil20a.html) was arbitrarily chosen as a representative model to build a dynamic Bayesian network (DBN).
- The relevant parameters are as follows (only lag 1 is considered for now):
```
p = 1
lambda_w = 0.1
lambda_a = 0.1
w_threshold = 0.05
```
- The other parameters are set to default settings. Refer to the repo for more information on the different parameters: https://github.com/mckinsey/causalnex/blob/develop/causalnex/structure/dynotears.py.
- From the estimated BN structure (and its adjacency matrix), it seems only ```BM_lag1```, ```OperProf_lga1```, ```RSSL2K_lag1```, ```GDP_lag1```, ```SP500_lag0```, and ```UNRATE_lag0``` may have some direct causal influence on the factors.

### 2.2 Parameter Learning
- After the BN structure was estimated, the parameters were estimated.
- The result is the conditional probability tables (CPTs) associated with the BN.
### 2.3 An Inference Example
- An example of inference is presented. Since the goal is predict the states of the factors in the next time period (i.e. whether they will be in an up-trend or down-trend), the states of the following ```lag1``` variables were used as evidence for inference:
    - `GDP_lag1`
    - `RSSL2K_lag1`
    - `BM_lag1`
    - `Investment_lag1`
    - `OperProf_lag1`
- The marginal probabilities of the factors given the evidence can then be calculated.
---

## 3. Weight Allocation Optimization
### 3.1 State-Dependent Returns & Covariance Estimation
- To be able to perform utility optimization (for factor portfolio allocations), the inference from the BN above (which was built based on discretized data) need to be translated / converted / mapped / transformed into continuous estimates of future expected returns $\mu$ and covariance $\Sigma$.
- One idea (losely based on: Rebonato & Denev, 2012, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1824207) is to take the returns distributions from each of the 3 states, and treat them as a mixture.

- For an example, suppose there are two states $S \in \{0, 1\}$. If we assign probability of being in state 1, $\pi_1 = p$, and $\pi_0 = 1 - p$ then:
    - $\bar{\mu} = \mathbb{E}[R] = \sum_s \pi_s \mathbb{E}[R \mid s]$
    - $\text{Var}(R) = \sum_s \pi_s \text{Var}(R \mid s) + (\mathbb{E}[R \mid s] - \bar{\mu})(\mathbb{E}[R \mid s] - \bar{\mu})^\top \big)$ 
    
(standard law of total variance / mixture variance decomposition)

- In our case, the mean returns ($\mu_0, \mu_1, \mu_2$) and covariance matrix ($\Sigma_0, \Sigma_1, \Sigma_2$) associated with each of the 3 states were estimated.
- The expected returns were adjusted by the probabilities resulting from the BN inference above.

### 3.2 Factor Weight Optimization
#### 3.2.1 Weight Allocations Based on Traditional MVO
- Markowitz-style Mean-Variance Optimization (MVO) was performed on continuous returns data from the training set to be compared with the weight allocations from the dynamic BN (DBN) model below.
- As examples, only long-only maximum Sharpe ratio portfolios are considered in this notebook. For simplicity, the risk-free rate was assumed to be 0.
#### 3.2.1 Weight Allocations Based on DBN Model
- Using the state-dependent returns & variance estimates (section 3.1), optimization was performed again.
- Since there are 3 state / trend labels, from the way the labels were constructed, $\pi_0 = \pi_1 = \pi_2 = 1/3$ (this was also observed in the data too).
- The resulting weight allocations between the 6 factors were found to be different between MVO and DBN models.
---

## 4. Walk-Forward Backtest
- The cycle of inference & weights optimization was implemented on a rolling basis at every time step on the testing dataset (i.e., factor weight allocations were rebalanced every month). No model re-training was performed.
- As in section 2.3, as we move forward in time, we would observe the states of `GDP`, `RSSL2K`, `BM`, `Investment`, and `OperProf`, and treat them as a `lag1` observations. These observations were then used to infer the next-period factor states.
- **Assumptions**:
    - There are tradeable ETFs that exactly track these factor exposure and returns.
    - The marginal probabilities from BN inference was used to adjust the expected returns ($\mu_0, \mu_1, \mu_2$), but the covariance matrix ($\Sigma_0, \Sigma_1, \Sigma_2$) is assumed to be unchanging with time.
    - We can buy and sell at exactly the close of each month.
    - A simplistic fee structure of 5 % p.a. (charged monthly) applies (i.e., each month, 0.05/12 is deducted from our portfolio returns).
- The results indicate that the DBN portfolio mainly rotates between `OperProf`, `Investment`, `BM`, and `Mom12m`, with occasional little allocations to `IdioVol3F` and almost no allocations to `Size`.
- Assuming the above, the performance of this dynamic factor portfolio was compared to that of the static MVO portfolio (section 3.2.1) in terms of cumulative returns, CAGR, Sharpe ratio, and maximum drawdown. Although the maximum drawdowns were similar, the DBN portfolio would've outperformed the static MVO portfolio.
---

## **TO DO / For further considerations**
- So far, variables / features were chosen arbitrarily, somewhat based on variables commonly found in the econometric literature. We would like to include an information theoretic framework for building a more systematic feature selection process.
- We may not want to stick with DYNOTEARS model. Other causal structure learning algorithms can be explored, including those that don't require data discretization.
- Model parameter optimization has not been performed (e.g., with grid search) & model accuracy on test set has not been evaluated.
- Only lag 1 has been included. We may look at ACF or other data characteristics to determine if longer lags should be considered too.
- Although utility optimization has been performed, it is a separate module from the BN, and we have not built an integrated influence diagram (ID). This will be our next step.
- Tradeable ETFs that track specific risk factors may not always be available. Can we use the factors and the resulting ID to select individual stocks instead?
