import axiosInstance from '@api/instance';
import { LoginUser, RegisterUser } from '@customTypes/user';

export const register = async (userData: RegisterUser) => {
    const response = await axiosInstance.post('/auth/register', userData);
    return response.data;
};

export const login = async (credentials: LoginUser) => {
    const response = await axiosInstance.post('/auth/login', credentials);
    return response.data;
};
