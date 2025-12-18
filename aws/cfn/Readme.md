# CloudFormation Deployment Guide

---

## Stack Overview/order

Stacks **must** be deployed in the following order. Each layer depends on exports from the previous layer.

1. **bootstrap**
   - S3 bucket for CloudFormation artifacts
   - One-time per account and region

2. **networking**
   - VPC
   - Public subnets (ECS / ALB)
   - Private subnets (RDS)
   - Route tables
   - DynamoDB VPC endpoint

3. **cluster**
   - ECS Fargate cluster
   - Application Load Balancer
   - Listeners and target groups
   - Shared service security group

4. **db**
   - Postgres RDS instance
   - Private subnet placement
   - Security group restricted to ECS services
   - After deployment: retrieve the new RDS endpoint

5. **service**
   - ECS task definition
   - ECS service
   - Service Connect
   - Logs, roles, and permissions

6. **dns**
   - Public hosted zone
   - ACM certificate (DNS validated)
   - ALB alias record (depends on cluster exports)

7. **frontend**
   - S3 static site buckets (root + www redirect)
   - CloudFront distribution with ACM cert from `dns`
   - Route53 aliases pointing at CloudFront

8. **cicd**
   - CodePipeline with GitHub source (CodeStar connection)
   - CodeBuild image bake using repo buildspec
   - ECS deploy action targeting the backend service

## Frontend/DNS Notes
- Deploy `dns` after `cluster` so ALB exports are available for the alias record.
- Deploy `frontend` after `dns`; pass the `dns` certificate ARN and hosted zone values into `aws/cfn/frontend/frontend.yaml`.
- Both S3 site buckets are retained on stack delete and allow public reads for CloudFront; CloudFront aliases use the ACM cert from `dns`.

## CI/CD Notes
- The `cicd` stack packages a nested CodeBuild project from `aws/cfn/cicd/codebuild-bake/codebuild-bake.yaml` using the artifact bucket created by `bootstrap`.
- Deploy with `bin/cfn/deploy-cicd`; you will be prompted to complete the GitHub CodeStar connection in AWS before the pipeline can pull source.
- The Build stage outputs `ImageDefinition` for the ECS deploy action; ensure the service stack is up so the deploy stage can import its exports.

---
