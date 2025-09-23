import './HomeFeedPage.css';
import React from "react";

// amplify-cognito Authenication
import { getCurrentUser, signOut , fetchAuthSession} from 'aws-amplify/auth';



import DesktopNavigation  from '../components/DesktopNavigation';
import DesktopSidebar     from '../components/DesktopSidebar';
import ActivityFeed from '../components/ActivityFeed';
import ActivityForm from '../components/ActivityForm';
import ReplyForm from '../components/ReplyForm';


export default function HomeFeedPage() {
  const [activities, setActivities] = React.useState([]);
  const [popped, setPopped] = React.useState(false);
  const [poppedReply, setPoppedReply] = React.useState(false);
  const [replyActivity, setReplyActivity] = React.useState({});
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);
  

  const loadData = async () => {
    try {
      const session = await fetchAuthSession(); //ass session tokens as headers 
      const token = session.tokens?.accessToken?.toString(); //ass session tokens as headers 


      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/home`
      const res = await fetch(backend_url, {
        headers: { 
          Authorization: `Bearer ${token}` //ass session tokens as headers 
        },
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


//check auth with amplify-cognito
const checkAuth = async () => {
  try {
    const user = await getCurrentUser();
    console.log({user});
    setUser({
      display_name: user.signInDetails?.loginId || user.username,
      handle: user.username
    });
    return true; // User is authenticated
  } catch (err) {
    if (err.name === 'UserUnAuthenticatedException') {
      console.log('User not authenticated');
    } else {
      console.log(err);
    }
    setUser(null);
    return false; // User is not authenticated
  }
};






React.useEffect(() => {
  if (dataFetchedRef.current) return;
  dataFetchedRef.current = true;

  checkAuth().then(isAuthenticated => {
    if (isAuthenticated) {
      loadData();
    }
  });
}, [])

  return (
    <article>
      <DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
      <div className='content'>
        <ActivityForm  
          popped={popped}
          setPopped={setPopped} 
          setActivities={setActivities} 
        />
        <ReplyForm 
          activity={replyActivity} 
          popped={poppedReply} 
          setPopped={setPoppedReply} 
          setActivities={setActivities} 
          activities={activities} 
        />
        <ActivityFeed 
          title="Home" 
          setReplyActivity={setReplyActivity} 
          setPopped={setPoppedReply} 
          activities={activities} 
        />
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}