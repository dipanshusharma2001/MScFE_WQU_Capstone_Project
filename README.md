# MScFE Capstone Project: Causal Factor Investing using Influence Diagrams & Dynamic Bayesian Networks

## 🎓 Project Information

> **MScFE 690: Capstone Project**  
> **Influence Diagram as a Decision-Making Tool for Factor Investing**  
>
> **Student Group:** 11186  
> **Members:**  
> 1. **Vahid Nikoofard**  
> 2. **Dipanshu Sharma**  
> 3. **Rhesa Prabowo Budhidarmo**

---

### 🧭 Overview
This project explores the application of **Bayesian Networks (BN)**, **Dynamic Bayesian Networks (DBN)**, and **Influence Diagrams (ID)** 
in modeling causal relationships among financial factors and optimizing portfolio decisions under uncertainty.  
It forms part of the **MSc in Financial Engineering (MScFE)** Capstone Course at **WorldQuant University (WQU)**.

The goal is to design a **causal factor investing framework** that uses probabilistic graphical models to identify, 
quantify, and act upon relationships among key market factors. By leveraging Bayesian reasoning and decision theory, 
the project aims to build interpretable and dynamic investment decision tools.


---

### 📁 Repository Structure

```text
MScFE_WQU_Capstone_Project/
│
├── README.md                 ← concise overview + stage summaries
├── config.py                 ← project setup- loading the required libraries, mapping.yaml, helper_functions.py, creating the required directories
├── mapping.yaml              ← creating the mapping/parameters/hyperparameters/paths for different steps in the projects 
│
├── inputs/
│   ├── raw/                  ← raw input datasets
│   ├── clean/                ← cleaned input dataset
│   └── meta/
│       ├── etl_decisions.md  ← detailed record of all EDA/ETL steps
│       ├── sources.md        ← detailed record of all sources used to download the datasets
│
├── outputs/
│   ├── eda/                  ← eda summaries and results
│   ├── models/               ← Trained model files (.pkl, .bif, .json, etc.)
│   └── results/              ←  Post-modeling results and scenario analysis outputs
│
├── notebooks/                ← working python notebook files for various steps of the project (EDA, Modelling, Testing etc.)
|
├── helper_functions.py       ← custom functions 
└── requirements.txt          ←  packages and libraries required to run the project smoothly

```
---

### 📚 Detailed Documentation

For detailed ETL, EDA, and data-source documentation:

- **ETL & EDA Process:** [`inputs/meta/etl_decisions.md`](inputs/meta/etl_decisions.md)  
- **Data Sources & References:** [`inputs/meta/sources.md`](inputs/meta/sources.md)  
- **Project Metadata:** [`mapping.yaml`](mapping.yaml), [`config.py`](config.py)
