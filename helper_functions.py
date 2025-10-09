"""
helper_functions.py
Custom helper functions for the MScFE Capstone Project - Causal Factor Investing
"""

from config import *

def compute_drawdown(ts: pd.Series) -> pd.Series:
    """
    Compute the drawdown series for a time series of returns.
    Parameters:
        ts (pd.Series): Time series of returns (in decimal form).
    Returns:
        pd.Series: Drawdown series as fraction of peak cumulative value.
    """
    cum = (1 + ts).cumprod()
    hwm = cum.cummax()
    dd = (cum - hwm) / hwm
    return dd
