import axios from 'axios';
import { UpdatePDFDocument } from '@customTypes/pdf_document';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const getDocument = async (token: string, documentId: string) => {
  const response = await axios.get(`${API_URL}/documents/${documentId}`, {
    headers: { Authorization: token },
  });
  return response.data;
};

export const downloadDocument = async (token: string, documentId: string) => {
  const response = await axios.get(`${API_URL}/documents/${documentId}/download`, {
    headers: { Authorization: token },
    responseType: 'arraybuffer',
  });
  return response.data;
};

export const createDocument = async (token: string, formData: FormData) => {
  const response = await axios.post(`${API_URL}/documents`, formData, {
    headers: { Authorization: token },
  });
  return response.data;
};

export const updateDocument = async (token: string, documentId: string, updateData: UpdatePDFDocument) => {
  const response = await axios.patch(`${API_URL}/documents/${documentId}`, updateData, {
    headers: { Authorization: token },
  });
  return response.data;
};

export const deleteDocument = async (token: string, documentId: string) => {
  const response = await axios.delete(`${API_URL}/documents/${documentId}`, {
    headers: { Authorization: token },
  });
  return response.data;
};

export const addCollaborator = async (token: string, documentId: string, email: string) => {
  const response = await axios.post(`${API_URL}/documents/${documentId}/add_collaborator`, { email }, {
    headers: { Authorization: token },
  });
  return response.data;
};

export const removeCollaborator = async (token: string, documentId: string, email: string) => {
  const response = await axios.post(`${API_URL}/documents/${documentId}/remove_collaborator`, { email }, {
    headers: { Authorization: token },
  });
  return response.data;
};

export const getShareToken = async (token: string, documentId: string) => {
  const response = await axios.get(`${API_URL}/documents/${documentId}/share`, {
    headers: { Authorization: token },
  });
  return response.data;
};

export const useShareToken = async (token: string, documentId: string, shareToken: string) => {
  const response = await axios.post(`${API_URL}/documents/${documentId}/share/${shareToken}`, {}, {
    headers: { Authorization: token },
  });
  return response.data;
};
