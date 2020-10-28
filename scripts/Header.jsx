import React from 'react';
import PropTypes from 'prop-types';

const Header = ({ username }) => (
  <h1
    className="header"
  >
    Welcome
    {' '}
    {username}
    {' '}
    to the public chat room
  </h1>
);

Header.propTypes = {
  username: PropTypes.string,
};
Header.defaultProps = {
  username: 'default',
};

export default Header;
