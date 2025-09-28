import { useState, useEffect } from 'react';
import { getCurrentUser, fetchAuthSession, fetchUserAttributes, signOut } from 'aws-amplify/auth';

export default function useAuth() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const initAuth = async () => {
      try {
        const user = await getCurrentUser();
        const attributes = await fetchUserAttributes();
        const session = await fetchAuthSession();
        const token = session.tokens?.accessToken?.toString();
        
        setUser({
          display_name: attributes.preferred_username,
          handle: user.signInDetails?.loginId
        });
        setToken(token);
      } catch (err) {
        console.log("User not authenticated", err);
        
        // If token is revoked, sign out completely
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

  return { user, token, loading };
}
