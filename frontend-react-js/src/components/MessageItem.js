import './MessageItem.css';
import { Link } from "react-router-dom";
import { DateTime } from 'luxon';

export default function MessageItem(props) {

  const format_time_created_at = (value) => {
    const created = DateTime.fromISO(value).setZone('Europe/London')
    const now = DateTime.now().setZone('Europe/London')
    const diff_mins = now.diff(created, 'minutes').toObject().minutes;
    const diff_hours = now.diff(created, 'hours').toObject().hours;

    if (diff_hours > 24.0){
      return created.toFormat("LLL L");
    } else if (diff_hours < 24.0 && diff_hours > 1.0) {
      return `${Math.floor(diff_hours)}h`;
    } else if (diff_hours < 1.0) {
      return `${Math.round(diff_mins)}m`;
    }
  };

  return (
    <Link className='message_item' to={`/messages/@`+props.message.handle}>
      <div className='message_avatar'></div>
      <div className='message_content'>
        <div className='message_meta'>
          <div className='message_identity'>
            <div className='display_name'>{props.message.full_name}</div>
            <div className="handle">@{props.message.handle}</div>
          </div>
        </div>
        <div className="message">{props.message.message}</div>
        <div className="created_at" title={props.message.created_at}>
          <span className='ago'>{format_time_created_at(props.message.created_at)}</span> 
        </div>
      </div>
    </Link>
  );
}
