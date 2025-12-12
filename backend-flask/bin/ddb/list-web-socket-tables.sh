#!/usr/bin/env bash

# Load env variables
source $(dirname $0)/../.env

# Check Node.js
if ! command -v node &> /dev/null; then
  echo "Node.js is required but not installed"
  exit 1
fi

echo "Connecting to WebSocket API at $DYNAMODB_WEBSOCKET_API_URL ..."

# Run Node.js script
DYNAMODB_WEBSOCKET_API_URL=$DYNAMODB_WEBSOCKET_API_URL \
WS_JWT_TOKEN=$WS_JWT_TOKEN \
node $(dirname $0)/web-socket-test.js
