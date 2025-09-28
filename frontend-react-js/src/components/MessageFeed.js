import './MessageFeed.css';
import MessageItem from './MessageItem';
import React from 'react';

export default function MessageFeed(props) {
  const messagesEndRef = React.useRef(null);

  React.useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && props.onScrollToBottom) {
          props.onScrollToBottom();
        }
      },
      { threshold: 1.0 }
    );

    if (messagesEndRef.current) {
      observer.observe(messagesEndRef.current);
    }

    return () => observer.disconnect();
  }, [props.onScrollToBottom]);

  return (
    <div className='message_feed'>
      <div className='message_feed_heading'>
        <div className='title'>Messages</div>
      </div>
      <div className='message_feed_collection'>
        {props.messages.map(message => {
        return  <MessageItem key={message.uuid} message={message} user={props.user} />
        })}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}
