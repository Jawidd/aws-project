import './ActivityItem.css';

import ActivityContent from '../components/ActivityContent';
import ActivityActionReply from '../components/ActivityActionReply';
import ActivityActionRepost from '../components/ActivityActionRepost';
import ActivityActionLike from '../components/ActivityActionLike';
import ActivityActionShare from '../components/ActivityActionShare';
import { format_datetime } from '../lib/DateTimeFormats';

export default function ActivityShowItem(props) {
  return (
    <div className="activity_item expanded">
      <ActivityContent activity={props.activity} />
      <div className="created_at_full">
        {format_datetime(props.activity.created_at)}
      </div>
      <div className="activity_actions">
        <ActivityActionReply setReplyActivity={props.setReplyActivity} activity={props.activity} setPopped={props.setPopped} activity_uuid={props.activity.uuid} count={props.activity.replies_count}/>
        <ActivityActionRepost activity_uuid={props.activity.uuid} count={props.activity.reposts_count}/>
        <ActivityActionLike activity_uuid={props.activity.uuid} count={props.activity.likes_count} liked={props.activity.liked}/>
        <ActivityActionShare activity_uuid={props.activity.uuid} />
      </div>
    </div>
  )
}
