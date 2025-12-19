FROM postgres:15-alpine

RUN apk add --no-cache bash

WORKDIR /workspace

# Include DB helper scripts so they are available inside the exec session
COPY backend-flask/bin/db /opt/db-scripts

ENV PATH="/opt/db-scripts:${PATH}"

# Keep the task running for ECS Exec sessions
CMD ["sh", "-c", "while true; do sleep 3600; done"]
