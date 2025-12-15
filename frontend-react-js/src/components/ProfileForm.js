import './ProfileForm.css';
import './Popup.css';
import React from "react";
import process from 'process';
import useAuth from '../hooks/useAuth';

export default function ProfileForm(props) {
  const { token } = useAuth();
  const [bio, setBio] = React.useState('');
  const [displayName, setDisplayName] = React.useState('');
  const [avatarPreview, setAvatarPreview] = React.useState('');
  const [uploadingAvatar, setUploadingAvatar] = React.useState(false);
  const [uploadMessage, setUploadMessage] = React.useState('');
  const [uploadError, setUploadError] = React.useState('');

  React.useEffect(()=>{
    setBio(props.profile.bio || "");
    setDisplayName(props.profile.display_name || "");
    setAvatarPreview(props.profile.avatar_url || "");
  }, [props.profile])

  const requestPresignedUrl = async (extension, contentType) => {
    if (!token) {
      throw new Error("You must be signed in to upload an avatar");
    }

    const gatewayBase = process.env.REACT_APP_AVATAR_API_URL;
    if (!gatewayBase) {
      throw new Error("Avatar upload endpoint is not configured");
    }

    const res = await fetch(`${gatewayBase}/avatars/presign`, {
      method: "POST",
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        extension: extension,
        content_type: contentType
      }),
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || 'Unable to get upload URL');
    }
    return data.upload_url;
  };

  const fetchProfile = async () => {
    if (!token) return null;
    const res = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/profile/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!res.ok) return null;
    return res.json();
  };

  const waitForProcessedAvatar = async (previousUrl) => {
    const attempts = 5;
    const delayMs = 1500;

    for (let i = 0; i < attempts; i++) {
      await new Promise((resolve) => setTimeout(resolve, delayMs));
      const profile = await fetchProfile();
      if (profile?.avatar_url && profile.avatar_url !== previousUrl) {
        return profile;
      }
    }
    return null;
  };

  const handleAvatarChange = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploadError('');
    setUploadMessage('');
    setUploadingAvatar(true);

    const previewUrl = URL.createObjectURL(file);
    setAvatarPreview(previewUrl);

    const parts = file.name.split('.');
    const extension = (parts.length > 1 ? parts.pop() : 'jpg');

    try {
      const uploadUrl = await requestPresignedUrl(extension, file.type);
      const uploadRes = await fetch(uploadUrl, {
        method: "PUT",
        headers: { 'Content-Type': file.type },
        body: file
      });

      if (!uploadRes.ok) {
        throw new Error(`Upload failed with status ${uploadRes.status}`);
      }

      const previousUrl = props.profile?.avatar_url || "";
      const refreshedProfile = await waitForProcessedAvatar(previousUrl);

      if (refreshedProfile && props.updateUserProfile) {
        props.updateUserProfile({
          display_name: refreshedProfile.display_name || displayName,
          bio: refreshedProfile.bio ?? bio,
          avatar_url: refreshedProfile.avatar_url,
          handle: refreshedProfile.handle,
          uuid: refreshedProfile.uuid,
          cognito_user_id: refreshedProfile.cognito_user_id
        });
        setAvatarPreview(refreshedProfile.avatar_url || previewUrl);
        setUploadMessage("Avatar updated!");
      } else {
        setUploadMessage("Upload started. The image will refresh after processing.");
      }
    } catch (err) {
      console.log(err);
      setUploadError(err.message || 'Upload failed');
      setAvatarPreview(props.profile.avatar_url || "");
    } finally {
      setUploadingAvatar(false);
    }
  };

  const onsubmit = async (event) => {
    event.preventDefault();
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/profile/update`
      const res = await fetch(backend_url, {
        method: "POST",
        headers: {
          'Authorization': `Bearer ${token}`,
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          bio: bio,
          display_name: displayName
        }),
      });
      let data = await res.json();
      if (res.status === 200) {
        // Update the user profile globally
        if (props.updateUserProfile) {
          props.updateUserProfile({
            bio: bio,
            display_name: displayName
          });
        }
        props.setPopped(false)
      } else {
        console.log('Profile update failed:', res, data)
      }
    } catch (err) {
      console.log(err);
    }
  }

  const bio_onchange = (event) => {
    setBio(event.target.value);
  }

  const display_name_onchange = (event) => {
    setDisplayName(event.target.value);
  }

  const close = (event)=> {
    if (event.target.classList.contains("profile_popup")) {
      props.setPopped(false)
    }
  }

  if (props.popped === true) {
    return (
      <div className="popup_form_wrap profile_popup" onClick={close}>
        <form 
          className='profile_form popup_form'
          onSubmit={onsubmit}
        >
          <div className="popup_heading">
            <div className="popup_title">Edit Profile</div>
            <div className='submit'>
              <button type='submit'>Save</button>
            </div>
          </div>
          <div className="popup_content">
            <div className="field avatar">
              <label>Avatar</label>
              <div className="avatar_upload">
                <div
                  className="avatar_preview"
                  style={avatarPreview ? { backgroundImage: `url(${avatarPreview})` } : {}}
                ></div>
                <label className="upload_button">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleAvatarChange}
                    disabled={uploadingAvatar}
                  />
                  {uploadingAvatar ? 'Uploading...' : 'Choose file'}
                </label>
              </div>
              {uploadMessage && <div className="upload_message">{uploadMessage}</div>}
              {uploadError && <div className="upload_error">{uploadError}</div>}
            </div>
            <div className="field display_name">
              <label>Display Name</label>
              <input
                type="text"
                placeholder="Display Name"
                value={displayName}
                onChange={display_name_onchange} 
              />
            </div>
            <div className="field bio">
              <label>Bio</label>
              <textarea
                placeholder="Bio"
                value={bio}
                onChange={bio_onchange} 
              />
            </div>
          </div>
        </form>
      </div>
    );
  }
}
