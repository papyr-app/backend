import axiosInstance from '@api/instance';
import { UpdatePDFDocument } from '@customTypes/pdf_document';

export const getDocument = async (documentId: string) => {
  const response = await axiosInstance.get(`/documents/${documentId}`);
  return response.data;
};

export const downloadDocument = async (documentId: string) => {
  const response = await axiosInstance.get(`/documents/${documentId}/download`, {
    responseType: 'arraybuffer',
  });
  return response.data;
};

export const createDocument = async (formData: FormData) => {
  const response = await axiosInstance.post('/documents', formData);
  return response.data;
};

export const updateDocument = async (documentId: string, updateData: UpdatePDFDocument) => {
  const response = await axiosInstance.patch(`/documents/${documentId}`, updateData);
  return response.data;
};

export const deleteDocument = async (documentId: string) => {
  const response = await axiosInstance.delete(`/documents/${documentId}`);
  return response.data;
};

export const addCollaborator = async (documentId: string, email: string) => {
  const response = await axiosInstance.post(`/documents/${documentId}/add_collaborator`, { email });
  return response.data;
};

export const removeCollaborator = async (documentId: string, email: string) => {
  const response = await axiosInstance.post(`/documents/${documentId}/remove_collaborator`, { email });
  return response.data;
};

export const getShareToken = async (documentId: string) => {
  const response = await axiosInstance.get(`/documents/${documentId}/share`);
  return response.data;
};

export const useShareToken = async (shareToken: string) => {
  const response = await axiosInstance.post(`/documents/share/${shareToken}`);
  return response.data;
};
