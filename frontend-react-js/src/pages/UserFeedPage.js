import './UserFeedPage.css';
import React from "react";
import { useParams } from 'react-router-dom';
import process from 'process';
import useAuth from '../hooks/useAuth';

import DesktopNavigation  from '../components/DesktopNavigation';
import DesktopSidebar     from '../components/DesktopSidebar';
import ActivityFeed from '../components/ActivityFeed';
import ActivityForm from '../components/ActivityForm';
import ProfileInfo from '../components/ProfileInfo';
import ProfileForm from '../components/ProfileForm';
import LoadingSpinner from '../components/LoadingSpinner';

export default function UserFeedPage() {
  const { user, token, loading } = useAuth();
  const [activities, setActivities] = React.useState([]);
  const [popped, setPopped] = React.useState([]);
  const [poppedProfile, setPoppedProfile] = React.useState(false);
  const [profile, setProfile] = React.useState([]);
  const dataFetchedRef = React.useRef(false);

  const params = useParams();
  const title = `@${params.handle}`;

  const loadData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/${title}`
      const res = await fetch(backend_url, {
        method: "GET"
      });
      let resJson = await res.json();
      if (res.status === 200) {
        setActivities(resJson)
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  };

  const loadUserShortData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/users/${title}/short`
      const res = await fetch(backend_url, {
        method: "GET"
      });
      let resJson = await res.json();
      if (res.status === 200) {
        setProfile(resJson)
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  };



  React.useEffect(()=>{
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadData();
    loadUserShortData();
  }, [])

  if (loading) return <LoadingSpinner text="Loading user profile..." />;

  return (
    <article>
      <DesktopNavigation user={user} active={'profile'} setPopped={setPopped} />
      <div className='content'>
        <ActivityForm popped={popped} setActivities={setActivities} />
        <div className='content_feed'>
          <div className='content_feed_heading'>
            <div className='title'>{title}</div>
          </div>
          <ProfileInfo user={user} profile={profile} setPopped={setPoppedProfile} />
          <ActivityFeed title={title} activities={activities} />
        </div>
      </div>
      <DesktopSidebar user={user} />
      <ProfileForm 
        profile={profile}
        popped={poppedProfile} 
        setPopped={setPoppedProfile} 
      />
    </article>
  );
}