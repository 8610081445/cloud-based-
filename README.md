# OmniSales: Cloud-Based Sales Forecasting & Business Intelligence Platform

[![CI/CD Pipeline](https://github.com/example/omnisales-bi/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/example/omnisales-bi/actions/workflows/ci-cd.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)](https://www.docker.com/)
[![Google Cloud Run](https://img.shields.io/badge/Google%20Cloud-Run%20Deployed-4285F4.svg)](https://cloud.google.com/run)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade, cloud-native Sales Forecasting and Business Intelligence platform. It analyzes omnichannel sales transactions, computes compound growth rates and commercial correlations, estimates price elasticity of demand, benchmarks statistical and machine learning forecasting models, and serves a modern, interactive SaaS Business Intelligence dashboard deployed via a containerized CI/CD pipeline.

---

## 1. System Architecture

```
OmniSales Architecture
├── Data Layer
│   ├── Synthetic Omnichannel Transaction Generator (Multi-category, seasonal, promo-aware)
│   ├── ETL & Schema Validation Pipeline
│   └── Time-Series Feature Engineering (Lag 1-30, Rolling 7-30d, Cyclical sin/cos encodings)
├── Analytics & Statistical Engine
│   ├── Growth Analytics (MoM %, YoY %, CAGR %, Rolling Moving Averages)
│   ├── Commercial Correlation Matrix (Pearson & Spearman)
│   ├── Log-Log Price Elasticity of Demand (PED) by Product Category
│   └── Rolling Z-Score & IQR Anomaly Detection Engine
├── Predictive Machine Learning Core (ml-best-practices compliant)
│   ├── Stationarity Testing: Augmented Dickey-Fuller (ADF)
│   ├── Strict Chronological Split (Train 70% / Val 15% / Test 15%)
│   ├── Model Benchmarking: Seasonal Naive, Moving Average, Holt-Winters, LightGBM
│   ├── Demand Planning Metrics: WAPE, MAPE, RMSE, MAE
│   └── 45-Day Forward Projections with 95% Confidence Bounds
├── Live SaaS BI Dashboard (Streamlit + Plotly + Zinc Theme)
│   ├── Executive KPI Cards with Dynamic Trend Badges
│   ├── Interactive Visual Analytics & Donut/Bar Distributions
│   ├── Real-Time What-If Pricing & Marketing Scenario Simulator
│   └── Data Health & Filtered Transaction Ledger
└── Cloud & DevOps Infrastructure
    ├── Multi-Stage Non-Root Dockerfile
    ├── Docker Compose Local Orchestration
    ├── GitHub Actions Automated CI/CD Workflow (.github/workflows/ci-cd.yml)
    └── Google Cloud Run / Cloud Build Automated Deployment (deploy_gcp.sh)
```

---

## 2. Statistical & Econometric Formulations

### 1. Compound Annual Growth Rate (CAGR)
$$\text{CAGR} = \left(\frac{\text{End Value}}{\text{Start Value}}\right)^{\frac{1}{N}} - 1$$

### 2. Price Elasticity of Demand (PED)
Estimated via log-log Ordinary Least Squares (OLS) regression:
$$\ln(Q_i) = \alpha + \beta \ln(P_i) + \epsilon_i$$
where $\beta$ is the price elasticity coefficient:
* $|\beta| > 1.2$: **Elastic** (demand shifts significantly with price adjustments).
* $|\beta| < 0.8$: **Inelastic** (demand is resistant to price changes).

### 3. Weighted Absolute Percentage Error (WAPE)
The supply-chain gold standard for demand forecasting:
$$\text{WAPE} = \frac{\sum_{t=1}^n |y_t - \hat{y}_t|}{\sum_{t=1}^n y_t} \times 100\%$$

### 4. Stationarity Testing (Augmented Dickey-Fuller)
$$\Delta y_t = \alpha + \beta t + \gamma y_{t-1} + \sum_{i=1}^p \delta_i \Delta y_{t-i} + \epsilon_t$$
Tests $H_0: \gamma = 0$ (unit root / non-stationary) vs $H_1: \gamma < 0$ (stationary).

---

## 3. Directory Structure

```
.
├── .github/
│   └── workflows/
│       └── ci-cd.yml             # GitHub Actions CI/CD Pipeline
├── config/
│   └── settings.yaml             # Centralized application & forecasting parameters
├── notebooks/
│   └── sales_forecasting_bi.ipynb # Complete narrative notebook (EDA, ADF test, ML benchmark)
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── generator.py          # Omnichannel transaction generator
│   │   └── processor.py          # Data cleaning, aggregation & feature engineering
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── statistics.py         # MoM, YoY, CAGR & KPI calculators
│   │   ├── correlation.py        # Correlation matrices, PED & marketing ROI
│   │   └── anomalies.py          # Rolling Z-score & IQR anomaly detectors
│   ├── models/
│   │   ├── __init__.py
│   │   ├── baseline.py           # Seasonal Naive & Moving Average baselines
│   │   ├── time_series.py        # Holt-Winters Triple Exponential Smoothing
│   │   ├── ml_forecasting.py     # LightGBM Regressor with prediction intervals
│   │   └── evaluator.py          # ADF test, chronological splitter, WAPE/RMSE evaluator
│   └── dashboard/
│       ├── __init__.py
│       ├── app.py                # Main Streamlit Business Intelligence application
│       ├── styles.py             # SaaS Zinc/Dark-Mode CSS design system
│       ├── components.py         # Styled KPI cards, HTML tables & chart containers
│       └── simulator.py          # Interactive What-If demand & profit simulator
├── tests/
│   ├── __init__.py
│   ├── test_pipeline.py          # Data pipeline unit tests
│   ├── test_analytics.py         # Statistical & correlation unit tests
│   └── test_models.py            # Forecasters & metric evaluators tests
├── Dockerfile                    # Multi-stage production container
├── docker-compose.yml            # Local container orchestration
├── cloudbuild.yaml               # Google Cloud Build deployment specification
├── deploy_gcp.sh                 # Cloud Run automated deployment script
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development & test dependencies
└── README.md                     # Documentation
```

---

## 4. Quickstart: Local Setup

### Prerequisites
* Python 3.11+
* Git
* (Optional) Docker & Docker Compose

### Step 1: Clone and Set Up Virtual Environment
```bash
# Navigate to the workspace
cd "Cloud-Based Sales Forecasting and Business Intelligence"

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements-dev.txt
```

### Step 2: Run Automated Tests
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

### Step 3: Launch the Business Intelligence Dashboard
```bash
streamlit run src/dashboard/app.py
```
Open your browser to 

---

## 5. Docker Containerization

### Build and Run with Docker
```bash
# Build the container image
docker build -t omnisales-bi:latest .

# Run container on port 8080
docker run -d -p 8080:8080 --name omnisales-app omnisales-bi:latest
```
Access the application at `http://localhost:8080`.

### Run with Docker Compose
```bash
docker compose up -d
```

---

## 6. Cloud Deployment & CI/CD Pipeline

### Render Cloud Deployment (1-Click Blueprint)
The repository includes [`render.yaml`](./render.yaml) and [`runtime.txt`](./runtime.txt) for immediate deployment on Render:
1. Push repository to GitHub: `https://github.com/8610081445/cloud-based-.git`
2. In [Render](https://dashboard.render.com), click **New +** -> **Blueprint**.
3. Select your GitHub repository; Render will automatically detect `render.yaml` and deploy the dashboard.
4. Detailed instructions are available in [DEPLOYMENT_RENDER.md](./DEPLOYMENT_RENDER.md).

### Automated CI/CD (GitHub Actions)
The workflow in `.github/workflows/ci-cd.yml` executes on every push to `main`:
1. **Linting & Code Quality**: Executes `flake8` and `black` syntax validation.
2. **Automated Testing**: Executes `pytest` across all units and outputs coverage reports.
3. **Container Packaging**: Builds the Docker image and tests the healthcheck endpoint.
4. **Cloud Run Deployment**: Automatically pushes the container to Google Container Registry (GCR) and deploys to **Google Cloud Run** using GitHub repository secrets (`GCP_PROJECT_ID`, `GCP_SA_KEY`).

### Manual Google Cloud Run Deployment
Using the included deployment script:
```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud config set project YOUR_GCP_PROJECT_ID

# Deploy to Cloud Run
chmod +x deploy_gcp.sh
./deploy_gcp.sh
```

---

## 7. Business Intelligence Dashboard Features

| Tab | Key Visual Analytics & Decision Levers |
| :--- | :--- |
| **Executive Overview** | Real-time Gross Revenue, MoM Growth %, AOV, CAGR %, 30-Day Moving Average, Revenue by Category Donut. |
| **Statistical & Correlations** | Pearson Correlation Heatmap, Category Price Elasticity Table, Marketing Efficiency Ratio (MER), Rolling Z-Score Anomaly Detection. |
| **Demand Forecasting** | ADF Stationarity Test result, Model Benchmark Leaderboard (WAPE %, RMSE, MAE), 45-Day Out-of-Sample Demand Projection with 95% Confidence Bounds, LightGBM Feature Importance. |
| **What-If Scenario Simulator** | Dynamic sliders for Unit Price Adjustment ($-30\%$ to $+30\%$), Marketing Spend, and Promotional Discounts with immediate revenue/profit variance projections. |
| **Data Explorer & Health** | Ingested transaction ledger, pagination, data quality hygiene indicators, and filtered CSV export. |

---

## 8. License
Distributed under the MIT License. See `LICENSE` for details.
