# Cruddur  Deployment Guide

### Step 1: Bootstrap (One-time setup)

./bin/cfn/bootstrap  Creates S3 bucket for CloudFormation artifacts.

### Step 2: Request SSL Certificates
manually request certificates for alb(eu-west-2) and cloudfront(us-east-1)
VAlidate certfs via DNS records in Route53
Update certificate ARNs in deployment scripts

### Step 3: Deploy Database stack
need to assign pass 
export DB_PASSWORD="your-secure-password"

# Deploy all stacks in order
./bin/cfn/deploy-all
```

Or deploy individually:
```bash
./bin/cfn/bootstrap                 # S3 artifacts bucket
./bin/cfn/deploy-networking         # VPC, subnets, security groups
./bin/cfn/deploy-cluster           # ECS cluster, ALB
./bin/cfn/deploy-database-rds      # RDS PostgreSQL
./bin/cfn/deploy-dns               # Route53, certificates
./bin/cfn/deploy-backend-service   # ECS backend service
./bin/cfn/deploy-frontend          # CloudFront, S3
```

### Step 4: Deploy Serverless Components

sam build
sam deploy --guided


### Step 5: Database Setup

cd backend-flask
Create database schema: ./bin/db/schema-load
Seed initial data: ./bin/db/seed

### Step 6: Build and Deploy Application Code



Build and push BAckend Docker image to ECR
./bin/backend/ecr-ecs/build-backend-prod
./bin/backend/ecr-ecs/tag-push-backend-prod



Update Frontend Environment Variables
Update these values in `/bin/frontend/build-and-upload-frontend`:
- `REACT_APP_BACKEND_URL`
- `REACT_APP_WEBSOCKET_URL` 
- `REACT_APP_USER_POOL_ID`
- `REACT_APP_USER_POOL_CLIENT_ID`
- `REACT_APP_AVATAR_API_URL`
Build and upload Frontend to S3
./bin/frontend/build-and-upload-frontend





### 2. Cognito Configuration
- Create Cognito User Pool and User Pool Client
- Update IDs in frontend build script and serverless templates

### 3. DynamoDB Tables
Serverless deployment creates:
- `cruddur-messages` table
- `cruddur-conversations` table




## Stack Dependencies

1. **Bootstrap** → Creates S3 artifacts bucket
2. **Networking** → VPC, subnets, security groups
3. **Cluster** → ECS cluster, ALB (depends on Networking)
4. **Database** → RDS PostgreSQL (depends on Networking, Cluster)
5. **DNS** → Route53, certificates (depends on Cluster for ALB)
6. **Backend Service** → ECS service (depends on Networking, Cluster)
7. **Frontend** → CloudFront, S3 (depends on DNS for certificate)






