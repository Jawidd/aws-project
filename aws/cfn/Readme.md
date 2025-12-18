# Cruddur CloudFormation Infrastructure

## Architecture Overview

```
Domain Layout:
- cruddur.jawid.me     → CloudFront → S3 (React Frontend)
- api.cruddur.jawid.me → ALB → ECS (Backend Flask)
```

## Stack Dependencies

1. **Bootstrap** (`CfnBootstrap`)
   - S3 bucket for CloudFormation artifacts
   - One-time setup per account/region

2. **Networking** (`CrdNet`)
   - VPC with public/private subnets
   - Internet Gateway, Route Tables
   - DynamoDB VPC Endpoint

3. **Cluster** (`CrdCluster`)
   - ECS Fargate Cluster
   - Application Load Balancer (api.cruddur.jawid.me)
   - Security Groups

4. **Database** (`CrdDb`)
   - RDS PostgreSQL instance
   - Database security group
   - DB subnet group

5. **DNS** (`CrdDns`)
   - Route53 hosted zone (jawid.me)
   - ACM certificate (*.jawid.me)
   - Alias record for api.cruddur.jawid.me → ALB

6. **Backend Service** (`CrdSrvBackendFlask`)
   - ECS service and task definition
   - IAM roles for execution and task
   - CloudWatch logs

7. **Frontend** (`CrdSrvFrontend`)
   - S3 bucket for static assets
   - CloudFront distribution
   - Route53 alias record for cruddur.jawid.me → CloudFront

## Deployment

Deploy all stacks in order:
```bash
./bin/cfn/deploy-all
```

Or deploy individually:
```bash
./bin/cfn/bootstrap
./bin/cfn/deploy-networking
./bin/cfn/deploy-cluster
./bin/cfn/deploy-database-rds
./bin/cfn/deploy-dns
./bin/cfn/deploy-backend-service
./bin/cfn/deploy-frontend
```

## Environment Variables

Production environment uses:
- Frontend: `https://cruddur.jawid.me`
- Backend API: `https://api.cruddur.jawid.me`