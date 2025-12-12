#!/usr/bin/env node
const WebSocket = require('ws');

const url = process.env.DYNAMODB_WEBSOCKET_API_URL;

if (!url) {
  console.error("Please set DYNAMODB_WEBSOCKET_API_URL in your environment");
  process.exit(1);
}

console.log(`Connecting to WebSocket API at ${url} ...`);

// No headers at all
const ws = new WebSocket(url);

ws.on('open', () => {
  console.log('✅ Connected!');
  ws.send(JSON.stringify({ action: 'list_tables' }));
});

ws.on('message', (data) => {
  console.log('📩 Received:', data.toString());
});

ws.on('error', (err) => {
  console.error('❌ WebSocket error:', err);
});

ws.on('close', (code, reason) => {
  console.log(`⚠️ Connection closed: ${code} ${reason}`);
});
