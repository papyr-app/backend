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
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            <div>
                <h2>My documents</h2>
                <ul>
                    {documents.map((doc) => (
                        <li key={doc._id}>
                            <p>{doc.title}</p>
                            <button onClick={() => goToDocument(doc._id)}>Edit/View</button>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};
