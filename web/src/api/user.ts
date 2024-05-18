import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const getUser = async (token: string) => {
  const response = await axios.get(`${API_URL}/users`, {
    headers: { Authorization: token },
  });
  return response.data;
};

export const updateUser = async (token: string, userData: { last_name: string }) => {
  const response = await axios.patch(`${API_URL}/users`, userData, {
    headers: { Authorization: token },
  });
  return response.data;
};

export const getUserDocuments = async (token: string) => {
  const response = await axios.get(`${API_URL}/users/documents`, {
    headers: { Authorization: token },
  });
  return response.data;
};
