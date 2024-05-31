import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import api from '@api/index';

export default function GrantAccess() {
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();
    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const token = searchParams.get('token');

    useEffect(() => {
        const authorizeUser = async () => {
            try {
                if (token) {
                    await api.document.useShareToken(token);
                } else {
                    throw new Error('No share token provided.');
                }
            } catch (err) {
                setError('Failed to use share token');
                console.log(err);
            } finally {
                setLoading(false);
            }
        };

        authorizeUser();
    }, [token, navigate]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div className="authorize-access">
            <p>Authorizing access, please wait...</p>
        </div>
    );
}
