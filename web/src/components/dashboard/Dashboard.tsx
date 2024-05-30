import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { PDFDocument } from '@customTypes/pdf_document';
import { SlShare, SlPencil, SlCloudUpload } from "react-icons/sl";
import api from '@api/index';
import './Dashboard.scss';

export default function Dashboard() {
    const [documents, setDocuments] = useState<PDFDocument[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
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

    function editDocument(id: string) {
        // TODO
    }

    function shareDocument(shareToken: string) {
        // TODO
    }

    function uploadDocument() {
        navigate(`/document/new`);
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
                        <button className='button-secondary' onClick={() => editDocument(doc._id)}>
                            <SlPencil className='icon' /> Edit
                        </button>
                        <button className='button-secondary' onClick={() => shareDocument(doc.share_token)}>
                            <SlShare className='icon' /> Share
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
}
