# 🚀 CRUDDUR
## ✅ To-Do List

### 🏗️ Current Structure: 
- FrontEnd: React(port=3000) hosted on ecs, can be accessed via ALB (http://crudder-alb-76675061.eu-west-2.elb.amazonaws.com:3000)

- Backend:  Flask(port=5000)hosted on ecs, can be accessed via ALB (http://crudder-alb-76675061.eu-west-2.elb.amazonaws.com:5000/api/health-check)

- DB: AWS RDS for users and activitis/cruds 
    -  Setup Db using setup(create rds db, create schemas for db, populate db with users and !!!activities/cruds!!!) shell script in backend-flask/bin/db/setup 
    - Test using backend-flask/bin/db/test 

- DB: AWS DynamoDB for messages table and conversations table
    - setup using  shell script in backend-flask/bin/ddb

- ALB: target groups will listen to port 5000 and 3000 of alb ip, send them to containers, send back the answers
 means ALBsg ports of 3000 and 5000 need to be open
 means containersg ports of 3000 and 5000 need to be open to ALB only


### 🏗️ Phase 6: Migrating the dev env to aws
- [x] create a test shell script for testing connection to psql 
- [x] add health-check for flask app (create a route in app.py, create a file for calling healthcheck route from app.py) docker exec -it aws-project-backend-flask-1 python3 /backend-flask/bin/flask/health-check
- [X]  Create ECRs for base image of python. 
    - Retrieve an authentication token and authenticate your Docker client to your registry. ( aws ecr  get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 225442939245.dkr.ecr.eu-west-2.amazonaws.com)
    - pull from dockerhub (docker pull python:3.11-slim-buster)
    - Tag image (docker tag python:3.11-slim-buster \
        225442939245.dkr.ecr.eu-west-2.amazonaws.com/cruddur-python:3.11-slim-buster)
    - push image (docker push 225442939245.dkr.ecr.eu-west-2.amazonaws.com/cruddur-python:3.11-slim-buster )
    - make flask app to use repo from aws(change docker file  in backend to use ecr python docker uri)

- [X]  Create ECR for FLASK.
    - Retrieve an authentication token and authenticate  Docker client to  registry. 
    - build image 
    - Tag image 
    - push image 
    
- [X] Create ECS cluster with name and namespace Cruddur 
- [X] Create ECS service not task for ECR Flask
    -attaching AWS-managed ECS execution policy and AmazonSSMReadOnlyAccess ( aws iam attach-role-policy \ --role-name crudder-ecs-service-execution-role \ --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy ),(arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess)

- [X] save parameters in system manager to be used by ecs (AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,CONNECTION_URL for postgres,ROLLBAR_ACCESS_TOKEN,OTEL_EXPORTER_OTLP_HEADERS) cat ssmparams.txt | while IFS='=' read -r name value; do
  aws ssm put-parameter \
    --name "$name" \
    --value "$value" \
    --type SecureString \
    --overwrite
done

- [X] Create ecs execution role (which is required by ecs, ecs-execution-trust.json) and Create the ECS Task Role (permissions for backend application, ecs-task-trust.json)
    1. create the role CruddurECSTaskExecutionRole
    2. Attach required AWS-managed policies and SSM read policy
    3. create ecs-task-trust.json
    4. create ecs task policy.json


- [X] Create task definition
    1. create task definition json file for backend
    2. register task defination (aws ecs register-task-definition --cli-input-json file://backend-flask-task-definition.json)
    


- [X] create service in ecs (sg is important, it needs to self refernce on ports 443 for ssm and 5000 for self check)( using created task definition,fargate,new sg) aws ecs create-service --cli-input-json file://service-backend-flask.json 
    
- [X] connect to service backend flask (bin/ecs/connect-to-service) aws ecs execute-command --cluster crudder --task 0a9a4ebcd8b14415885e9b62eb0b8ca7 --container backend-flask --interactive --command '/bin/sh'

- [X] Test if ecs backend  public ip is working (open port 5000 in sg)

- [X] check connection between ECS-backend and rds

- [X] create load balancer with target groups for front and back. anyd check if target groups are healthy for backend
<!--
- [X] commit to github -->

- [X] create a docker file for frontend production.(reason: we use only builded react app in container)

- [] create a ecr for frontend, build,tag and push react app to ecr,   docker build \
--build-arg REACT_APP_BACKEND_URL="http://crudder-ALB-76675061.eu-west-2.elb.amazonaws.com:5000" \
--build-arg REACT_APP_AWS_PROJECT_REGION="eu-west-2" \
--build-arg REACT_APP_AWS_COGNITO_REGION="eu-west-2" \
--build-arg REACT_APP_AWS_USER_POOLS_ID="eu-west-2_Jwi9THX3b" \
--build-arg REACT_APP_CLIENT_ID="1ls5p1vu83m5ahseab36ufk6vm" \
-t frontend-react-js \
-f Dockerfile.prod \
.

- [X] create task definition, service for frontend, tested frontend , tested rds(activities), failed test dynamodb(messages)
aws ecs register-task-definition --cli-input-json file://aws/task-definitions/frontend-reactjs-task-definition.json
aws ecs create-service --cli-input-json file://aws/json/service-frontend-reactjs.json


## 🧭 Project Overview
CRUDDUR is an app similar to twittr.
- Crudds
---



### 🏗️ Setup & Infrastructure
- [x] Initialize Git repository

### 💻 Backend Development
- [x] Implement user authentication (JWT)

### 🎨 Frontend Development
- [x] Build login and registration pages

### 📚 Documentation
- [ ] Write setup guide in `docs/SETUP.md`
- [ ] Add API reference (`/docs/api.md`)
- [ ] Include screenshots in README
- [ ] Write contributor guidelines

---

## 🎯 Milestones

### **v0.1 — MVP**
- [x] Core authentication & dashboard


### **v1.0 — Stable Release**
- [ ] Full CI/CD pipeline


---

## 🧠 Future Enhancements
- [ ] Mobile app (React Native)

---

## 🧩 How to Contribute
1. Fork this repository  
2. Create your feature branch: `git checkout -b feature/amazing-feature`  
3. Commit your changes: `git commit -m 'feat: add amazing feature'`  
4. Push to the branch: `git push origin feature/amazing-feature`  
5. Open a Pull Request 🚀

---

## 👥 Contributors
| Name | Role | GitHub |
|------|------|--------|
| Jawid  | Lead Developer | [@alexmorgn](https://github.com/alexmorgn) |



---

## 🗓️ Project Status
> Currently in **Active Development** — contributions welcome!
