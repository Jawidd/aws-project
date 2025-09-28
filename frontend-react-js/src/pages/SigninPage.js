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

// Add this check at the beginning of SigninPage component
React.useEffect(() => {
  const checkAuthStatus = async () => {
    try {
      const user = await getCurrentUser();
      if (user) {
        // User is already signed in, redirect to home
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
      console.log('Authentication successful for user:', email); //DEBUG!! line
      const { isSignedIn, nextStep } = await signIn({ username: email, password });
      if (isSignedIn) {
        console.log('Authentication successful for user:', email);//DEBUG!! line
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
      <div className='signin-info'>
        <Logo className='logo' />
      </div>
      <div className='signin-wrapper'>
        <form 
          className='signin_form'
          onSubmit={onsubmit}
        >
          <h2>Sign into your Cruddur account</h2>
          {isFromConfirmation && (
            <div style={{
              color: '#10b981',
              textAlign: 'center',
              marginBottom: '20px',
              padding: '12px',
              backgroundColor: 'rgba(16, 185, 129, 0.1)',
              borderRadius: '8px',
              border: '1px solid rgba(16, 185, 129, 0.2)'
            }}>
              ✅ Email confirmed successfully! Please sign in.
            </div>
          )}
          <div className='fields'>
            <div className='field text_field username'>
              <label>Email</label>
              <input
                type="text"
                value={email}
                onChange={email_onchange} 
              />
            </div>
            <div className='field text_field password'>
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={password_onchange} 
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
          <span>
            Don't have an account?
          </span>
          <Link to="/signup">Sign up!</Link>
        </div>
      </div>
    </article>
  );
}
