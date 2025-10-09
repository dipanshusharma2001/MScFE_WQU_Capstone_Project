
"""
config.py
---------
Configuration file for MScFE Capstone Project: 
'Causal Factor Investing using Influence Diagrams & Dynamic Bayesian Networks'

Purpose:
--------
Centralizes imports, path setup, and directory management for consistent use 
across all notebooks and scripts (ETL, EDA, Modeling, and Decision Analysis).
"""

# Core Libraries
import io
import os
import sys
import math
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yaml
from tqdm import tqdm

# time series & econometrics libraries
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from statsmodels.tsa.stattools import acf, adfuller, kpss
from scipy.stats import spearmanr
from arch import arch_model
import ruptures as rpt

# data access libraries
import openassetpricing as oap

# configuration and settings
import warnings
warnings.filterwarnings("ignore")

# importing custom functions
from helper_functions import *
with open("../mapping.yaml", "r") as f:
    mapping = yaml.safe_load(f)


# Project Directory Setup
# NOTE: Adjust this path if running outside your local project folder.
# base_path = "/Users/sharmadipanshu/Developer/MScFE 2509 Capstone/WQU_Capstone_Project/MScFE_WQU_Capstone_Project"
base_path = "../"

# Define main directories
inputs_dir = f"{base_path}/inputs"
outputs_dir = f"{base_path}/outputs"

# Define input subdirectories
inputs_raw = f"{inputs_dir}/raw"
inputs_clean = f"{inputs_dir}/clean"
inputs_meta = f"{inputs_dir}/meta"

# Define output subdirectories
outputs_eda = f"{outputs_dir}/eda"
outputs_models = f"{outputs_dir}/models"
outputs_results = f"{outputs_dir}/results"

# Create directories if not exist
os.makedirs(inputs_raw, exist_ok=True)
os.makedirs(inputs_clean, exist_ok=True)
os.makedirs(inputs_meta, exist_ok=True)
os.makedirs(outputs_eda, exist_ok=True)
os.makedirs(outputs_models, exist_ok=True)
os.makedirs(outputs_results, exist_ok=True)


# plotting Style Configurations
sns.set(style="whitegrid", context="notebook", palette="muted")
plt.rcParams["figure.figsize"] = (10, 5)
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 10
plt.rcParams["legend.fontsize"] = 9

print("Configuration loaded successfully.")
