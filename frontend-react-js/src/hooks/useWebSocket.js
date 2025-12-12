import { useEffect, useRef, useState } from 'react';

export default function useWebSocket(url) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState(null);
  const ws = useRef(null);

  useEffect(() => {
    if (!url) return;
    let socket;
    let retryTimeout;

    const log = (...args) => {
      if (process.env.NODE_ENV !== 'production') {
        console.log(...args);
      }
    };

    const connect = () => {
      socket = new WebSocket(url);

      socket.onopen = () => {
        setIsConnected(true);
        log('WebSocket connected');
      };

      socket.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          setLastMessage(message);
        } catch (err) {
          log('Invalid WebSocket message:', event.data);
        }
      };

      socket.onclose = () => {
        setIsConnected(false);
        log('WebSocket disconnected. Reconnecting in 3s...');
        retryTimeout = setTimeout(connect, 3000); // auto-reconnect
      };

      socket.onerror = (err) => {
        log('WebSocket error:', err);
        socket.close(); // ensure onclose is called
      };

      ws.current = socket;
    };

    // Optional small delay to avoid race conditions on page load
    const timeout = setTimeout(connect, 150);

    return () => {
      clearTimeout(timeout);
      clearTimeout(retryTimeout);
      socket?.close();
    };
  }, [url]);

  // Safe send function
  const sendMessage = (data) => {
    if (ws.current && isConnected) {
      ws.current.send(JSON.stringify(data));
    } else if (process.env.NODE_ENV !== 'production') {
      console.warn('WebSocket not connected. Message not sent:', data);
    }
  };

  return { isConnected, lastMessage, sendMessage };
}
