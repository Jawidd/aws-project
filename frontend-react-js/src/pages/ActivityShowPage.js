import './ActivityShowPage.css';
import React from "react";
import { useParams } from 'react-router-dom';

import DesktopNavigation from '../components/DesktopNavigation';
import DesktopSidebar from '../components/DesktopSidebar';
import ActivityContent from '../components/ActivityContent';

export default function ActivityShowPage() {
  const [activity, setActivity] = React.useState(null);
  const [replies, setReplies] = React.useState([]);
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);
  const params = useParams();

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
  }, []);

  return (
    <article>
      <DesktopNavigation user={user} active={'home'} />
      <div className='content'>
        <div className='activity_feed'>
          <div className='activity_feed_heading'>
            <div className='title'>Activity</div>
          </div>
          {activity && (
            <div className="activity_item_full">
              <ActivityContent activity={activity} />
            </div>
          )}
          {replies && replies.length > 0 && (
            <div className="replies_list">
              {replies.map((reply) => (
                <div key={reply.uuid} className="activity_item_full">
                  <ActivityContent activity={reply} />
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}
