import './DesktopNavigation.css';
import {ReactComponent as Logo} from './svg/logo.svg';
import DesktopNavigationLink from '../components/DesktopNavigationLink';
import CrudButton from '../components/CrudButton';
import ProfileInfo from '../components/ProfileInfo';
import React from 'react';
import { Link } from 'react-router-dom';

export default function DesktopNavigation(props) {
  const [isLocked, setIsLocked] = React.useState(() => {
    const saved = document.cookie.split('; ').find(row => row.startsWith('navLocked='));
    return saved ? saved.split('=')[1] === 'true' : true;
  });
  const [isHovered, setIsHovered] = React.useState(false);


  const toggleLock = () => {
    const newLockState = !isLocked;
    setIsLocked(newLockState);
    document.cookie = `navLocked=${newLockState}; path=/; max-age=31536000`;
  };

  let button;
  let profile;
  let notificationsLink;
  let messagesLink;
  let profileLink;
  if (props.user) {
    button = <CrudButton setPopped={props.setPopped} />;
    profile = <ProfileInfo user={props.user} profile={props.user} />;
    notificationsLink = <DesktopNavigationLink 
      url="/notifications" 
      name="Notifications" 
      handle="notifications" 
      active={props.active} />;
    messagesLink = <DesktopNavigationLink 
      url="/messages"
      name="Messages"
      handle="messages" 
      active={props.active} />
    profileLink = <DesktopNavigationLink 
      url="/profile" 
      name="Profile"
      handle="profile"
      active={props.active} />
  }

  const showProfile = isLocked || (!isLocked && isHovered);

  return (
    <nav 
      className={!isLocked ? 'hidden' : ''}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <button className="toggle-btn" onClick={toggleLock}>
        {isLocked ? '🔒' : ''}
      </button>
      <Logo className='logo' />
      <DesktopNavigationLink url="/" 
        name="Home"
        handle="home"
        active={props.active} />
      {notificationsLink}
      {messagesLink}
      {profileLink}
      <div className="more-menu-container">
        <button 
          className="more-menu-trigger"
          disabled
        >
          More
        </button>
      </div>
      {button}
      {showProfile && profile}
    </nav>
  );
}
