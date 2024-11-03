import React, { useState } from 'react';

function App() {
  const [user1Message, setUser1Message] = useState('');
  const [user2Message, setUser2Message] = useState('');
  const [user1Messages, setUser1Messages] = useState([]);
  const [user2Messages, setUser2Messages] = useState([]);
  const [error, setError] = useState('');

  const baseUrl = 'http://127.0.0.1:5000';

  // Function to send a message from User 1 to User 2
  const sendMessageUser1 = async () => {
    try {
      const response = await fetch(`${baseUrl}/send_message_user1`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: user1Message }),
      });
      const data = await response.json();
      if (response.ok) {
        alert('Message sent from User 1 to User 2!');
        setUser1Message(''); // Clear input field
      } else {
        setError(`Error: ${data.status}`);
      }
    } catch (error) {
      console.error('Error:', error);
      setError('Failed to send message from User 1.');
    }
  };

  // Function to send a message from User 2 to User 1
  const sendMessageUser2 = async () => {
    try {
      const response = await fetch(`${baseUrl}/send_message_user2`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: user2Message }),
      });
      const data = await response.json();
      if (response.ok) {
        alert('Message sent from User 2 to User 1!');
        setUser2Message(''); // Clear input field
      } else {
        setError(`Error: ${data.status}`);
      }
    } catch (error) {
      console.error('Error:', error);
      setError('Failed to send message from User 2.');
    }
  };

  // Function to retrieve messages for User 1
  const receiveMessagesUser1 = async () => {
    try {
      const response = await fetch(`${baseUrl}/receive_messages_user1`);
      const data = await response.json();
      if (response.ok) {
        setUser1Messages(data.decrypted_messages || []);
        setError('');
      } else {
        setError('Failed to retrieve messages for User 1.');
      }
    } catch (error) {
      console.error('Error:', error);
      setError('Error retrieving messages for User 1.');
    }
  };

  // Function to retrieve messages for User 2
  const receiveMessagesUser2 = async () => {
    try {
      const response = await fetch(`${baseUrl}/receive_messages_user2`);
      const data = await response.json();
      if (response.ok) {
        setUser2Messages(data.decrypted_messages || []);
        setError('');
      } else {
        setError('Failed to retrieve messages for User 2.');
      }
    } catch (error) {
      console.error('Error:', error);
      setError('Error retrieving messages for User 2.');
    }
  };

  return (
    <div style={styles.container}>
      {/* User 1 Section */}
      <div style={styles.userBox}>
        <h2>User 1</h2>
        <textarea
          style={styles.textarea}
          value={user1Message}
          onChange={(e) => setUser1Message(e.target.value)}
          placeholder="Enter your message..."
        ></textarea>
        <button style={styles.button} onClick={sendMessageUser1}>
          Send Message to User 2
        </button>
        <button style={styles.button} onClick={receiveMessagesUser1}>
          Retrieve Messages
        </button>
        <div style={styles.messages}>
          {error && <p style={{ color: 'red' }}>{error}</p>}
          {user1Messages.length > 0 ? (
            user1Messages.map((msg, index) => <p key={index} style={{ color: 'black' }}>{msg}</p>)
          ) : (
            <p>No messages found.</p>
          )}
        </div>
      </div>

      {/* User 2 Section */}
      <div style={styles.userBox}>
        <h2>User 2</h2>
        <textarea
          style={styles.textarea}
          value={user2Message}
          onChange={(e) => setUser2Message(e.target.value)}
          placeholder="Enter your message..."
        ></textarea>
        <button style={styles.button} onClick={sendMessageUser2}>
          Send Message to User 1
        </button>
        <button style={styles.button} onClick={receiveMessagesUser2}>
          Retrieve Messages
        </button>
        <div style={styles.messages}>
          {error && <p style={{ color: 'red' }}>{error}</p>}
          {user2Messages.length > 0 ? (
            user2Messages.map((msg, index) => <p key={index} style={{ color: 'black' }}>{msg}</p>)
          ) : (
            <p>No messages found.</p>
          )}
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'space-evenly',
    alignItems: 'flex-start',
    padding: '20px',
    backgroundColor: '#f4f4f4',
    minHeight: '100vh',
    gap: '20px',
  },
  userBox: {
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '20px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    width: '40%',
  },
  textarea: {
    width: '100%',
    height: '100px',
    padding: '10px',
    marginBottom: '10px',
    border: '1px solid #ccc',
    borderRadius: '4px',
  },
  button: {
    backgroundColor: '#007bff',
    color: 'white',
    padding: '10px',
    width: '100%',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    marginBottom: '10px',
  },
  messages: {
    backgroundColor: '#f9f9f9',
    color: 'black', // Added black font color for the message box
    padding: '10px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    minHeight: '100px',
    whiteSpace: 'pre-wrap',
  },
};

export default App;
