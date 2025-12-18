# CloudFormation Deployment Guide

This repository migrates an existing, manually-created AWS setup
to CloudFormation using layered stacks.

The goal is to deploy infrastructure **in parallel** with the
existing application, validate it, then cut over safely.

---

## Stack Overview

Deployment is split into the following stacks:

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

5. **service**
   - ECS task definition
   - ECS service
   - Service Connect
   - Logs, roles, and permissions

---

## Deployment Order

Stacks **must** be deployed in the following order:

1. bootstrap
2. networking
3. cluster
4. db
5. service

Each stack depends on exports from the previous layer.

---

## First-Time Deployment Notes

This project assumes an application is already running
from console-created resources.

For the first deployment:

- Do **not** delete existing infrastructure
- Deploy stacks in parallel
- Validate functionality before switching traffic

---

## Database Migration

The DB stack creates a **new RDS instance**.

After deployment:
1. Retrieve the new RDS endpoint
2. Update the application connection string
3. Restart ECS tasks if required

The old database should remain untouched
until the new stack is fully validated.

---

## Traffic Cutover

Traffic is not automatically switched.

To go live:
- Update Route53 to point to the new ALB
- Monitor logs, health checks, and error rates
- Keep old infrastructure running during validation

---

## Cleanup (Later)

Only after confirmed stability:
- Remove console-created resources
- Remove hardcoded AWS credentials
- Treat CloudFormation as the source of truth
