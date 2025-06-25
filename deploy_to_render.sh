#!/bin/bash
# Script to deploy the Multi-Format Video and Audio Downloader to Render.com

# Check if render-cli is installed
if ! command -v render &> /dev/null; then
    echo "render-cli not found. Installing..."
    npm install -g @render/cli
fi

# Check if logged in to Render
render whoami || {
    echo "Please log in to Render:"
    render login
}

# Deploy to Render
echo "Deploying to Render.com..."
render deploy --yaml render.yaml

echo "Deployment initiated. Check the Render dashboard for progress."
echo "Your application will be available at: https://multi-format-downloader.onrender.com"
echo "Note: It may take a few minutes for the deployment to complete."