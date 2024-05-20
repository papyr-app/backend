import axios from 'axios';
import { UpdateUser } from '@customTypes/user';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const getUser = async (token: string) => {
  const response = await axios.get(`${API_URL}/users`, {
    headers: { Authorization: token },
  });
  return response.data;
};

export const updateUser = async (token: string, userData: UpdateUser) => {
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
