import axiosInstance from '@api/instance';
import { UpdateUser } from '@customTypes/user';

export const getUser = async () => {
  const response = await axiosInstance.get('/users');
  return response.data;
};

export const updateUser = async (userData: UpdateUser) => {
  const response = await axiosInstance.patch('/users', userData);
  return response.data;
};

export const getUserDocuments = async () => {
  const response = await axiosInstance.get('/users/documents');
  return response.data;
};
