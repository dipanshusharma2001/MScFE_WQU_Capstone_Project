# ETL & EDA Decisions Summary

## 1. Data Extraction and Cleaning
- **Dataset Used:** Open Asset Pricing (OAP) factor library, monthly frequency (1963–2023).
- **Selected Factors:**  
  - Book-to-Market (BM)  
  - Idiosyncratic Volatility (IdioVol3F)  
  - Investment  
  - Momentum (Mom12m)  
  - Operating Profitability (OperProf)  
  - Size
- **Data Source:** Retrieved via the `openassetpricing` Python package (open-source, public).
- **Cleaning Steps:**
  - Converted returns from percentage to decimal format.
  - Resampled to month-end frequency.
  - Forward and backward filled minor missing values.
  - Saved cleaned dataset as `inputs/clean/osap_factor_returns.csv`.

---

## 2. Exploratory Data Analysis (EDA)
### 2.1 Summary Statistics & Distributions
- Generated summary statistics and plotted return distributions for each factor.
- Observed heavier tails and higher volatility in Momentum and IdioVol3F.

### 2.2 Correlation & Stability
- Calculated Pearson and Spearman correlations.
- Conducted decade-wise correlation analysis and stability checks.
- Observed dynamic relationships between factors, with strongest correlations between IdioVol3F–OperProf and IdioVol3F–Size.

### 2.3 Time-Series Analysis
- Computed and visualized rolling mean, rolling standard deviation, rolling Sharpe ratios, and drawdowns (24M, 36M, 60M windows).
- Detected persistent volatility regimes (e.g., 2000, 2008, 2020).

### 2.4 Autocorrelation & Volatility Clustering
- ACF/PACF showed mild lag-1 autocorrelation for several factors.
- ARCH-LM and GARCH(1,1) tests confirmed strong volatility persistence (α₁ + β₁ ≈ 0.9–0.98).
- Recommended including lag-1 nodes and a latent volatility/regime node in Dynamic BN.

### 2.5 Predictive IC & Stationarity
- Time-series predictive IC showed mild short-horizon predictability (mostly at h=1).
- ADF/KPSS tests confirmed stationarity for most factors; Size and Mom12m showed episodic non-stationarity.
- Detected recent structural breaks via `ruptures` and rolling KPSS, supporting a regime-aware modeling approach.

---

## 3. Outputs & Final Prepared Datasets
- **Cleaned Monthly Returns:** `inputs/clean/osap_factor_returns.csv`
- **DBN Dataset (with lag-1 variables):** `inputs/clean/osap_factors_for_dbn.csv`
- **Regime-aware DBN Dataset:** `inputs/clean/osap_factors_for_dbn_with_regime.csv`
- **Segmented Regime Files:** `inputs/clean/osap_factors_for_dbn_regime_0.csv`, `inputs/clean/osap_factors_for_dbn_regime_1.csv`

All EDA artifacts (plots, summaries, CSVs) are stored under `Outputs/eda/`.

---

## 4. Key Takeaways
- Factor returns are largely stationary and mean-reverting, but exhibit regime-dependent volatility.
- Evidence supports the use of **Dynamic Bayesian Networks** with lag-1 temporal links and a **latent volatility/regime node**.
- The Influence Diagram can leverage GARCH/EWMA-based covariance structures for risk-adjusted decision-making.

