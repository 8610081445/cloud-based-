# Deploying OmniSales BI Dashboard to Render

This repository is pre-configured for **1-click / automated deployment on Render** using the included [`render.yaml`](./render.yaml).

---

## Method 1: Deploy with Blueprint (Automatic / Recommended)

1. **Push your code to GitHub** using the provided script:
   ```cmd
   .\push_to_github.bat
   ```
2. Go to [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** in the top right corner and choose **Blueprint**.
4. Connect your GitHub repository:
   ```
   https://github.com/8610081445/cloud-based-
   ```
5. Render will automatically read [`render.yaml`](./render.yaml) and configure:
   - **Name**: `cloud-based-sales-bi`
   - **Runtime**: `Python 3.11.9`
   - **Plan**: `Free`
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `streamlit run src/dashboard/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
6. Click **Apply**.
7. Render will build the environment and provide your live public URL (e.g. `https://cloud-based-sales-bi.onrender.com`).

---

## Method 2: Manual Web Service Setup

If you prefer setting it up manually on Render:

1. Go to [Render Dashboard](https://dashboard.render.com/) -> **New +** -> **Web Service**.
2. Select **Build and deploy from a Git repository** -> Connect `8610081445/cloud-based-`.
3. Configure the following fields:
   - **Name**: `omnisales-bi`
   - **Region**: Choose the closest region (e.g., Singapore, Frankfurt, Oregon)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     streamlit run src/dashboard/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
     ```
   - **Instance Type**: `Free`
4. Expand **Advanced** -> **Add Environment Variable**:
   - `PYTHON_VERSION` = `3.11.9`
   - `STREAMLIT_SERVER_HEADLESS` = `true`
   - `STREAMLIT_BROWSER_GATHER_USAGE_STATS` = `false`
5. Click **Create Web Service**.

