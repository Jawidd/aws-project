FROM python:3.11-slim

WORKDIR /backend-flask

# Update system packages for security
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]

#docker build -t backend-flask .\backend-flask 
# docker run --rm -p 5000:5000 -it  -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask