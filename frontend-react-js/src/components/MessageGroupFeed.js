import './MessageGroupFeed.css';
import MessageGroupItem from './MessageGroupItem';
import UserWithoutConversationItem from './UserWithoutConversationItem';

export default function MessageGroupFeed(props) {
  return (
    <div className='message_group_feed'>
      <div className='message_group_feed_heading'>
        <div className='title'>Messages</div>
      </div>
      <div className='message_group_feed_collection'>
        {props.message_groups.map(message_group => {
        return  <MessageGroupItem 
                                  key={message_group.uuid} 
                                  message_group={message_group}
                                  hasNewMessage={props.newMessages?.has(message_group.uuid)}
                                  onMarkAsRead={() => props.setNewMessages?.(prev => {
                                    const newSet = new Set(prev);
                                    newSet.delete(message_group.uuid);
                                    return newSet;
                                  })}
                                />
        })}
      </div>
      {props.users_without_conversations && props.users_without_conversations.length > 0 && (
        <>
          <div className='users_without_conversations_heading'>
            <div className='title'>Start New Conversation</div>
          </div>
          <div className='users_without_conversations_collection'>
            {props.users_without_conversations.map(user => {
              return <UserWithoutConversationItem key={user.uuid} user={user} />;
            })}
          </div>
        </>
      )}
    </div>
  );
}