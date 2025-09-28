import './SignupPage.css';
import React from "react";
import {ReactComponent as Logo} from '../components/svg/logo.svg';
import { Link } from "react-router-dom";

import { signUp, getCurrentUser } from 'aws-amplify/auth';

export default function SignupPage() {

  // Username is Email
  const [name, setName] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [errors, setErrors] = React.useState('');

  React.useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const user = await getCurrentUser();
        if (user) {
          // User is already signed in, redirect to home
          window.location.href = "/";
        }
      } catch (err) {
        // User not signed in, continue with signup page
      }
    };
    
    checkAuthStatus();
  }, []);

  const onsubmit = async (event) => {
    event.preventDefault();
    setErrors('')
    event.preventDefault();
    try {
      const { isSignUpComplete, userId, nextStep } = await signUp({
        username: email,
        password,
        options: {
          userAttributes: {
            name,
            email,
            preferred_username: username,
          },
          autoSignIn: true, // optional - enables auto sign in after user is confirmed
        }
      });
      console.log('Sign up successful for user:', email);
      window.location.href = `/confirm?email=${email}`;
    } catch (error) {
      setErrors(error.message);
    }
    return false;
  }

  const name_onchange = (event) => {
    setName(event.target.value);
  }
  const email_onchange = (event) => {
    setEmail(event.target.value);
  }
  const username_onchange = (event) => {
    setUsername(event.target.value);
  }
  const password_onchange = (event) => {
    setPassword(event.target.value);
  }

  let el_errors;
  if (errors){
    el_errors = <div className='errors'>{errors}</div>;
  }

  return (
    <article className='signup-article'>
      <div className='signup-info'>
        <Logo className='logo' />
      </div>
      <div className='signup-wrapper'>
        <form 
          className='signup_form'
          onSubmit={onsubmit}
        >
          <h2>Sign up to create a Cruddur account</h2>
          <div className='fields'>
            <div className='field text_field name'>
              <label>Name</label>
              <input
                type="text"
                value={name}
                onChange={name_onchange} 
              />
            </div>

            <div className='field text_field email'>
              <label>Email</label>
              <input
                type="text"
                value={email}
                onChange={email_onchange} 
              />
            </div>

            <div className='field text_field username'>
              <label>Username</label>
              <input
                type="text"
                value={username}
                onChange={username_onchange} 
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
            <button type='submit'>Sign Up</button>
          </div>
        </form>
        <div className="already-have-an-account">
          <span>
            Already have an account?
          </span>
          <Link to="/signin">Sign in!</Link>
        </div>
      </div>
    </article>
  );
}
