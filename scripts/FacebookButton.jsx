import React from 'react';
import PropTypes from 'prop-types';
import FacebookLogin from 'react-facebook-login';
import Socket from './Socket';

const FacebookButton = ({ setUsername }) => {
  const responseFacebook = (response) => {
    Socket.emit('new facebook user', {
      name: response.name,
      email: response.email,
      url: response.picture.data.url,
    });
    setUsername(response.name);
  };

  return (
    <FacebookLogin
      appId="993947061124717"
      autoLoad={false}
      textButton="Facebook Login"
      fields="name,email,picture"
      callback={responseFacebook}
    />
  );
};

FacebookButton.propTypes = {
  setUsername: PropTypes.func,
};
FacebookButton.defaultProps = {
  setUsername: PropTypes.func,
};

export default FacebookButton;
