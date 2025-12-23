import './SigninPage.css';
import React from "react";
import {ReactComponent as Logo} from '../components/svg/logo.svg';
import { Link, useSearchParams } from "react-router-dom";
import { signIn, getCurrentUser } from 'aws-amplify/auth';

export default function SigninPage() {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [errors, setErrors] = React.useState('');
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
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-header">
          <Logo className='auth-logo' />
          <h1>Sign in to Cruddur</h1>
        </div>
        
        <form className='auth-form' onSubmit={onsubmit}>
          {isFromConfirmation && (
            <div className="success-message">
              ✅ Email confirmed successfully! Please sign in.
            </div>
          )}
          
          <div className='form-field'>
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={email_onchange}
              required
            />
          </div>
          
          <div className='form-field'>
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={password_onchange}
              required
            />
          </div>
          
          {el_errors}
          
          <button type='submit' className="auth-button">Sign In</button>
          
          <Link to="/forgot" className="forgot-link">Forgot Password?</Link>
        </form>
        
        <div className="auth-footer">
          <span>Don't have an account?</span>
          <Link to="/signup">Sign up</Link>
        </div>
      </div>
    </div>
  );
}
