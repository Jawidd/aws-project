import './Replies.css';
import ActivityContent from './ActivityContent';
import ActivityActionReply from './ActivityActionReply';
import ActivityActionRepost from './ActivityActionRepost';
import ActivityActionLike from './ActivityActionLike';
import ActivityActionShare from './ActivityActionShare';

export default function Replies(props) {
  const { replies = [], setReplyActivity, setPopped } = props;

  let content;
  if (!replies.length) {
    content = (
      <div className='replies_primer'>
        <span>Nothing to see here yet</span>
      </div>
    );
  } else {
    content = (
      <div className='replies'>
        {replies.map((activity) => (
          <div key={activity.uuid} className='activity_item'>
            <ActivityContent activity={activity} />
            <div className="activity_actions">
              <ActivityActionReply setReplyActivity={setReplyActivity} activity={activity} setPopped={setPopped} activity_uuid={activity.uuid} count={activity.replies_count}/>
              <ActivityActionRepost activity_uuid={activity.uuid} count={activity.reposts_count}/>
              <ActivityActionLike activity_uuid={activity.uuid} count={activity.likes_count} liked={activity.liked}/>
              <ActivityActionShare activity_uuid={activity.uuid} />
            </div>
          </div>
        ))}
      </div>
    );
  }

  return <div>{content}</div>;
}
