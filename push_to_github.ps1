# OmniSales: Push to GitHub Script (PowerShell)
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "  OmniSales: Cloud-Based Sales Forecasting & BI Platform" -ForegroundColor Cyan
Write-Host "  GitHub & Render Automated Git Deployment" -ForegroundColor Cyan
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Target Repository: https://github.com/8610081445/cloud-based-.git" -ForegroundColor Yellow
Write-Host ""

if (-not (Test-Path ".git")) {
    Write-Host "[1/5] Initializing Git repository..." -ForegroundColor Green
    git init
} else {
    Write-Host "[1/5] Git repository already initialized." -ForegroundColor Green
}

Write-Host "[2/5] Setting branch to main..." -ForegroundColor Green
git branch -M main

Write-Host "[3/5] Configuring remote origin..." -ForegroundColor Green
git remote remove origin 2>$null
git remote add origin https://github.com/8610081445/cloud-based-.git

Write-Host "[4/5] Staging files and creating commit..." -ForegroundColor Green
git add .
git commit -m "feat: complete cloud-based sales forecasting and BI platform with Render deployment config"

Write-Host "[5/5] Pushing to GitHub (origin main)..." -ForegroundColor Green
git push -u origin main --force

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=======================================================================" -ForegroundColor Green
    Write-Host "  SUCCESS! Project pushed to https://github.com/8610081445/cloud-based-" -ForegroundColor Green
    Write-Host "=======================================================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[!] Push failed or requires authentication. Try: git push -u origin main" -ForegroundColor Red
}

