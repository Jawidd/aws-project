import './HomeFeedPage.css';
import React from "react";
import useAuth from '../hooks/useAuth';

import DesktopNavigation  from '../components/DesktopNavigation';
import DesktopSidebar     from '../components/DesktopSidebar';
import ActivityFeed from '../components/ActivityFeed';
import ActivityForm from '../components/ActivityForm';
import ReplyForm from '../components/ReplyForm';
import LoadingSpinner from '../components/LoadingSpinner';

export default function HomeFeedPage() {
  const { user, token, loading, updateUserProfile } = useAuth();
  const [activities, setActivities] = React.useState([]);
  const [popped, setPopped] = React.useState(false);
  const [poppedReply, setPoppedReply] = React.useState(false);
  const [replyActivity, setReplyActivity] = React.useState({});
  const dataFetchedRef = React.useRef(false);

  const loadData = async (token) => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/home`;
      const res = await fetch(backend_url, {
        headers: { Authorization: `Bearer ${token}` },
        method: "GET"
      });
      const contentType = res.headers.get('content-type') || '';
      const isJson = contentType.includes('application/json');
      const body = isJson ? await res.json() : await res.text();

      if (!res.ok) {
        console.error('Failed to load home feed', { status: res.status, body });
        return;
      }

      setActivities(isJson ? body : []);
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

  if (loading) return <LoadingSpinner text="Loading home feed..." />;

  return (
    <article>
      <DesktopNavigation user={user} active={'home'} setPopped={setPopped} updateUserProfile={updateUserProfile} />
      <div className='content'>
        <ActivityForm  
          popped={popped} setPopped={setPopped} setActivities={setActivities} 
        />
        <ReplyForm 
          activity={replyActivity} popped={poppedReply} 
          setPopped={setPoppedReply} setActivities={setActivities} activities={activities} 
        />
        <ActivityFeed title="Home" setReplyActivity={setReplyActivity} setPopped={setPoppedReply} activities={activities} />
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}
