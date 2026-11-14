"""Main CLI application entrypoint for the OmniSales platform.

Usage:
    python main.py                 # Runs full pipeline: data ingestion -> analytics -> ML forecasting
    python main.py generate        # Synthesizes datasets into data/raw/ and data/processed/
    python main.py analyze         # Computes and displays statistical KPIs and price elasticities
    python main.py forecast        # Trains forecasters, prints leaderboard, and projects future demand
    python main.py run-dashboard   # Launches the Streamlit Business Intelligence web dashboard
"""

from __future__ import annotations

import os
import sys
import argparse
import subprocess
from pathlib import Path
import pandas as pd

# Add workspace root to sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.data.generator import generate_sales_data
from src.data.processor import clean_transactions, aggregate_daily_demand, build_time_series_features
from src.analytics.statistics import compute_growth_metrics, get_category_performance
from src.analytics.correlation import compute_correlation_matrix, calculate_price_elasticity, calculate_marketing_roi
from src.analytics.anomalies import detect_anomalies_zscore
from src.models.evaluator import (
    test_stationarity_adf,
    benchmark_models,
    generate_future_forecast,
)


def run_generate_data(start_date: str = "2023-01-01", end_date: str = "2026-10-01"):
    """Synthesize transactions and save cleaned datasets to disk."""
    print("=" * 70)
    print("1. DATA GENERATION & PIPELINE PROCESSING")
    print("=" * 70)

    raw_dir = BASE_DIR / "data" / "raw"
    processed_dir = BASE_DIR / "data" / "processed"
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    raw_path = raw_dir / "sales_transactions.csv"
    daily_path = processed_dir / "daily_sales_demand.csv"
    feat_path = processed_dir / "daily_demand_features.csv"

    print(f"Generating realistic omnichannel transactions from {start_date} to {end_date}...")
    raw_df = generate_sales_data(start_date=start_date, end_date=end_date, seed=42, output_path=str(raw_path))
    print(f"[OK] Raw Transactions Generated: {len(raw_df):,} records -> {raw_path}")

    print("Cleaning transactions and aggregating daily time-series...")
    clean_df = clean_transactions(raw_df)
    daily_df = aggregate_daily_demand(clean_df)
    daily_df.to_csv(daily_path, index=False)
    print(f"[OK] Daily Time-Series Saved: {len(daily_df)} days -> {daily_path}")

    print("Building zero-lookahead lag and rolling features...")
    feat_df = build_time_series_features(daily_df, target_col="gross_revenue")
    feat_df.to_csv(feat_path, index=False)
    print(f"[OK] Engineered Features Saved: {feat_df.shape[1]} columns -> {feat_path}")

    return clean_df, daily_df, feat_df


def run_analytics(clean_df: pd.DataFrame = None, daily_df: pd.DataFrame = None):
    """Compute and print statistical growth rates, correlations, and anomalies."""
    print("\n" + "=" * 70)
    print("2. STATISTICAL & COMMERCIAL ANALYTICS")
    print("=" * 70)

    if clean_df is None or daily_df is None:
        raw_path = BASE_DIR / "data" / "raw" / "sales_transactions.csv"
        daily_path = BASE_DIR / "data" / "processed" / "daily_sales_demand.csv"
        if not raw_path.exists() or not daily_path.exists():
            clean_df, daily_df, _ = run_generate_data()
        else:
            clean_df = clean_transactions(pd.read_csv(raw_path))
            daily_df = pd.read_csv(daily_path)

    # Growth & KPIs
    kpis = compute_growth_metrics(daily_df)
    print("\n--- Executive Key Performance Indicators ---")
    print(f"Total Gross Revenue:   ${kpis['total_revenue']:,.2f}")
    print(f"Total Net Profit:      ${kpis['total_profit']:,.2f} ({kpis['profit_margin_pct']:.1f}% Margin)")
    print(f"Total Completed Orders:{kpis['total_orders']:,} orders ({kpis['total_units']:,} units)")
    print(f"Average Order Value:   ${kpis['avg_order_value']:.2f}")
    print(f"Latest MoM Growth:     {kpis['latest_mom_growth_pct']:+.2f}%")
    print(f"Latest YoY Growth:     {kpis['latest_yoy_growth_pct']:+.2f}%")
    print(f"3-Year CAGR:           {kpis['cagr_pct']:.2f}%")

    # Price Elasticity
    print("\n--- Log-Log Price Elasticity of Demand (PED) by Category ---")
    ped_df = calculate_price_elasticity(clean_df)
    print(ped_df.to_string(index=False))

    # Marketing ROI
    m_roi = calculate_marketing_roi(daily_df)
    print("\n--- Marketing Efficiency Attribution ---")
    print(f"Total Marketing Spend: ${m_roi['total_marketing_spend']:,.2f}")
    print(f"Marketing Efficiency Ratio (MER): {m_roi['marketing_efficiency_ratio']:.2f}x")
    print(f"Marketing-Revenue Pearson Correlation: r = {m_roi['marketing_revenue_correlation']:.3f} (p = {m_roi['correlation_p_value']})")

    # Anomalies
    anom_df = detect_anomalies_zscore(daily_df, threshold=2.5)
    spike_count = len(anom_df[anom_df["anomaly_type"] == "Demand Spike (Positive)"])
    drop_count = len(anom_df[anom_df["anomaly_type"] == "Demand Drop (Negative)"])
    print(f"\n--- Anomaly Detection (Rolling Z-Score > 2.5 sigma) ---")
    print(f"Total Statistical Anomalies Detected: {spike_count + drop_count} ({spike_count} positive spikes, {drop_count} negative drops)")


def run_forecast(feat_df: pd.DataFrame = None, daily_df: pd.DataFrame = None):
    """Benchmark forecasting models and generate out-of-sample forward projections."""
    print("\n" + "=" * 70)
    print("3. MACHINE LEARNING & DEMAND FORECASTING (ml-best-practices)")
    print("=" * 70)

    if feat_df is None or daily_df is None:
        feat_path = BASE_DIR / "data" / "processed" / "daily_demand_features.csv"
        daily_path = BASE_DIR / "data" / "processed" / "daily_sales_demand.csv"
        if not feat_path.exists() or not daily_path.exists():
            _, daily_df, feat_df = run_generate_data()
        else:
            feat_df = pd.read_csv(feat_path)
            daily_df = pd.read_csv(daily_path)

    # Stationarity test
    print("\n--- Stationarity Test: Augmented Dickey-Fuller (ADF) ---")
    adf_res = test_stationarity_adf(daily_df["gross_revenue"])
    print(f"ADF Statistic: {adf_res['test_statistic']}")
    print(f"p-value:       {adf_res['p_value']}")
    print(f"Decision:      {adf_res['interpretation']}")

    # Benchmark models
    print("\n--- Chronological Validation Leaderboard ---")
    benchmark_df, _, lgbm_model = benchmark_models(feat_df, target_col="gross_revenue")
    print(benchmark_df.to_string(index=False))

    # Feature importances
    print("\n--- LightGBM Top 5 Predictive Features ---")
    imp_df = lgbm_model.get_feature_importances().head(5)
    print(imp_df.to_string(index=False))

    # Forward projection
    horizon = 45
    print(f"\n--- Generating {horizon}-Day Forward Demand Projection with 95% Confidence Bounds ---")
    forecast_df = generate_future_forecast(daily_df, lgbm_model, horizon_days=horizon)
    print(forecast_df.head(10).to_string(index=False))
    print(f"... and {len(forecast_df) - 10} more future days projected.")

    return forecast_df


def run_dashboard():
    """Launch the Streamlit web dashboard."""
    app_path = BASE_DIR / "src" / "dashboard" / "app.py"
    print(f"Launching OmniSales Business Intelligence Dashboard from {app_path}...")
    print("Local URL: http://localhost:8501")
    import webbrowser
    try:
        webbrowser.open("http://localhost:8501")
    except Exception:
        pass
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path),
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
        ],
        check=True,
    )


def main():
    parser = argparse.ArgumentParser(
        description="OmniSales: Cloud-Based Sales Forecasting & Business Intelligence CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="run-dashboard",
        choices=["run-dashboard", "all", "generate", "analyze", "forecast"],
        help="Command to execute (default: 'run-dashboard')",
    )

    args = parser.parse_args()

    if args.command == "generate":
        run_generate_data()
    elif args.command == "analyze":
        run_analytics()
    elif args.command == "forecast":
        run_forecast()
    elif args.command == "run-dashboard":
        run_dashboard()
    elif args.command == "all":
        clean_df, daily_df, feat_df = run_generate_data()
        run_analytics(clean_df, daily_df)
        run_forecast(feat_df, daily_df)
        print("\n" + "=" * 70)
        print("PIPELINE EXECUTION COMPLETE! Launching Business Intelligence Dashboard...")
        print("=" * 70)
        run_dashboard()


if __name__ == "__main__":
    main()
