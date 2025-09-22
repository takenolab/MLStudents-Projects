// src/components/NotFound.js
import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>404 - Page Not Found</h1>
      <p style={styles.message}>
        Oops! The page you're looking for does not exist.
      </p>
      <Link to="/" style={styles.link}>
        Go Back to Home
      </Link>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    textAlign: 'center',
  },
  title: {
    fontSize: '48px',
    color: '#333',
  },
  message: {
    fontSize: '18px',
    color: '#666',
  },
  link: {
    fontSize: '16px',
    color: '#007bff',
    textDecoration: 'none',
    marginTop: '20px',
  },
};

export default NotFound;
