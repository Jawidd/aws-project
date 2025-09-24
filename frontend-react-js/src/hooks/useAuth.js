import { useState, useEffect } from 'react';
import { getCurrentUser, fetchAuthSession, fetchUserAttributes } from 'aws-amplify/auth';

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
        setUser(null);
        setToken(null);
        window.location.href = "/signin"; // Redirect to signin
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  return { user, token, loading };
}
