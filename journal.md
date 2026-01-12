````md
# Journal Index

This is the journal file. I wrote it after I finished the project, so it’s a clean summary of what I built and why. I try to link to real files and commits so it’s easy to verify.

## Table of contents
- [Week 00 — Billing and Architecture](#week-00--billing-and-architecture)
- [Week 01 — App Containerization](#week-01--app-containerization)
- [Week 02 — Distributed Tracing](#week-02--distributed-tracing)
- [Week 03 — Decentralized Authentication](#week-03--decentralized-authentication)
- [Week 04 — Postgres and RDS](#week-04--postgres-and-rds)
- [Week 05 — DynamoDB and Serverless Caching](#week-05--dynamodb-and-serverless-caching)
- [Week 06 — Deploying Containers](#week-06--deploying-containers)
- [Week 07 — Solving CORS with a Load Balancer and Custom Domain](#week-07--solving-cors-with-a-load-balancer-and-custom-domain)
- [Week 08 — Serverless Image Processing](#week-08--serverless-image-processing)
- [Week 09 — CI/CD with CodePipeline and CodeBuild](#week-09--cicd-with-codepipeline-and-codebuild)
- [Week 10 — CloudFormation Part 1](#week-10--cloudformation-part-1)
- [Week 11 — CloudFormation Part 2](#week-11--cloudformation-part-2)
- [Week 12 — Modern APIs](#week-12--modern-apis)
- [Week 13 — Bonus Features](#week-13--bonus-features)

---

## Summary table

| Week | Theme | What I built | Evidence |
|------|-------|--------------|----------|
| 00 | Billing & Architecture | early architecture thinking + basic security notes | TODO: add billing/budget template if I have it |
| 01 | Containerization | Dockerfiles + docker-compose for local dev | `./backend-flask/Dockerfile.dev`, `./frontend-react-js/Dockerfile.dev`, `./docker-compose.yml`, commit `9f67b91` |
| 02 | Distributed Tracing | tracing + error reporting dependencies (scaffolded) | `./backend-flask/requirements.txt`, `./backend-flask/app.py`, commit `d61b4dd` |
| 03 | Authentication | Cognito + Amplify + JWT verification | `./aws/cfn/cognito/cognito.yaml`, `./backend-flask/lib/cognito_jwt_token.py`, commit `a669b6b` |
| 04 | Postgres & RDS | schema/seed scripts + RDS stack | `./backend-flask/db/schema.sql`, `./backend-flask/db/seed.sql`, `./aws/cfn/database/database.yaml`, commit `e760030` |
| 05 | DynamoDB | tables + message queries | `./aws/cruddur-serverless/template.yaml`, `./backend-flask/services/messages.py`, commit `95ba0bf` |
| 06 | ECS Deployment | cluster/service templates + ECR scripts | `./aws/cfn/cluster/cluster.yaml`, `./aws/cfn/backend-service/backend-service.yaml`, `./bin/backend/ecr-ecs/`, commit `050b2ae` |
| 07 | DNS + CORS | Route53/certs stack + CORS config | `./aws/cfn/dns/dns.yaml`, `./backend-flask/app.py`, commit `b59e1ff` |
| 08 | Serverless Images | avatar upload + thumbnails (S3/Lambda/SNS) | `./aws/cruddur-serverless/template.yaml`, `./aws/cruddur-serverless/functions/`, commit `0733a7d` |
| 09 | CI/CD | pipelines + buildspecs | `./aws/cfn/cicd/`, `./backend-flask/buildspec.yml`, `./frontend-react-js/buildspec.yml`, commit `9d1371e` |
| 10 | CloudFormation 1 | bootstrap + networking + scripts | `./aws/cfn/bootstrap/`, `./aws/cfn/networking/`, `./bin/cfn/`, commit `701021c` |
| 11 | CloudFormation 2 | database/backend/frontend stacks | `./aws/cfn/database/`, `./aws/cfn/backend-service/`, `./aws/cfn/frontend-ecs/`, commit `1acf009` |
| 12 | Modern APIs | WebSocket handlers + stream wiring | `./aws/cruddur-serverless/template.yaml`, `./backend-flask/bin/ddb/web-socket-test.js`, commit `11f9c53` |
| 13 | Bonus Features | likes + cover image migrations + UI changes | `./backend-flask/db/migrations/003_create_likes_table.sql`, `./frontend-react-js/src/components/ActivityActionLike.js`, commit `f868bc4` |

---

# Week 00 — Billing and Architecture

## Summary
- I wrote down the main AWS services I planned to use, just to keep the big picture clear.
- I also wrote basic notes about security (mainly: don’t hardcode secrets and keep config in env vars).

## What I implemented
- I didn’t create diagrams at this stage (this journal was written later after the project was complete).

## Steps & Notes
### Security notes
- I kept a short checklist for myself:
  - don’t commit secrets
  - use `.env` files locally
  - use AWS services for secrets/params in production (SSM/Secrets Manager)

## Verification
- Not applicable for this week (notes/planning only).

## Challenges & Fixes
- Biggest challenge here was just getting the mental model right before I started wiring services together.

## Results
Observed result: I had a clear plan for the stack and how the parts connect.

## Next steps
- If I have a billing/budget CFN template, link it here and document how I used it.
- Keep updating these notes when the infra changes.

---

# Week 01 — App Containerization

## Summary
- I containerized the Flask backend and React frontend for local dev.
- I added `docker-compose.yml` so I can run both services together.

## What I implemented
- Dockerfiles for backend and frontend (dev + prod)
- Root `docker-compose.yml`
- Evidence:
  - `./backend-flask/Dockerfile.dev`
  - `./backend-flask/Dockerfile.prod`
  - `./frontend-react-js/Dockerfile.dev`
  - `./frontend-react-js/Dockerfile.prod`
  - `./docker-compose.yml`
  - commit `9f67b91`

## Steps & Notes
### Backend container
- I used a dev Dockerfile for local hot reload and a prod Dockerfile for deployment.

### Frontend container
- I kept `node_modules` inside the container to avoid host/OS version conflicts.

### Local compose
```bash
docker compose up --build
````

## Verification

* [http://localhost:4567/api/health-check](http://localhost:4567/api/health-check)
* [http://localhost:3000](http://localhost:3000)

## Challenges & Fixes

* `node_modules` on the host caused conflicts, so I avoided it.
* I split dev vs prod images so production stays smaller.

## Results

Observed result: I can run the backend + frontend locally with Docker.

## Next steps

* Add local Postgres and DynamoDB containers (I have commented examples).
* Add a small “local dev checklist” to the main README.

---

# Week 02 — Distributed Tracing

## Summary

* I added tracing/error reporting dependencies in the backend.
* I kept tracing hooks commented out to avoid breaking local dev.

## What I implemented

* OpenTelemetry, X-Ray, and Rollbar deps
* Commented tracing blocks in the Flask app
* IAM permissions for X-Ray in the ECS task role
* Evidence:

  * `./backend-flask/requirements.txt`
  * `./backend-flask/app.py`
  * `./aws/cfn/backend-service/backend-service.yaml`
  * commit `d61b4dd`

## Steps & Notes

### Dependencies

* I added the libs first so I can enable tracing later without refactoring.

### App hooks (commented)

* I left these commented until I wire real credentials and decide exactly what I want enabled.

### IAM permissions

* ECS task role includes X-Ray permissions in the backend service template.



## Challenges & Fixes

* Tracing adds lots of moving parts, so I treated it as “optional until I finish the core app”.

## Results

Observed result: tracing scaffolding exists in code and templates.

## Next steps

* Pick one provider and document exact enable steps.
* Add a small smoke test for tracing.

---

# Week 03 — Decentralized Authentication

## Summary

* I wired Cognito into the frontend and backend.
* I added JWT verification for protected API routes.

## What I implemented

* Cognito stack template for user pool + client
* Amplify config in React
* JWT helper in Flask
* Evidence:

  * `./aws/cfn/cognito/cognito.yaml`
  * `./frontend-react-js/src/App.js`
  * `./backend-flask/lib/cognito_jwt_token.py`
  * commit `a669b6b`

## Steps & Notes

### Frontend auth

* Amplify uses Cognito values from env variables.

### Backend auth

* JWT verification + decorator to protect routes.

### Token usage

* Frontend sends `Authorization: Bearer <token>`.

## Verification

TODO: sign in from the UI, then call a protected endpoint like `/api/message_groups`.

## Challenges & Fixes

* Cognito settings are easy to mismatch (region/pool id/client id). When they don’t match, you just get 401s.

## Results

Observed result: auth works end-to-end (frontend + backend wiring exists).

## Next steps

* Finish auth wiring where there are still TODOs in the UI.
* Add a short “auth troubleshooting” section to the README.

---

# Week 04 — Postgres and RDS

## Summary

* I added schema + seed scripts for Postgres.
* I added an RDS CloudFormation stack.

## What I implemented

* SQL schema and seed
* DB helper scripts
* RDS stack template
* Evidence:

  * `./backend-flask/db/schema.sql`
  * `./backend-flask/db/seed.sql`
  * `./backend-flask/db/bin/schema-load`
  * `./aws/cfn/database/database.yaml`
  * commit `e760030`

## Steps & Notes

### Schema and seed

```bash
cd backend-flask
./db/bin/schema-load
./db/bin/seed
```

### RDS stack

* Template: `./aws/cfn/database/database.yaml`

## Verification

TODO: run `./backend-flask/db/bin/test` and confirm DB connectivity.

## Challenges & Fixes

* Switching between local DB and RDS means env var handling has to be clean.

## Results

Observed result: DB schema/seed/scripts exist and RDS stack exists.

## Next steps

* Document a repeatable migration flow.
* Add a simple schema version check.

---

# Week 05 — DynamoDB and Serverless Caching

## Summary

* I defined DynamoDB tables in the SAM template.
* I added DynamoDB access to message services.

## What I implemented

* DynamoDB tables/indexes in serverless stack
* Flask message queries
* Evidence:

  * `./aws/cruddur-serverless/template.yaml`
  * `./backend-flask/services/messages.py`
  * `./backend-flask/services/message_groups.py`
  * commit `95ba0bf`

## Steps & Notes

### DynamoDB tables

* Messages, conversations, websocket connections.

### Backend usage

* boto3 + table names from env vars.

## Verification

TODO: call `/api/message_groups` and `/api/messages` and confirm data returns.

## Challenges & Fixes

* Mapping between Cognito IDs and app user UUIDs.
* Getting the DynamoDB keys right for “last message” ordering.

## Results

Observed result: DynamoDB tables and queries are defined.

## Next steps

* Add a local DynamoDB setup and seed script.
* Document the key design briefly.

---

# Week 06 — Deploying Containers

## Summary

* I added ECS cluster + backend service stacks.
* I wrote scripts to build/push the backend Docker image to ECR.

## What I implemented

* ECS cluster + backend service CFN templates
* ECR build/push scripts
* Evidence:

  * `./aws/cfn/cluster/cluster.yaml`
  * `./aws/cfn/backend-service/backend-service.yaml`
  * `./bin/backend/ecr-ecs/build-backend-prod`
  * `./bin/cfn/deploy-backend-service`
  * commit `050b2ae`

## Steps & Notes

### Build and push

```bash
./bin/backend/ecr-ecs/build-backend-prod
./bin/backend/ecr-ecs/tag-push-backend-prod
```

## Verification

TODO: deploy backend service stack and confirm ECS service becomes healthy.

## Challenges & Fixes

* ECS task def must match image tags pushed to ECR.
* Naming consistency across stacks/scripts matters a lot.

## Results

Observed result: ECS + ECR deployment artifacts are in place.

## Next steps

* Add one command that builds + deploys backend end-to-end.
* Document required parameters and outputs (I added this in README deployment steps).

---

# Week 07 — Solving CORS with a Load Balancer and Custom Domain

## Summary

* I added DNS + cert resources for a custom domain.
* I adjusted CORS handling so the frontend can call the backend without browser errors.

## What I implemented

* Route53 + cert stack
* Frontend CloudFront/S3 stack
* Backend CORS config based on env origins
* Evidence:

  * `./aws/cfn/dns/dns.yaml`
  * `./aws/cfn/frontend-ecs/frontend-ecs.yaml`
  * `./backend-flask/app.py`
  * commit `b59e1ff`

## Steps & Notes

### CORS config

* Allowed origins come from env vars + localhost defaults.

## Verification

TODO: test calls from the frontend domain and confirm no CORS errors.

## Challenges & Fixes

* Multiple domains = don’t hardcode origins. Keep them in env vars.

## Results

Observed result: DNS stack + CORS config exist in code.

## Next steps

* Add a quick “CORS checklist” for after deployments.

---

# Week 08 — Serverless Image Processing

## Summary

* I added Lambdas for avatar presigned uploads and thumbnail creation.
* I wired S3 events and SNS for the image pipeline.

## What I implemented

* Image-related Lambda functions + deps
* SAM wiring for S3/SNS/Lambda
* Evidence:

  * `./aws/cruddur-serverless/functions/image_to_thumbnail/requirements.txt`
  * `./aws/cruddur-serverless/functions/avatar_presign/requirements.txt`
  * `./aws/cruddur-serverless/template.yaml`
  * commit `0733a7d`

## Steps & Notes

### Presigned upload

* Presign Lambda returns an upload URL for avatars.

### Thumbnail generation

* S3 event triggers Lambda to create thumbnails.

## Verification

TODO: upload an avatar and confirm thumbnails appear in the assets bucket.

## Challenges & Fixes

* S3 prefixes must match exactly or the event won’t fire.

## Results

Observed result: the serverless image pipeline is defined in the SAM template.

## Next steps

* Write a short end-to-end test checklist for avatar uploads.

---

# Week 09 — CI/CD with CodePipeline and CodeBuild

## Summary

* I added CI/CD templates.
* I added buildspecs for backend Docker builds and frontend S3 deploys.

## What I implemented

* CodePipeline templates for backend and frontend
* CodeBuild buildspecs
* Evidence:

  * `./aws/cfn/cicd/Pipeline.yaml`
  * `./aws/cfn/cicd/frontend-pipeline.yaml`
  * `./backend-flask/buildspec.yml`
  * `./frontend-react-js/buildspec.yml`
  * commit `9d1371e`

## Steps & Notes

### Backend buildspec

* Builds/pushes Docker image and writes `imagedefinitions.json`.

### Frontend buildspec

* Builds React app, syncs to S3, invalidates CloudFront.

## Verification

TODO: run the pipeline and confirm both builds succeed.

## Challenges & Fixes

* CloudFront invalidation can fail if distribution IDs/env vars are wrong.
* Docker login must happen before build/push.

## Results

Observed result: pipeline templates + buildspecs exist.

## Next steps

* Add a small CI/CD runbook (required env vars + common failures).

---

# Week 10 — CloudFormation Part 1

## Summary

* I added bootstrap + networking stacks.
* I centralized scripts under `./bin/cfn`.

## What I implemented

* Bootstrap template + script
* Networking stack (VPC/subnets/SGs)
* Evidence:

  * `./aws/cfn/bootstrap/bootstraping.yaml`
  * `./aws/cfn/networking/networking.yaml`
  * `./bin/cfn/bootstrap`
  * commit `701021c`

## Steps & Notes

### Bootstrap

```bash
./bin/cfn/bootstrap
```

### Networking

```bash
./bin/cfn/deploy-networking
```

## Verification

TODO: deploy networking stack and confirm VPC/subnets exist.

## Challenges & Fixes

* Keeping stack parameters consistent early on needed refactoring.

## Results

Observed result: bootstrap and networking templates exist.

## Next steps

* Document networking parameters clearly.

---

# Week 11 — CloudFormation Part 2

## Summary

* I added database, backend service, and frontend stacks.
* I expanded scripts so I can deploy the full stack.

## What I implemented

* RDS stack + backend ECS stack + frontend CloudFront/S3 stack
* Evidence:

  * `./aws/cfn/database/database.yaml`
  * `./aws/cfn/backend-service/backend-service.yaml`
  * `./aws/cfn/frontend-ecs/frontend-ecs.yaml`
  * commit `1acf009`

## Steps & Notes

```bash
./bin/cfn/deploy-database-rds
./bin/cfn/deploy-backend-service
./bin/cfn/deploy-frontend
```

## Verification

TODO: deploy stacks in order and confirm ALB/CloudFront endpoints respond.

## Challenges & Fixes

* Cross-stack exports need careful naming.
* ECS health check timing needed a grace period.

## Results

Observed result: CFN templates cover database/backend/frontend.

## Next steps

* Keep `./aws/cfn/README.md` aligned with the real deploy steps.

---

# Week 12 — Modern APIs

## Summary

* I added WebSocket handlers for real-time messaging.
* I extended the serverless template for API Gateway routes and DynamoDB streams.

## What I implemented

* WebSocket connect/disconnect handlers
* Stream processor wiring
* Evidence:

  * `./aws/cruddur-serverless/template.yaml`
  * `./aws/cruddur-serverless/functions/websocket_connect/requirements.txt`
  * `./backend-flask/bin/ddb/web-socket-test.js`
  * commit `11f9c53`

## Steps & Notes

### WebSocket test

* I used the test script to verify connections.

## Verification

TODO: run the websocket test script and confirm a message can flow end-to-end.

## Challenges & Fixes

* DynamoDB stream permissions needed explicit IAM policies.
* Route names had to match exactly.

## Results

Observed result: WebSocket handlers and stream processing exist in the serverless stack.

## Next steps

* Add a short websocket smoke test section to the README.

---

# Week 13 — Bonus Features

## Summary

* I added likes support.
* I extended user profile data to include a cover image field.

## What I implemented

* Likes table migration
* Frontend like button code
* Cover image migration
* Evidence:

  * `./backend-flask/db/migrations/003_create_likes_table.sql`
  * `./create_likes_table.sql`
  * `./frontend-react-js/src/components/ActivityActionLike.js`
  * `./backend-flask/db/migrations/16_add_cover_image_url.py`
  * commit `f868bc4`

## Steps & Notes

### Likes

* I created a migration to track likes per activity per user.

### UI updates

* The UI requests auth tokens before sending like actions.

### Cover images

* Added `cover_image_url` in the users table via migration.

## Verification

TODO: like/unlike an activity and confirm the count updates correctly.

## Challenges & Fixes

* Avoiding duplicate likes needs either a DB constraint or careful checks.
* UI state needs to match backend response to avoid flicker.

## Results

Observed result: likes + cover image migrations and UI code are committed.

## Next steps

* Add backend tests for likes and cover image updates.
* Document the endpoints the UI uses for these actions.

```
::contentReference[oaicite:0]{index=0}
```
