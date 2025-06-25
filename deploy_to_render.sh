#!/bin/bash
# Script to deploy the Multi-Format Video and Audio Downloader to Render.com

echo "===== Multi-Format Video and Audio Downloader Deployment ====="
echo "This script will help you deploy the application to Render.com"
echo ""

# Check if render-cli is installed
if ! command -v render &> /dev/null; then
    echo "render-cli not found. Installing..."
    if ! command -v npm &> /dev/null; then
        echo "Error: npm is required to install render-cli."
        echo "Please install Node.js and npm first, then run this script again."
        exit 1
    fi
    npm install -g @render/cli
fi

# Check if logged in to Render
render whoami || {
    echo "Please log in to Render:"
    render login
}

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is required for deployment."
    echo "Please install git and try again."
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree &> /dev/null; then
    echo "Error: Not in a git repository."
    echo "Please run this script from within the repository directory."
    exit 1
fi

# Check if there are uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "Warning: You have uncommitted changes."
    echo "It's recommended to commit all changes before deploying."
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Deployment cancelled."
        exit 1
    fi
fi

# Deploy to Render
echo "Deploying to Render.com..."
render deploy --yaml render.yaml

echo ""
echo "===== Deployment Initiated ====="
echo "Check the Render dashboard for progress: https://dashboard.render.com"
echo "Your application will be available at: https://multi-format-downloader.onrender.com"
echo "Note: It may take a few minutes for the deployment to complete."
echo ""
echo "After deployment, you can access your application at the URL shown in the Render dashboard."
echo "===== Deployment Complete ====="