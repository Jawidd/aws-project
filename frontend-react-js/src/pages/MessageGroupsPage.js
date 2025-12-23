// this page shows only MessageGroupFeed (list of groups)
import './MessageGroupsPage.css';
import React from "react";
import { useNavigate } from 'react-router-dom';
import useAuth from '../hooks/useAuth';
import useWebSocket from '../hooks/useWebSocket';

import DesktopNavigation from '../components/DesktopNavigation';
import MessageGroupFeed from '../components/MessageGroupFeed';
import LoadingSpinner from '../components/LoadingSpinner';

export default function MessageGroupsPage() {
  const { user, token, loading } = useAuth();
  const [messageGroups, setMessageGroups] = React.useState([]);
  const [usersWithoutConversations, setUsersWithoutConversations] = React.useState([]);
  const [popped, setPopped] = React.useState([]);
  const dataFetchedRef = React.useRef(false);
  const navigate = useNavigate();
  const [newMessages, setNewMessages] = React.useState(new Set());

  
  // WebSocket connection
  const { lastMessage } = useWebSocket(process.env.REACT_APP_WEBSOCKET_URL);

  const loadData = async (token) => {
    try {
      // Load message groups
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/message_groups`;
      const res = await fetch(backend_url, {
        method: "GET",
        headers: { Authorization: `Bearer ${token}` }
      });

      const resJson = await res.json();
      if (res.status === 200) {
        setMessageGroups(resJson);
      } else if (res.status === 401) {
        alert('Please sign in to access message groups.');
        navigate('/signin');
        return;
      } else {
        console.log(res);
      }

      // Load users without conversations
      const users_url = `${process.env.REACT_APP_BACKEND_URL}/api/users/without_conversations`;
      const usersRes = await fetch(users_url, {
        method: "GET",
        headers: { Authorization: `Bearer ${token}` }
      });

      if (usersRes.status === 200) {
        const usersJson = await usersRes.json();
        setUsersWithoutConversations(usersJson);
      }
    } catch (err) {
      console.log(err);
    }
  };

  React.useEffect(() => {
    if (!loading && token && !dataFetchedRef.current) {
      dataFetchedRef.current = true;
      loadData(token);
    }
  }, [loading, token]);

  // Handle WebSocket messages
  React.useEffect(() => {
    if (lastMessage?.type === 'new_message') {
      const conversationId = lastMessage.data.conversation_id;
      setNewMessages(prev => new Set([...prev, conversationId]));
      if (token) {
        loadData(token);
      }
    }
  }, [lastMessage, token]);

  if (loading) return <LoadingSpinner text="Loading messages..." />;

  return (
    <div className="app">
      <div className="main-container">
        <div className="sidebar">
          <DesktopNavigation user={user} active={'messages'} setPopped={setPopped} />
        </div>
        <main className="main-content">
          <MessageGroupFeed 
            message_groups={messageGroups} 
            users_without_conversations={usersWithoutConversations}
            newMessages={newMessages}
            setNewMessages={setNewMessages}
          />
        </main>
        <div className="right-sidebar">
          {/* Empty for messages page */}
        </div>
      </div>
    </div>
  );
}
