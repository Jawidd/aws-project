import './MessageItem.css';
import { format_datetime, message_time_ago } from '../lib/DateTimeFormats';

export default function MessageItem(props) {
  const isSent = props.user?.handle?.startsWith(props.message.handle);

  return (
    <div className={`message_item ${isSent ? 'sent' : 'received'}`}>
      <div className='message_avatar'></div>
      <div className='message_content'>
        <div className='message_meta'>
          <div className='message_identity'>
            <div className='display_name'>{props.message.full_name}</div>
            <div className="handle"></div>
          </div>
        </div>
        <div className="message">{props.message.message}</div>
        <div className="created_at" title={format_datetime(props.message.created_at)}>
          <span className='ago'>{message_time_ago(props.message.created_at)}</span> 
        </div>
      </div>
    </div>
  );
}
