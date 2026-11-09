# German Electricity Market Intelligence

### Interactive Energy Market Analytics | Germany (DE-LU) | 2018–2026

**Python · Pandas · NumPy · Plotly · Statsmodels · Streamlit**

An interactive portfolio demonstrating electricity-market analysis,
energy-transition indicators, data visualization, and econometric modelling.

**Developed by:** Chetan Masram

**Live dashboard:** https://german-electricity-market-intelligence-b6drwomgtytftpkg5o7jv.streamlit.app/

> **SYNTHETIC DATA DEMONSTRATION**
>
> All market observations displayed in this public dashboard are
> artificially generated. They do not represent actual German
> electricity-market conditions. Numerical results must not be
> interpreted as empirical findings about Germany.

---

## 1. Project Overview

This project demonstrates an interactive analytical framework for
exploring electricity-market indicators.

The dashboard focuses on three areas:

- **Wholesale electricity markets:** Illustrative electricity,
  natural gas, and carbon-price relationships.
- **Energy transition:** Wind, solar, and conventional generation.
- **Econometric analysis:** Statistical relationships estimated
  using multivariate regression.

The application is a technical portfolio demonstration, not an
official source of German energy-market statistics.

## 2. Dashboard Features

### Market Overview

- Monthly electricity-price visualizations
- Electricity and natural gas price comparisons
- Interactive date-range selection
- Summary market indicators

### Energy Transition

- Wind and solar generation trends
- Gas, lignite, and hard-coal generation
- Wind-and-solar generation relative to grid load

The wind-and-solar-to-load indicator is not Germany's official
renewable-electricity share.

### Econometrics

- Correlation heatmap
- Multivariate ordinary least squares regression
- HAC-robust standard errors
- Coefficient estimates and p-values
- Confidence intervals
- Date-range-sensitive estimation

Regression results describe associations within synthetic data.
They are not causal estimates.

### Methodology

The dashboard documents analytical assumptions, data limitations,
and interpretation safeguards.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming | Python |
| Data processing | Pandas, NumPy |
| Visualization | Plotly |
| Econometrics | Statsmodels |
| Web application | Streamlit |
| Development | JupyterLab |

## 4. Run Locally

Clone or download the release repository.

Install dependencies:

    python -m pip install -r requirements.txt

Launch the application from the repository root:

    python -m streamlit run PUBLIC_DEMO/dashboard/demo_app.py

The dashboard reads:

    PUBLIC_DEMO/german_energy_market_eex_2018_2026.csv

## 5. Data and Research Integrity

### Public demonstration

The public application uses 96 synthetic monthly observations
covering November 2018 through October 2026.

The dataset is intended exclusively to demonstrate analytical
workflows, visualization, and software implementation.

### Separate empirical research

A separate private research workflow examines historical German
electricity-market data and related energy indicators.

The public synthetic dashboard does not reproduce the empirical
estimates or underlying datasets from that research.

Real-data outputs will be shared only after relevant publication
and data-use permissions have been verified.

## 6. Analytical Limitations

- Synthetic observations do not establish historical facts.
- Correlation does not imply causation.
- Regression estimates depend on model specification.
- Time-series dependence and nonstationarity require attention.
- Short sample periods may produce unstable estimates.
- Illustrative indicators are not official statistics.

## 7. Portfolio Relevance

This project demonstrates practical skills relevant to energy-market
analyst, commercial analyst, and market-intelligence positions:

- Time-series data preparation and validation
- Interactive dashboard development
- Electricity-market indicator analysis
- Econometric modelling
- Statistical interpretation
- Research transparency and reproducibility

---

**Author:** Chetan Masram

**Project:** German Electricity Market Intelligence
