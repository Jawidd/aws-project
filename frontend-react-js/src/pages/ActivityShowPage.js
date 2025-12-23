import './ActivityShowPage.css';
import React from "react";
import { useParams, useNavigate } from 'react-router-dom';

import DesktopNavigation from '../components/DesktopNavigation';
import DesktopSidebar from '../components/DesktopSidebar';
import ActivityShowItem from '../components/ActivityShowItem';
import ReplyForm from '../components/ReplyForm';
import Replies from '../components/Replies';
import ActivityForm from '../components/ActivityForm';
import { checkAuth } from '../lib/CheckAuth';

export default function ActivityShowPage() {
  const [activity, setActivity] = React.useState(null);
  const [replies, setReplies] = React.useState([]);
  const [popped, setPopped] = React.useState(false);
  const [poppedReply, setPoppedReply] = React.useState(false);
  const [replyActivity, setReplyActivity] = React.useState(null);
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);
  const params = useParams();
  const navigate = useNavigate();

  const loadData = async () => {
    try {
      const res = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/activities/${params.activity_uuid}`);
      const data = await res.json();
      if (res.ok && data && data.activity) {
        setActivity(data.activity);
        setReplies(data.replies || []);
      }
    } catch (err) {
      console.error('Error loading activity', err);
    }
  };

  React.useEffect(() => {
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;
    loadData();
    checkAuth(setUser);
  }, []);

  const goBack = () => navigate('/');

  let el_activity = null;
  if (activity) {
    el_activity = (
      <ActivityShowItem
        expanded={true}
        setReplyActivity={setReplyActivity}
        setPopped={setPoppedReply}
        activity={activity}
      />
    );
  }

  return (
    <div className="app">
      <div className="main-container">
        <div className="sidebar">
          <DesktopNavigation user={user} active={null} setPopped={setPopped} />
        </div>
        <main className="main-content">
          <ActivityForm
            popped={popped}
            setPopped={setPopped}
          />
          <ReplyForm
            activity={replyActivity || activity}
            popped={poppedReply}
            setReplies={setReplies}
            setPopped={setPoppedReply}
          />
          <div className='activity_feed'>
            <div className='activity_feed_heading'>
              <button className='back-button' onClick={goBack} title="Back to Home">
                <span aria-hidden="true">←</span>
              </button>
              <div className='title'>Post</div>
            </div>
            {el_activity}
            <Replies
              setReplyActivity={setReplyActivity}
              setPopped={setPoppedReply}
              replies={replies}
            />
          </div>
        </main>
        <div className="right-sidebar">
          <DesktopSidebar user={user} forceTrending={true} hideJoin={true} />
        </div>
      </div>
    </div>
  );
}
