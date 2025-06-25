# Updating Your Render Deployment

This guide provides alternative methods for updating your Multi-Format Video and Audio Downloader deployment on Render.com.

## What's New in Version 1.2.0

- **Proxy support enhancements**:
  - Added random proxy selection for YouTube downloads
  - Automatically selects working proxies from a public list
  - Helps bypass geo-restrictions on YouTube videos
  - Available in all interfaces (CLI, GUI, web)

## Previous Updates (Version 1.1.0)

- **OAuth token authentication support** added to all interfaces (CLI, GUI, web)
- Support for Bearer, Basic, Digest, and OAuth token types
- Automatically adds Authorization header to requests
- Works with sites requiring OAuth authentication instead of cookies

## Update Methods

### Method 1: Using the Render Dashboard (Manual)

1. Log in to your [Render Dashboard](https://dashboard.render.com)
2. Navigate to your Multi-Format Downloader service
3. Click on "Manual Deploy" and select "Deploy latest commit"
4. Wait for the deployment to complete (this may take a few minutes)

### Method 2: Using the One-Click Deploy Button

If you're setting up a new instance or want to create a separate deployment:

1. Click the "Deploy to Render" button in the README.md:
   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/djb3232/Ytytyt)
2. Follow the on-screen instructions to complete the deployment

### Method 3: Using GitHub Integration with Auto-Deploy

If you've set up GitHub integration with auto-deploy:

1. The deployment will automatically update when new commits are pushed to the repository
2. Check the Render Dashboard for deployment status and logs

### Method 4: Using the Render CLI (Advanced)

If you want to use the Render CLI:

1. Install Node.js and npm if not already installed
2. Install the Render CLI:
   ```
   npm install -g @render/cli
   ```
3. Log in to your Render account:
   ```
   render login
   ```
4. Deploy using the render.yaml configuration:
   ```
   render deploy --yaml render.yaml
   ```

## Verifying the Update

After updating, verify that the new proxy functionality is working:

1. Access your application at your Render URL (e.g., https://multi-format-downloader.onrender.com)
2. Check that the proxy fields are visible in the Advanced Options section:
   - Proxy URL field
   - "Use Random Proxy for YouTube" checkbox
3. Test downloading a YouTube video with the random proxy option enabled
4. Verify that the download log shows a proxy being used

You can also verify the previous OAuth token functionality:

1. Check that the OAuth token fields are visible in the web interface
2. Test downloading content that requires OAuth authentication

## Troubleshooting

If you encounter issues with the update:

1. Check the deployment logs in the Render Dashboard
2. Ensure all dependencies are correctly installed
3. Verify that the environment variables are correctly set
4. If needed, restart the service from the Render Dashboard

For additional help, refer to the [Render Documentation](https://render.com/docs) or open an issue in the GitHub repository.