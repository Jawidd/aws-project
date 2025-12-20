import './Replies.css';
import ActivityItem from './ActivityItem';

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
      <div className='activities_feed_collection'>
        {replies.map((activity) => (
          <ActivityItem
            setReplyActivity={setReplyActivity}
            setPopped={setPopped}
            key={activity.uuid}
            activity={activity}
          />
        ))}
      </div>
    );
  }

  return <div>{content}</div>;
}
