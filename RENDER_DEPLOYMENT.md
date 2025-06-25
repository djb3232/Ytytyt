# Deploying to Render.com

This guide will help you deploy the Multi-Format Video and Audio Downloader to Render.com, which offers a free tier for web services.

## Prerequisites

1. A [Render.com](https://render.com/) account
2. Your code pushed to a GitHub repository

## Deployment Steps

1. **Sign up for Render.com**
   - Go to [Render.com](https://render.com/) and sign up for an account
   - You can sign up using your GitHub account for easier integration

2. **Create a New Web Service**
   - From your Render dashboard, click on "New" and select "Web Service"
   - Connect your GitHub repository
   - If you don't want to use GitHub, you can also deploy directly from your local machine using the Render CLI

3. **Configure Your Web Service**
   - Name: Choose a name for your service (e.g., "multi-format-downloader")
   - Environment: Select "Python 3"
   - Region: Choose the region closest to your users
   - Branch: Select the branch you want to deploy (e.g., "main" or "feature/multi-format-downloader")
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn web_downloader:app`

4. **Environment Variables**
   - Add the following environment variables:
     - `PORT`: 10000
     - `SECRET_KEY`: (generate a secure random string)

5. **Advanced Settings**
   - Under "Advanced" settings, you can configure:
     - Auto-Deploy: Enable this to automatically deploy when you push to your repository
     - Health Check Path: Set to `/` to ensure your application is running correctly

6. **Create Web Service**
   - Click "Create Web Service" to start the deployment process
   - Render will build and deploy your application

7. **Access Your Application**
   - Once deployment is complete, you can access your application at the URL provided by Render
   - The URL will be in the format: `https://your-service-name.onrender.com`

## Important Notes

1. **Free Tier Limitations**
   - The free tier on Render has some limitations:
     - Your service will spin down after 15 minutes of inactivity
     - Limited bandwidth and compute resources
     - No persistent storage (files will be deleted when the service restarts)

2. **Persistent Storage**
   - For persistent storage, consider using cloud storage services like AWS S3 or Google Cloud Storage
   - You can modify the application to store downloaded files in cloud storage instead of local storage

3. **Custom Domains**
   - If you want to use a custom domain, you can configure it in the Render dashboard
   - This feature is available on paid plans

4. **Scaling**
   - If you need more resources, you can upgrade to a paid plan
   - Paid plans offer more CPU, memory, and bandwidth

## Troubleshooting

1. **Deployment Failures**
   - Check the build logs in the Render dashboard
   - Ensure all dependencies are correctly listed in requirements.txt
   - Verify that your start command is correct

2. **Application Errors**
   - Check the application logs in the Render dashboard
   - Enable debug mode temporarily to get more detailed error messages

3. **Performance Issues**
   - Consider optimizing your application for better performance
   - Use background tasks for long-running operations
   - Implement caching where appropriate

## Updating Your Application

To update your application:

1. Push changes to your GitHub repository
2. If auto-deploy is enabled, Render will automatically deploy the changes
3. If auto-deploy is disabled, manually deploy from the Render dashboard

## Conclusion

Your Multi-Format Video and Audio Downloader is now deployed on Render.com and accessible to users worldwide. Remember to monitor your application's performance and usage to ensure it meets your needs.