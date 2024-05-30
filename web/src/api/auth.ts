import axios from 'axios';
import { LoginUser, RegisterUser } from '@customTypes/user';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const register = async (userData: RegisterUser) => {
    console.log(userData)
    const response = await axios.post(`${API_URL}/auth/register`, userData, { headers: { 'Content-Type': 'application/json' } });
    return response.data;
};

export const login = async (credentials: LoginUser) => {
    const response = await axios.post(`${API_URL}/auth/login`, credentials, { headers: { 'Content-Type': 'application/json' } });
    return response.data;
};

