# Dataset Sources and References

| Dataset / Source | Description | Access Method | Period | Notes |
|------------------|--------------|----------------|---------|--------|
| **Open Asset Pricing (OAP) Factors** | Monthly factor returns for multiple global markets, including cross-sectional signals for asset pricing research. [https://www.openassetpricing.com/]| `openassetpricing` Python package (open source GitHub: [https://github.com/mk0417/open-asset-pricing-download](https://github.com/mk0417/open-asset-pricing-download)) | July 1963 – September 2023 | Used to extract 6 main factor portfolios: BM, IdioVol3F, Investment, Mom12m, OperProf, and Size. |
| **MSCI Emerging Market Factor Index** *(optional backup)* | Proprietary factor indices for Emerging Markets. | Excel file: `Inputs/raw/MSCI_Emerging_Markets_Factor_Index.xlsx` | 2000–2025 | Used only for cross-reference validation. |
| **Python Libraries** | Open-source scientific and econometrics packages. | Installed via `requirements.txt` | – | See `inputs/meta/requirements.txt` for versions and dependencies. |

> **Note:**  
> All datasets are publicly available and accessed using open-source tools.  
> The data is used strictly for academic and research purposes as part of the MScFE Capstone Project.

