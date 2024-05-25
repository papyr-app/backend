import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { PDFDocument } from '@customTypes/pdf_document';
import api from '@api/index';

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
                    console.log(data)
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

    function goToDocument(id: string) {
        navigate(`/document/${id}`);
    }

    function shareDocument(shareToken: string) {
        // TODO
        console.log(`Share document with token: ${shareToken}`);
    }

    function uploadDocument() {
        navigate(`/document/new`);
    }

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            <div>
                <h2>My Documents</h2>
                <button onClick={uploadDocument}>Upload Document</button>
                <ul>
                    {documents.map((doc) => (
                        <li key={doc._id} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px 0' }}>
                            <h3>{doc.title}</h3>
                            <p>{doc.description}</p>
                            <p>Status: {doc.status}</p>
                            <p>Owner: {doc.owner.first_name} {doc.owner.last_name} ({doc.owner.username})</p>
                            <p>Created at: {new Date(doc.created_at).toLocaleDateString()}</p>
                            <p>Updated at: {new Date(doc.updated_at).toLocaleDateString()}</p>
                            {doc.collaborators && doc.collaborators.length > 0 && (
                                <p>Collaborators: {doc.collaborators.map(col => `${col.first_name} ${col.last_name}`).join(', ')}</p>
                            )}
                            <button onClick={() => goToDocument(doc._id)}>Edit/View</button>
                            <button onClick={() => shareDocument(doc.share_token)}>Share</button>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}
