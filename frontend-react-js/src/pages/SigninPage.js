import './SigninPage.css';
import React from "react";
import {ReactComponent as Logo} from '../components/svg/logo.svg';
import { Link, useSearchParams } from "react-router-dom";
import { signIn, getCurrentUser } from 'aws-amplify/auth';
import DesktopNavigation from '../components/DesktopNavigation';
import DesktopSidebar from '../components/DesktopSidebar';

export default function SigninPage() {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [errors, setErrors] = React.useState('');
  const [user, setUser] = React.useState(null);
  const [searchParams] = useSearchParams();

  React.useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const user = await getCurrentUser();
        if (user) {
          window.location.href = "/";
        }
      } catch (err) {
        // User not signed in, continue with signin page
      }
    };
    
    checkAuthStatus();
  }, []);

  React.useEffect(() => {
    if (searchParams.get('email')) {
      setEmail(searchParams.get('email'));
    }
  }, []);

  const onsubmit = async (event) => {
    setErrors('')
    event.preventDefault();   
    try {
      const { isSignedIn } = await signIn({ username: email, password });
      if (isSignedIn) {
        window.location.href = "/";
      }
    } catch (error) {
      if (error.name === 'UserNotConfirmedException') {
        window.location.href = "/confirm"
      }
      setErrors(error.message)
    }
    return false;
  }

  const email_onchange = (event) => {
    setEmail(event.target.value);
  }
  const password_onchange = (event) => {
    setPassword(event.target.value);
  }

  let el_errors;
  if (errors){
    el_errors = <div className='errors'>{errors}</div>;
  }

  const isFromConfirmation = searchParams.get('email');

  return (
    <article className="signin-article">
      <DesktopNavigation user={user} active={null} setPopped={() => {}} />
      <div className='content'>
        <div className='signin-wrapper'>
          <form 
            className='signin_form'
            onSubmit={onsubmit}
          >
            <div className='signin-info'>
              <Logo className='logo' />
            </div>
            <h2>Sign into your Cruddur account</h2>
            {isFromConfirmation && (
              <div className="success-message">
                ✅ Email confirmed successfully! Please sign in.
              </div>
            )}
            <div className='fields'>
              <div className='field text_field username'>
                <label>Email</label>
                <input
                  type="email"
                  value={email}
                  onChange={email_onchange}
                  required
                />
              </div>
              <div className='field text_field password'>
                <label>Password</label>
                <input
                  type="password"
                  value={password}
                  onChange={password_onchange}
                  required
                />
              </div>
            </div>
            {el_errors}
            <div className='submit'>
              <Link to="/forgot" className="forgot-link">Forgot Password?</Link>
              <button type='submit'>Sign In</button>
            </div>
          </form>
          <div className="dont-have-an-account">
            <span>Don't have an account?</span>
            <Link to="/signup">Sign up</Link>
          </div>
        </div>
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}
