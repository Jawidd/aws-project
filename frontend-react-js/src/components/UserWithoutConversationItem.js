import './UserWithoutConversationItem.css';
import { Link } from "react-router-dom";

export default function UserWithoutConversationItem(props) {
  return (
    <Link className="user_without_conversation_item" to={`/messages/@${props.user.uuid}`}>
      <div className='user_avatar'></div>
      <div className='user_content'>
        <div className='user_identity'>
          <div className='display_name'>{props.user.full_name}</div>
          <div className="handle">@{props.user.handle}</div>
        </div>
        <div className="start_conversation">Start conversation</div>
      </div>
    </Link>
  );
}