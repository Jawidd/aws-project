# FROM python:3.11-slim

From 225442939245.dkr.ecr.eu-west-2.amazonaws.com/cruddur-python:3.11-slim-buster


# Update system packages for security
# RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .


EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]

#docker build -t backend-flask ./backend-flask  
#docker run --rm -p 5000:5000 --env-file .env backend-flask
