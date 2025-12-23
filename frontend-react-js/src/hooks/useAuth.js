import { useState, useEffect } from 'react';
import { getCurrentUser, fetchAuthSession, fetchUserAttributes, signOut } from 'aws-amplify/auth';

export default function useAuth() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);
  
  const loadUserProfile = async (token, cognito_user_id) => {
    try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/profile/me`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (response.ok) {
          const profile = await response.json();
          return profile;
        }
    } catch (err) {
      console.log('Error loading profile:', err);
    }
    return null;
  };
  
  useEffect(() => {
    const initAuth = async () => {
      try {
        const user = await getCurrentUser();
        const attributes = await fetchUserAttributes();
        const session = await fetchAuthSession();
        const token = session.tokens?.accessToken?.toString();
        
        const email = user.signInDetails?.loginId;
        const urlSafeHandle = email ? email.split('@')[0] : 'user';
        
        // Load profile from database
        const profile = await loadUserProfile(token, user.userId);
        
        setUser({
          display_name: profile?.display_name || attributes.preferred_username || attributes.name || 'User',
          handle: profile?.handle || urlSafeHandle,
          email: email,
          bio: profile?.bio || '',
          uuid: profile?.uuid,
          avatar_url: profile?.avatar_url || null,
          cover_image_url: profile?.cover_image_url || null,
          cognito_user_id: profile?.cognito_user_id || user.userId
        });
        setToken(token);
      } catch (err) {
        console.log("User not authenticated", err);
        
        if (err.name === 'NotAuthorizedException' && err.message.includes('revoked')) {
          try {
            await signOut();
          } catch (signOutErr) {
            console.log('Error signing out:', signOutErr);
          }
        }
        
        setUser(null);
        setToken(null);
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  const updateUserProfile = (newProfile) => {
    setUser(prev => ({ ...prev, ...newProfile }));
  };

  return { user, token, loading, updateUserProfile };
}
