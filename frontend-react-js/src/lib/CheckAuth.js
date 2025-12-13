export const checkAuth = (setUser) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    const payload = JSON.parse(atob(token.split('.')[1]));
    if (payload.exp > Date.now() / 1000) {
      setUser({
        display_name: payload.display_name,
        handle: payload.handle
      });
      return true;
    }
  }
  return false;
};

export const getAccessToken = () => {
  return localStorage.getItem('access_token');
};