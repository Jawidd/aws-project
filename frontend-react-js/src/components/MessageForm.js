import './MessageForm.css';
import React from "react";
import { useParams } from 'react-router-dom';
import useAuth from '../hooks/useAuth';

export default function MessageForm({ setMessages }) {
  const { token } = useAuth(); // Get JWT token
  const [count, setCount] = React.useState(0);
  const [message, setMessage] = React.useState('');
  const params = useParams();

  const classes = ['count'];
  if (1024 - count < 0) classes.push('err');

  const onsubmit = async (event) => {
    event.preventDefault();
    if (!token || !message.trim()) return; // No token or empty message, do nothing

    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/messages`;
      const res = await fetch(backend_url, {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` // <-- Send JWT
        },
        body: JSON.stringify({
          message: message,
          user_receiver_uuid: params.uuid || params.handle
        }),
      });

      const data = await res.json();

      if (res.status === 200) {
        // Add new message to the messages feed
        setMessages(current => [...current, data]);
        setMessage(''); // clear textarea
        setCount(0);
      } else {
        console.error('Message POST failed', res, data);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const textarea_onchange = (event) => {
    setCount(event.target.value.length);
    setMessage(event.target.value);
  };
  const textarea_onkeydown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    onsubmit(event);
  }
};


  return (
    <form className='message_form' onSubmit={onsubmit}>
      <textarea
        type="text"
        placeholder="send a direct message..."
        value={message}
        onChange={textarea_onchange}
        onKeyDown={textarea_onkeydown}
      />

      <div className='submit'>
        <div className={classes.join(' ')}>{1024 - count}</div>
        <button 
          type='submit' 
          disabled={!message.trim()}
          className={!message.trim() ? 'disabled' : ''}
        >
          Send
        </button>
      </div>
    </form>
  );
}
