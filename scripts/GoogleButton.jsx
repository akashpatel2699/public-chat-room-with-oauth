import React from 'react';
import GoogleLogin from 'react-google-login';
import Socket from './Socket';

const onSuccessGoogle = (response) => {
  const { IDToken } = response.getAuthResponse();
  Socket.emit('new google user', {
    IDToken,
  });
};
/* eslint-disable no-console */
const onFailureGoogle = (response) => console.error(response);
/* eslint-enable no-console */

const GoogleButton = () => (
  <GoogleLogin
    clientId="209640983095-i1n972h3s4te5at8bdc0v91dmj89joit.apps.googleusercontent.com"
    buttonText="Google Login"
    onSuccess={onSuccessGoogle}
    onFailure={onFailureGoogle}
    cookiePolicy="single_host_origin"
  />
);

export default GoogleButton;
