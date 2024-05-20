import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '@api/index';
import PDFViewer from '@components/pdf_viewer/PDFViewer';

export default function Workspace() {
    const [fileBytes, setFileBytes] = useState<ArrayBuffer | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const { documentId } = useParams<{ documentId: string }>();

    useEffect(() => {
        async function fetchFile() {
            try {
                const token = localStorage.getItem('token');
                if (token && documentId) {
                    const bytes = await api.document.downloadDocument(token, documentId);
                    setFileBytes(bytes);
                } else {
                    setError('User is not authenticated');
                }
            } catch (err) {
                setError('Failed to fetch file');
            } finally {
                setLoading(false);
            }
        }

        fetchFile();
    }, [documentId]);

    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            {fileBytes && !loading ? <PDFViewer fileBytes={fileBytes}/> : <div>Loading...</div>}
        </div>
    )
}
