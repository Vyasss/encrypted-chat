import React, { useState } from 'react';

function UserMessageBox({ user, sendMessageEndpoint, receiveMessageEndpoint }) {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState('');

  const handleSendMessage = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/${sendMessageEndpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });
      if (!response.ok) {
        throw new Error('Message classified as unsafe. Not sent.');
      }
      setMessage('');
      alert(`Message sent from ${user}!`);
    } catch (err) {
      console.error('Error:', err);
      setError(err.message || 'Failed to send message.');
    }
  };

  const handleReceiveMessages = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/${receiveMessageEndpoint}`);
      const data = await response.json();
      setMessages(data.decrypted_messages || []);
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to retrieve messages.');
    }
  };

  return (
    <div style={styles.userBox}>
      <h2>{user}</h2>
      <textarea
        style={styles.textarea}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Enter your message..."
      />
      <button style={styles.button} onClick={handleSendMessage}>
        Send Message
      </button>
      <button style={styles.button} onClick={handleReceiveMessages}>
        Retrieve Messages
      </button>
      <div style={styles.messages}>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {messages.length > 0 ? messages.join('\n') : 'No messages found.'}
      </div>
    </div>
  );
}

const styles = {
  userBox: {
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '20px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    width: '45%',
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
    padding: '10px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    minHeight: '100px',
    whiteSpace: 'pre-wrap',
  },
};

export default UserMessageBox;
