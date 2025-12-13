import {ReactComponent as HeartIcon} from './svg/heart.svg';
import { useState } from 'react';
import { fetchAuthSession } from 'aws-amplify/auth';

export default function ActivityActionLike(props) {
  const [likesCount, setLikesCount] = useState(props.count || 0);
  const [isLiked, setIsLiked] = useState(props.liked || false);
  const [isLiking, setIsLiking] = useState(false);

  const onclick = async (event) => {
    event.preventDefault();
    
    if (isLiking) return;
    
    setIsLiking(true);
    
    try {
      const session = await fetchAuthSession();
      const token = session.tokens?.accessToken?.toString();
      
      if (!token) {
        console.error('Please sign in to like activities');
        return;
      }
      
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/${props.activity_uuid}/like`;
      
      const res = await fetch(backend_url, {
        method: "POST",
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (res.ok) {
        const data = await res.json();
        setLikesCount(data.likes_count);
        setIsLiked(data.liked);
      } else {
        console.error('Failed to like activity');
      }
    } catch (err) {
      console.error('Error liking activity:', err);
    } finally {
      setIsLiking(false);
    }
  }

  let counter;
  if (likesCount > 0) {
    counter = <div className="counter">{likesCount}</div>;
  }

  return (
    <div onClick={onclick} className={`action activity_action_heart ${isLiked ? 'liked' : ''} ${isLiking ? 'loading' : ''}`}>
      <HeartIcon className='icon' />
      {counter}
    </div>
  )
}