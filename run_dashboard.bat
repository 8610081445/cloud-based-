@echo off
title OmniSales Business Intelligence & Forecasting Platform
echo ======================================================================
echo    Starting OmniSales BI & Forecasting Platform (Streamlit)
echo ======================================================================
echo.
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment .venv not found.
    pause
    exit /b 1
)

echo Opening web browser to http://localhost:8501 ...
start http://localhost:8501

echo Launching Streamlit server on port 8501...
.venv\Scripts\python.exe -m streamlit run src\dashboard\app.py --server.port 8501
pause
