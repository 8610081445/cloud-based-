@echo off
setlocal enabledelayedexpansion

echo =======================================================================
echo   OmniSales: Cloud-Based Sales Forecasting & BI Platform
echo   GitHub & Render Automated Git Deployment
echo =======================================================================
echo.
echo Target Repository: https://github.com/8610081445/cloud-based-.git
echo.

:: 1. Initialize git if not present
if not exist .git (
    echo [1/5] Initializing Git repository...
    git init
) else (
    echo [1/5] Git repository already initialized.
)

:: 2. Set default branch to main
echo [2/5] Setting branch to main...
git branch -M main

:: 3. Configure remote origin
echo [3/5] Configuring remote origin...
git remote remove origin 2>nul
git remote add origin https://github.com/8610081445/cloud-based-.git

:: 4. Stage and commit changes
echo [4/5] Staging files and creating commit...
git add .
git commit -m "feat: complete cloud-based sales forecasting and BI platform with Render deployment config"

:: 5. Push to GitHub
echo [5/5] Pushing to GitHub (origin main)...
echo If prompted, please sign in via your browser or enter your Personal Access Token.
echo.
git push -u origin main --force

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =======================================================================
    echo   SUCCESS! All files pushed to GitHub successfully:
    echo   https://github.com/8610081445/cloud-based-
    echo =======================================================================
) else (
    echo.
    echo [!] Push encountered an issue. Please verify your GitHub credentials or run:
    echo     git push -u origin main
)

echo.
pause

