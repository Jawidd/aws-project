import './DesktopNavigation.css';
import {ReactComponent as Logo} from './svg/logo.svg';
import DesktopNavigationLink from '../components/DesktopNavigationLink';
import CrudButton from '../components/CrudButton';
import ProfileInfo from '../components/ProfileInfo';
import React from 'react';

export default function DesktopNavigation(props) {
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

  return (
    <nav className="nav-container">
      <div className="nav-header">
        <Logo className='nav-logo' />
      </div>
      <div className="nav-links">
        <DesktopNavigationLink url="/" 
          name="Home"
          handle="home"
          active={props.active} />
        {notificationsLink}
        {messagesLink}
        {profileLink}
      </div>
      {button}
      <div className="nav-profile">
        {profile}
      </div>
    </nav>
  );
}
