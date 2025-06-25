# Cloud Deployment Guide

This guide provides instructions for deploying the Multi-Format Video and Audio Downloader to various cloud platforms.

## Table of Contents
- [Render](#render)
- [Heroku](#heroku)
- [Railway](#railway)
- [DigitalOcean App Platform](#digitalocean-app-platform)
- [AWS Elastic Beanstalk](#aws-elastic-beanstalk)
- [Google Cloud Run](#google-cloud-run)

## Render

[Render](https://render.com/) offers a free tier for web services.

1. Create a Render account at https://render.com/
2. Click on "New" and select "Web Service"
3. Connect your GitHub repository or upload your code directly
4. Configure your service:
   - Name: multi-format-downloader
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn web_downloader:app`
5. Add the following environment variables:
   - `PORT`: 10000
   - `SECRET_KEY`: (generate a secure random string)
6. Click "Create Web Service"

Your application will be deployed and accessible at the URL provided by Render.

## Heroku

[Heroku](https://www.heroku.com/) offers a free tier for small applications.

1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login to Heroku: `heroku login`
3. Create a new Heroku app: `heroku create your-app-name`
4. Push your code to Heroku: `git push heroku main`
5. Set environment variables:
   ```
   heroku config:set SECRET_KEY=your-secret-key
   ```
6. Open your app: `heroku open`

## Railway

[Railway](https://railway.app/) offers a free tier for small applications.

1. Create a Railway account at https://railway.app/
2. Create a new project and select "Deploy from GitHub repo"
3. Connect your GitHub repository
4. Add the following environment variables:
   - `PORT`: 10000
   - `SECRET_KEY`: (generate a secure random string)
5. Deploy your application

Your application will be deployed and accessible at the URL provided by Railway.

## DigitalOcean App Platform

[DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform/) offers a paid service for hosting applications.

1. Create a DigitalOcean account
2. Go to the App Platform section
3. Click "Create App" and select your GitHub repository
4. Configure your app:
   - Type: Web Service
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn web_downloader:app`
5. Add environment variables:
   - `PORT`: 8080
   - `SECRET_KEY`: (generate a secure random string)
6. Click "Launch App"

## AWS Elastic Beanstalk

[AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) is a service for deploying and scaling web applications.

1. Install the [AWS CLI](https://aws.amazon.com/cli/) and [EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html)
2. Initialize your EB application: `eb init -p python-3.9 multi-format-downloader`
3. Create an environment: `eb create multi-format-downloader-env`
4. Deploy your application: `eb deploy`
5. Set environment variables:
   ```
   eb setenv SECRET_KEY=your-secret-key
   ```
6. Open your application: `eb open`

## Google Cloud Run

[Google Cloud Run](https://cloud.google.com/run) is a fully managed platform for containerized applications.

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Login to Google Cloud: `gcloud auth login`
3. Set your project: `gcloud config set project your-project-id`
4. Build and push your Docker image:
   ```
   gcloud builds submit --tag gcr.io/your-project-id/multi-format-downloader
   ```
5. Deploy to Cloud Run:
   ```
   gcloud run deploy multi-format-downloader \
     --image gcr.io/your-project-id/multi-format-downloader \
     --platform managed \
     --allow-unauthenticated \
     --set-env-vars="SECRET_KEY=your-secret-key"
   ```
6. Your application will be deployed and accessible at the URL provided by Google Cloud Run.

## Important Notes

1. **Storage**: Most cloud platforms provide ephemeral storage, which means files will be deleted when the application restarts. Consider using cloud storage services like AWS S3, Google Cloud Storage, or DigitalOcean Spaces for persistent storage.

2. **Resource Limits**: Free tiers often have CPU and memory limitations. Video processing can be resource-intensive, so you may need to upgrade to a paid plan for better performance.

3. **Security**: Always use a strong, unique `SECRET_KEY` in production environments.

4. **Scaling**: For high-traffic applications, consider implementing a queue system for processing downloads asynchronously.

5. **Costs**: Be aware of the pricing models for each platform, especially for bandwidth and storage usage, which can increase significantly with video downloads.