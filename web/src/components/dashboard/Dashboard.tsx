import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { PDFDocument } from '@customTypes/pdf_document';
import { SlShare, SlPencil, SlCloudUpload, SlDocs } from "react-icons/sl";
import ShareDocument from '@components/share_document/ShareDocument';
import EditDocument from '@components/edit_document/EditDocument';
import Modal from '@components/modal/Modal';
import api from '@api/index';
import './Dashboard.scss';

export default function Dashboard() {
    const [documents, setDocuments] = useState<PDFDocument[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedDocument, setSelectedDocument] = useState<PDFDocument | null>(null);
    const [showShareModal, setShowShareModal] = useState<boolean>(false);
    const [showEditModal, setShowEditModal] = useState<boolean>(false);

    const navigate = useNavigate();

    useEffect(() => {
        async function fetchDocuments() {
            try {
                const token = localStorage.getItem('token');
                if (token) {
                    const data = await api.user.getUserDocuments(token);
                    setDocuments(data.data);
                } else {
                    setError('User is not authenticated');
                }
            } catch (err) {
                setError('Failed to fetch documents');
            } finally {
                setLoading(false);
            }
        };

        fetchDocuments();
    }, []);

    function uploadDocument() {
        navigate(`/document/new`);
    }

    function handleShowShareModal(document: PDFDocument) {
        setSelectedDocument(document);
        setShowShareModal(true);
    }

    function handleCloseShareModal() {
        setSelectedDocument(null);
        setShowShareModal(false);
    }

    function handleShowEditModal(document: PDFDocument) {
        setSelectedDocument(document);
        setShowEditModal(true);
    }

    function handleCloseEditModal() {
        setSelectedDocument(null);
        setShowEditModal(false);
    }

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div className="dashboard-container">
            <div className="dashboard-header">
                <h2>My Documents</h2>
                <button className='button-primary' onClick={uploadDocument}>
                    <SlCloudUpload className='icon' /> Upload Document
                </button>
            </div>
            <ul className="document-list">
                {documents.map((doc) => (
                    <li key={doc._id}>
                        <a href={`document/${doc._id}`}>{doc.title}</a>
                        <p>{doc.description}</p>
                        <p>Status: {doc.status}</p>
                        <p>Owner: {doc.owner.first_name} {doc.owner.last_name} ({doc.owner.username})</p>
                        <p>Created at: {new Date(doc.created_at).toLocaleDateString()}</p>
                        <p>Updated at: {new Date(doc.updated_at).toLocaleDateString()}</p>
                        {doc.collaborators && doc.collaborators.length > 0 && (
                            <p>Collaborators: {doc.collaborators.map(col => `${col.first_name} ${col.last_name}`).join(', ')}</p>
                        )}
                        <button className='button-secondary' onClick={() => handleShowEditModal(doc)}>
                            <SlPencil className='icon' /> Edit
                        </button>
                        <button className='button-secondary' onClick={() => handleShowShareModal(doc)}>
                            <SlShare className='icon' /> Share
                        </button>
                    </li>
                ))}
            </ul>

            <Modal show={showShareModal} onClose={handleCloseShareModal}>
                <h2>Share</h2>
                {selectedDocument && <ShareDocument document={selectedDocument} />}
            </Modal>

            <Modal show={showEditModal} onClose={handleCloseEditModal}>
                <h2>Edit</h2>
                {selectedDocument && <EditDocument document={selectedDocument} />}
            </Modal>
        </div>
    );
}
