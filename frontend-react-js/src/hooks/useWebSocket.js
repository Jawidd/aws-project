import { useEffect, useRef, useState } from 'react';

export default function useWebSocket(url) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState(null);
  const ws = useRef(null);

  useEffect(() => {
    if (!url) return;

    ws.current = new WebSocket(url);
    
    ws.current.onopen = () => {
      setIsConnected(true);
      // console.log('WebSocket connected');
    };
    
    ws.current.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setLastMessage(message);
    };
    
    ws.current.onclose = () => {
      setIsConnected(false);
      // console.log('WebSocket disconnected');
    };
    
    ws.current.onerror = (error) => {
    };

    return () => {
      ws.current?.close();
    };
  }, [url]);

  return { isConnected, lastMessage };
}