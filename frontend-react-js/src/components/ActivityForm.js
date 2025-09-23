import './ActivityForm.css';
import React from "react";
import process from 'process';
import {ReactComponent as BombIcon} from './svg/bomb.svg';
import { fetchAuthSession} from 'aws-amplify/auth';

export default function ActivityForm(props) {
  const [count, setCount] = React.useState(0);
  const [message, setMessage] = React.useState('');
  const [ttl, setTtl] = React.useState('7-days');

  const classes = []
  classes.push('count')
  if (240-count < 0){
    classes.push('err')
  }

  const onsubmit = async (event) => {
    event.preventDefault();
    try {
      const session = await fetchAuthSession();
      const token = session.tokens?.accessToken?.toString();
      
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities`
      console.log('onsubmit payload', message)
      const res = await fetch(backend_url, {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          message: message,
          ttl: ttl
        }),
      });
      let data = await res.json();
      if (res.status === 200) {
        props.setActivities(current => [data,...current]);
        setCount(0)
        setMessage('')
        setTtl('7-days')
        props.setPopped(false)
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  }

  const textarea_onchange = (event) => {
    setCount(event.target.value.length);
    setMessage(event.target.value);
  }

  const ttl_onchange = (event) => {
    setTtl(event.target.value);
  }

  const close = () => {
    props.setPopped(false)
  }

  if (props.popped === true) {
    return (
      <div className="popup_form_wrap">
        <div className="popup_form">
          <button className="close_button" onClick={close}>×</button>
          <div className="popup_content">
            <form 
              className='activity_form'
              onSubmit={onsubmit}
            >
              <textarea
                type="text"
                placeholder="what would you like to say?"
                value={message}
                onChange={textarea_onchange} 
              />
              <div className='submit'>
                <div className='expires_at_field'>
                  <BombIcon className='icon' />
                  <select
                    value={ttl}
                    onChange={ttl_onchange} 
                  >
                    <option value='30-days'>30 days</option>
                    <option value='7-days'>7 days</option>
                    <option value='3-days'>3 days</option>
                    <option value='1-day'>1 day</option>
                    <option value='12-hours'>12 hours</option>
                    <option value='3-hours'>3 hours</option>
                    <option value='1-hour'>1 hour </option>
                  </select>
                </div>
                <div className={classes.join(' ')}>{240-count}</div>
                <button type='submit'>Crud</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    );
  }
}
