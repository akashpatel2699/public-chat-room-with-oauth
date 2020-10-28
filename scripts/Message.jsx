import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import ReactHtmlParser from 'react-html-parser';

const Message = ({ message, username }) => {
  const [style, setStyle] = useState('message-container');

  useEffect(() => {
    /* eslint-disable */
    (username === message.username) ? setStyle((prev) => `${prev} right-side`) : null;
    (message.username === 'sugerBot') ? setStyle((prev) => `${prev} bot-message`) : null;
    /* eslint-enable */
  }, []);

  const stringDatetimeObject = (string) => new Date(Date.parse(string));
  const createdAt = stringDatetimeObject(message.created_at);

  const imageOrAnchorTag = (url) => {
    let htmlTag = '';
    if (url.message_type === 'image url') {
      htmlTag = `<a href=${url.message} target="_blank">${url.message}</a><br>
                <img src=${url.message}>`;
    } else {
      htmlTag = `<a href=${url.message} target="_blank">${url.message}</a>`;
    }

    return htmlTag;
  };

  return (
    <div className={style}>
      <div className="message-info">
        <span className="username">
          <strong>
            {message.username}
          </strong>
        </span>
        <span className="date-time">
          {createdAt.getMonth()}
          /
          {createdAt.getDate()}
          /
          {createdAt.getFullYear()}
          <span className="time">
            {createdAt.getHours() === 12 ? createdAt.getHours()
              : createdAt.getHours() % 12}
            :
            {createdAt.getMinutes()}
          </span>
        </span>
      </div>
      <div className="message">
        <span>
          { ReactHtmlParser(
            (message.message_type === 'url link' || message.message_type === 'image url')
              ? imageOrAnchorTag(message) : message.message,
          ) }
        </span>
      </div>
    </div>
  );
};

Message.propTypes = {
  message: PropTypes.string,
  username: PropTypes.string,
};
Message.defaultProps = {
  message: '',
  username: '',
};

export default Message;
