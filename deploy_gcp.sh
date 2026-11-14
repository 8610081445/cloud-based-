#!/usr/bin/env bash
# ==============================================================================
# Script: deploy_gcp.sh
# Purpose: Build and deploy the OmniSales BI Dashboard to Google Cloud Run
# ==============================================================================

set -euo pipefail

# Configuration parameters
PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || echo '')}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="omnisales-bi-dashboard"
IMAGE_TAG="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest"

if [ -z "$PROJECT_ID" ]; then
    echo "ERROR: GCP_PROJECT_ID is not set. Run 'gcloud config set project <PROJECT_ID>' first."
    exit 1
fi

echo "=========================================================="
echo "Deploying ${SERVICE_NAME} to Google Cloud Run"
echo "Project: ${PROJECT_ID}"
echo "Region:  ${REGION}"
echo "Image:   ${IMAGE_TAG}"
echo "=========================================================="

# 1. Enable required Google Cloud APIs
echo "[1/4] Enabling required APIs (Cloud Run, Container Registry, Cloud Build)..."
gcloud services enable run.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com --project="${PROJECT_ID}"

# 2. Build the container using Cloud Build
echo "[2/4] Submitting build to Google Cloud Build..."
gcloud builds submit --tag "${IMAGE_TAG}" --project="${PROJECT_ID}" .

# 3. Deploy container image to Cloud Run
echo "[3/4] Deploying service to Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
    --image "${IMAGE_TAG}" \
    --platform managed \
    --region "${REGION}" \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 2 \
    --min-instances 0 \
    --max-instances 5 \
    --project="${PROJECT_ID}"

# 4. Retrieve and display public service URL
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --platform managed --region "${REGION}" --project="${PROJECT_ID}" --format='value(status.url)')

echo "=========================================================="
echo "Deployment successful!"
echo "Live Dashboard URL: ${SERVICE_URL}"
echo "=========================================================="
