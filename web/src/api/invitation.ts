import axiosInstance from '@api/instance';
import { CreateInvitation } from '@customTypes/invitation';

export const getInvitation = async (invitationId: string) => {
  const response = await axiosInstance.get(`/invitation/${invitationId}`)
  return response.data;
};

export const getSentInvitations = async () => {
  const response = await axiosInstance.get('invitation/sent');
  return response.data;
};

export const getReceivedInvitations = async () => {
  const response = await axiosInstance.get('/invitation/received');
  return response.data;
};

export const createInvitation = async (invitationData: CreateInvitation) => {
  const response = await axiosInstance.post('/invitation/invite', invitationData);
  return response.data;
};

export const acceptInvitation = async (invitationId: string) => {
  const response = await axiosInstance.post('/invitation/accept', { invitation_id: invitationId });
  return response.data;
};
