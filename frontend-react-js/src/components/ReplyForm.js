import './ReplyForm.css';
import React from "react";
import process from 'process';
import { fetchAuthSession } from 'aws-amplify/auth';

import ActivityContent from '../components/ActivityContent';

export default function ReplyForm(props) {
  const [count, setCount] = React.useState(0);
  const [message, setMessage] = React.useState('');

  const classes = []
  classes.push('count')
  if (240-count < 0){
    classes.push('err')
  }

  const onsubmit = async (event) => {
    event.preventDefault();
    try {
      const session = await fetchAuthSession();
      const token = session.tokens?.accessToken?.toString();
      
      // When we reply to a reply, we want to attach it to the original post.
      const original_activity_uuid = props.activity.reply_to_activity_uuid || props.activity.uuid;

      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/${original_activity_uuid}/reply`
      const res = await fetch(backend_url, {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          message: message
        }),
      });
      let data = await res.json();
      if (res.status === 200) {
        let activities_deep_copy = JSON.parse(JSON.stringify(props.activities))
        let found_activity = activities_deep_copy.find(function (element) {
          return element.uuid === original_activity_uuid;
        });
        found_activity.replies_count++; 
        found_activity.replies.push(data)

        props.setActivities(activities_deep_copy);
        setCount(0)
        setMessage('')
        props.setPopped(false)
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  }

  const textarea_onchange = (event) => {
    setCount(event.target.value.length);
    setMessage(event.target.value);
  }

  const close = () => {
    props.setPopped(false)
  }

  let content;
  if (props.activity){
    content = <ActivityContent activity={props.activity} />;
  }

  if (props.popped === true) {
    return (
      <div className="popup_form_wrap">
        <div className="popup_form">
          <button className="close_button" onClick={close}>×</button>
          <div className="popup_content">
            <div className="activity_wrap">
              {content}
            </div>
            <form 
              className='replies_form'
              onSubmit={onsubmit}
            >
              <textarea
                type="text"
                placeholder="what is your reply?"
                value={message}
                onChange={textarea_onchange} 
              />
              <div className='submit'>
                <div></div>
                <div className={classes.join(' ')}>{240-count}</div>
                <button type='submit'>Reply</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    );
  }
}
