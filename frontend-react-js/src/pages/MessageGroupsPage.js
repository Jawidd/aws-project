// this page shows only MessageGroupFeed (list of groups)
import './MessageGroupsPage.css';
import React from "react";
import { useNavigate } from 'react-router-dom';
import useAuth from '../hooks/useAuth';

import DesktopNavigation from '../components/DesktopNavigation';
import MessageGroupFeed from '../components/MessageGroupFeed';

export default function MessageGroupsPage() {
  const { user, token, loading } = useAuth();
  const [messageGroups, setMessageGroups] = React.useState([]);
  const [popped, setPopped] = React.useState([]);
  const dataFetchedRef = React.useRef(false);
  const navigate = useNavigate();

  const loadData = async (token) => {
    try {
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
      } else {
        console.log(res);
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

  if (loading) return <p>Loading...</p>;

  return (
    <article>
      <DesktopNavigation user={user} active={'messages'} setPopped={setPopped} />
      <section className='message_groups'>
        <MessageGroupFeed message_groups={messageGroups} />
      </section>
      <div className='content'></div>
    </article>
  );
}
