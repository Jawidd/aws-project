import './TrendingActivity.css';
import {ReactComponent as HeartIcon} from './svg/heart.svg';

export default function TrendingActivity(props) {
  return (
    <div className="trending_activity">
      <div className="trending_activity_content">
        <div className="trending_activity_message">{props.message}</div>
        <div className="trending_activity_meta">
          <span className="trending_activity_author">@{props.handle}</span>
          <div className="trending_activity_likes">
            <HeartIcon className="trending_heart_icon" />
            <span>{props.likes_count}</span>
          </div>
        </div>
      </div>
    </div>
  );
}