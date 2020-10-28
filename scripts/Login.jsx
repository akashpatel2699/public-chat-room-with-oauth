import React from 'react';
import PropTypes from 'prop-types';
import FacebookButton from './FacebookButton';
import GithubButton from './GithubButton';
import GoogleButton from './GoogleButton';

const Login = ({ setUsername }) => (
  <div className="login-container">
    <div className="login-buttons">
      <FacebookButton setUsername={setUsername} />
      <GithubButton />
      <GoogleButton />
    </div>
  </div>
);

Login.propTypes = {
  setUsername: PropTypes.string,
};
Login.defaultProps = {
  setUsername: '',
};
export default Login;
