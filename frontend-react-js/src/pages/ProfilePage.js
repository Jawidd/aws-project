import './ProfilePage.css';
import React from "react";
import useAuth from '../hooks/useAuth';

import DesktopNavigation from '../components/DesktopNavigation';
import DesktopSidebar from '../components/DesktopSidebar';
import ProfileForm from '../components/ProfileForm';
import LoadingSpinner from '../components/LoadingSpinner';

export default function ProfilePage() {
  const { user, token, loading, updateUserProfile } = useAuth();
  const [poppedEdit, setPoppedEdit] = React.useState(false);
  const avatarStyle = user?.avatar_url ? {
    backgroundImage: `url(${user.avatar_url})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center'
  } : {};
  
  const coverStyle = user?.cover_image_url ? {
    backgroundImage: `url(${user.cover_image_url})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center'
  } : {};

  if (loading) return <LoadingSpinner text="Loading profile..." />;

  if (!user) {
    return <p>Please sign in to view your profile.</p>;
  }

  return (
    <article>
      <DesktopNavigation user={user} active={'profile'} updateUserProfile={updateUserProfile} />
      <div className='content'>
        <div className='content_feed'>
          <div className='content_feed_heading'>
            <div className='title'>My Profile</div>
          </div>
          <div className="profile-display">
            <div className="profile-cover" style={coverStyle}></div>
            <div className="profile-header">
              <div className="profile-avatar-large" style={avatarStyle}></div>
              <div className="profile-details">
                <h2>{user.display_name || 'No Name'}</h2>
                <p className="profile-handle">@{user.handle}</p>
                <p className="profile-email">{user.email}</p>
                <button 
                  className="edit-profile-btn"
                  onClick={() => setPoppedEdit(true)}
                >
                  Edit Profile
                </button>
              </div>
            </div>
            <div className="profile-bio-section">
              <h3>Bio</h3>
              <p>{user.bio || 'No bio available'}</p>
            </div>
          </div>
        </div>
      </div>
      <DesktopSidebar user={user} />
      <ProfileForm 
        profile={user}
        popped={poppedEdit} 
        setPopped={setPoppedEdit}
        updateUserProfile={updateUserProfile}
      />
    </article>
  );
}
