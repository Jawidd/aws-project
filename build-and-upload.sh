#!/bin/bash

# Build React app
cd frontend-react-js
npm install
npm run build

# Upload to S3 (replace with your actual bucket name after stack deployment)
aws s3 sync build/ s3://YOUR_DOMAIN_NAME --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"