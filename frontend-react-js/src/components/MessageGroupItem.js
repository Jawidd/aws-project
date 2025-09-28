import './MessageGroupItem.css';
import { Link } from "react-router-dom";
import { DateTime } from 'luxon';
import { useParams } from 'react-router-dom';

export default function MessageGroupItem(props) {
  const params = useParams();

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

  const classes = () => {
    let classes = ["message_group_item"];
    if (params.handle == props.message_group.original_uuid){
      classes.push('active')
    }
    return classes.join(' ');
  }

  return (
    <Link className={classes()} to={`/messages/@`+props.message_group.original_uuid}>
      <div className='message_group_avatar'></div>
      <div className='message_content'>
        <div className='message_group_meta'>
          <div className='message_group_identity'>
            <div className='display_name'>{props.message_group.full_name}</div>
            <div className="handle">@{props.message_group.handle}</div>
          </div>
        </div>
        <div className="message">{props.message_group.message}</div>
        <div className="created_at" title={props.message_group.created_at}>
          <span className='ago'>{format_time_created_at(props.message_group.created_at)}</span> 
        </div>
      </div>
    </Link>
  );
}
