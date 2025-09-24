import './MessageGroupPage.css';
import React from "react";
import { useParams, useNavigate } from 'react-router-dom';
import useAuth from '../hooks/useAuth';

import DesktopNavigation from '../components/DesktopNavigation';
import MessagesFeed from '../components/MessageFeed';
import MessagesForm from '../components/MessageForm';
import MessageGroupFeed from '../components/MessageGroupFeed';

export default function MessageGroupPage() {
  const { user, token, loading } = useAuth();
  const [messageGroups, setMessageGroups] = React.useState([]);
  const [messages, setMessages] = React.useState([]);
  const [popped, setPopped] = React.useState([]);
  const dataFetchedRef = React.useRef(false);
  const params = useParams();
  const navigate = useNavigate();

  const loadMessageGroups = async (token) => {
    try {
      const res = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/message_groups`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      if (res.status === 200) setMessageGroups(data);
      else if (res.status === 401) navigate('/signin');
    } catch (err) {
      console.log(err);
    }
  };

  const loadMessages = async (token) => {
    try {
      const handle = `@${params.handle}`;
      const res = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/messages/@${handle}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      if (res.status === 200) setMessages(data);
      else if (res.status === 401) navigate('/signin');
    } catch (err) {
      console.log(err);
    }
  };

  React.useEffect(() => {
    if (!loading && token && !dataFetchedRef.current) {
      dataFetchedRef.current = true;
      loadMessageGroups(token);
      loadMessages(token);
    }
  }, [loading, token, params.handle]);

  if (loading) return <p>Loading...</p>;

  return (
    <article>
      <DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
      <section className='message_groups'>
        <MessageGroupFeed message_groups={messageGroups} />
      </section>
      <div className='content messages'>
        <MessagesFeed messages={messages} />
        <MessagesForm setMessages={setMessages} />
      </div>
    </article>
  );
}
