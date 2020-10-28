import * as React from 'react';
import Form from './Form';
import Socket from './Socket';
import Header from './Header';
import Messages from './Messages';
import ShowUsers from './ShowUsers';
import Login from './Login';

export default function Content() {
  const [messages, setMessages] = React.useState([]);
  const [user, setUser] = React.useState({});
  const [usersConnected, setUsersConnected] = React.useState([]);
  const [userLoggedIn, setUserLoggedIn] = React.useState(false);

  function getNewAddresses() {
    React.useEffect(() => {
      Socket.on('joinuser', (data) => {
        setUser({ username: data.user.username, email: data.user.email });
        setMessages(data.message_objects);
        setUsersConnected(data.usersConnected);
      });
      Socket.on('new message', (data) => {
        setMessages([...messages, data.newMessage]);
      });
      Socket.on('addNewUser', (data) => {
        setUsersConnected([...usersConnected, {
          username: data.addNewUser,
          auth_type: data.auth_type,
          profile_url: data.profile_url,
        },
        ]);
      });
      Socket.on('removeUser', (data) => {
        const { removeUser } = data;
        setUsersConnected(usersConnected.filter((leftUser) => leftUser.username !== removeUser));
      });
      Socket.on('authenticate', (data) => {
        setUserLoggedIn(data.isAuthenticated);
      });
      return () => {
        Socket.off('new message');
        Socket.off('addNewUser');
        Socket.off('removeUser');
        Socket.off('authenticate');
      };
    });
  }

  getNewAddresses();

  return (
    userLoggedIn
      ? (
        <div className="container">
          <Header username={user.username} />
          <ShowUsers usersConnected={usersConnected} />
          <Messages messages={messages} username={user.username} />
          <Form email={user.email} />
        </div>
      )
      : <Login setUsername={setUser} />
  );
}
