import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const register = async (userData: {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  password: string;
}) => {
  const response = await axios.post(`${API_URL}/auth/register`, userData);
  return response.data;
};

export const login = async (credentials: {
  username: string;
  password: string;
}) => {
  const response = await axios.post(`${API_URL}/auth/login`, credentials);
  return response.data;
};

