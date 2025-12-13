import './App.css';

import HomeFeedPage from './pages/HomeFeedPage';
import NotifcicationFeedPage from './pages/NotificationPage';
import UserFeedPage from './pages/UserFeedPage';
import ProfilePage from './pages/ProfilePage';
import SignupPage from './pages/SignupPage';
import SigninPage from './pages/SigninPage';
import RecoverPage from './pages/RecoverPage';
import MessageGroupsPage from './pages/MessageGroupsPage';
import MessageGroupPage from './pages/MessageGroupPage';
import ConfirmationPage from './pages/ConfirmationPage';
import React from 'react';
import process from 'process';
import {
  createBrowserRouter,
  RouterProvider
} from "react-router-dom";

// Amplify
import { Amplify } from 'aws-amplify';

Amplify.configure({
  Auth: {
    Cognito: {
      region: process.env.REACT_APP_AWS_REGION,
      userPoolId: process.env.REACT_APP_USER_POOL_ID,
      userPoolClientId: process.env.REACT_APP_USER_POOL_CLIENT_ID,
      loginWith: {
        email: true
      }
    }
  }
});




const router = createBrowserRouter([
  {
    path: "/",
    element: <HomeFeedPage />
  },
    {
    path: "/notifications",
    element: <NotifcicationFeedPage />
  },
  {
    path: "/@:handle",
    element: <UserFeedPage />
  },
  {
    path: "/profile",
    element: <ProfilePage />
  },
  {
    path: "/messages",
    element: <MessageGroupsPage />
  },
{
  path: "/messages/user/:handle",
  element: <MessageGroupPage />
},

  {
    path: "/signup",
    element: <SignupPage />
  },
  {
    path: "/signin",
    element: <SigninPage />
  },
  {
    path: "/confirm",
    element: <ConfirmationPage />
  },
  {
    path: "/forgot",
    element: <RecoverPage />
  }
]);

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;