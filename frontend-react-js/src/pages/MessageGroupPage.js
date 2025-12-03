import './MessageGroupPage.css';
import React from "react";
import { useParams, useNavigate } from 'react-router-dom';
import useAuth from '../hooks/useAuth';
import useWebSocket from '../hooks/useWebSocket';

import DesktopNavigation from '../components/DesktopNavigation';
import MessagesFeed from '../components/MessageFeed';
import MessagesForm from '../components/MessageForm';
import MessageGroupFeed from '../components/MessageGroupFeed';

export default function MessageGroupPage() {
  const { user, token, loading } = useAuth();
  const [messageGroups, setMessageGroups] = React.useState([]);
  const [messages, setMessages] = React.useState([]);
  const [popped, setPopped] = React.useState([]);
  const params = useParams();
  const navigate = useNavigate();
  const [newMessages, setNewMessages] = React.useState(new Set());

  
  // WebSocket connection
  const { lastMessage } = useWebSocket(process.env.REACT_APP_WEBSOCKET_URL);

  // -------------------------------
  // Fetch message groups (once per session)
  // -------------------------------
  React.useEffect(() => {
    if (!loading && token) {
      const fetchMessageGroups = async () => {
        try {
          const res = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/message_groups`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          if (res.status === 200) {
            const data = await res.json();
            setMessageGroups(data);
          } else if (res.status === 401) {
            navigate('/signin');
          }
        } catch (err) {
          console.error(err);
        }
      };
      fetchMessageGroups();
    }
  }, [loading, token, navigate]);

  // -------------------------------
  // Fetch messages whenever handle changes
  // -------------------------------
  React.useEffect(() => {
    if (!loading && token) {
      const fetchMessages = async () => {
        try {
          // const handle = params.handle.replace(/^@/, ''); // remove @
          // const res = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/messages/@${handle}`, {
          const uuid = params.handle;
const res = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/messages/user/${uuid}`, {

            headers: { Authorization: `Bearer ${token}` },
          });
          if (res.status === 200) {
            const data = await res.json();
            setMessages(data);
          } else if (res.status === 401) {
            navigate('/signin');
          }
        } catch (err) {
          console.error(err);
        }
      };
      fetchMessages();
    }
  }, [loading, token, params.handle, navigate]);

 // Handle WebSocket messages for real-time updates
React.useEffect(() => {
  if (lastMessage?.type === 'new_message' && token) {
    // Extract username from email for comparison
    const currentUserHandle = user?.handle?.split('@')[0];
    
    // Only show notification if message is not from current user
    if (lastMessage.data.sender_handle !== currentUserHandle) {
      const conversationId = lastMessage.data.conversation_id;
      setNewMessages(prev => new Set([...prev, conversationId]));
    }
    
    // Refresh message groups to show updated conversation list
    const fetchMessageGroups = async () => {
      try {
        const res = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/message_groups`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.status === 200) {
          const data = await res.json();
          setMessageGroups(data);
        }
      } catch (err) {
        console.error(err);
      }
    };
    fetchMessageGroups();
    
    // Refresh messages for current conversation
    // const handle = params.handle.replace(/^@/, '');
    const uuid = params.handle;
    const fetchMessages = async () => {
      try {
        // const res = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/messages/@${handle}`, {
        const uuid = params.handle;
const res = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/messages/user/${uuid}`, {

          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.status === 200) {
          const data = await res.json();
          setMessages(data);
        }
      } catch (err) {
        console.error(err);
      }
    };
    fetchMessages();
  }
}, [lastMessage, token, params.handle, user]);




  if (loading) return <p>Loading...</p>;

  return (
    <article>
      <DesktopNavigation user={user} active="messages" setPopped={setPopped} />
      
      <section className="message_groups">
        <MessageGroupFeed 
          message_groups={messageGroups} 
          newMessages={newMessages}
          setNewMessages={setNewMessages}
        />
      </section>

      <div className="content messages">
        {/* <MessagesFeed messages={messages} /> */}
        <MessagesFeed messages={messages} user={user} />

        <MessagesForm setMessages={setMessages} />
      </div>
    </article>
  );
}
