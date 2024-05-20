import axios from 'axios';
import { CreateInvitation } from '@customTypes/invitation';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const getInvitation = async (token: string, invitationId: string) => {
  const response = await axios.get(`${API_URL}/invitation/${invitationId}`, {
    headers: { Authorization: token },
  });
  return response.data;
};

export const getSentInvitations = async (token: string) => {
  const response = await axios.get(`${API_URL}/invitation/sent`, {
    headers: { Authorization: token },
  });
  return response.data;
};

export const getReceivedInvitations = async (token: string) => {
  const response = await axios.get(`${API_URL}/invitation/received`, {
    headers: { Authorization: token },
  });
  return response.data;
};

export const createInvitation = async (token: string, invitationData: CreateInvitation) => {
  const response = await axios.post(`${API_URL}/invitation/invite`, invitationData, {
    headers: { Authorization: token },
  });
  return response.data;
};

export const acceptInvitation = async (token: string, invitationId: string) => {
  const response = await axios.post(`${API_URL}/invitation/accept`, { invitation_id: invitationId }, {
    headers: { Authorization: token },
  });
  return response.data;
};
