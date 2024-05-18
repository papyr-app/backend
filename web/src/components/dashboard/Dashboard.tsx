import React, { useState, useEffect } from 'react';
import api from '@api/index';
import { PDFDocument } from '@customTypes/pdf_document';

export default function Dashboard() {
    const [documents, setDocuments] = useState<PDFDocument[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
       async function fetchDocuments() { 
            try {
                const token = localStorage.getItem('token');
                if (token) {
                    const data = await api.user.getUserDocuments(token);
                    setDocuments(data);
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

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    const half = Math.ceil(documents.length / 2);
    const firstColumn = documents.slice(0, half);
    const secondColumn = documents.slice(half);

    return (
        <div>
            <div>
                <h2>Column 1</h2>
                <ul>
                    {firstColumn.map((doc) => (
                        <li key={doc.id}>{doc.title}</li>
                    ))}
                </ul>
            </div>
            <div>
                <h2>Column 2</h2>
                <ul>
                    {secondColumn.map((doc) => (
                        <li key={doc.id}>{doc.title}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
};
