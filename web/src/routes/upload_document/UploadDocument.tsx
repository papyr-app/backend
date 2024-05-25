import React, { useState, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';
import { CreatePDFDocument } from '@customTypes/pdf_document';
import api from '@api/index';

export default function UploadDocument() {
    const [formData, setFormData] = useState<CreatePDFDocument>({
        title: '',
        description: '',
        file: null,
    });

    function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
        const { id, value } = e.target;
        setFormData((prevFormData) => ({
            ...prevFormData,
            [id]: value,
        }));
    };

    function handleFileChange(e: ChangeEvent<HTMLInputElement>) {
        const files = e.target.files;
        if (files && files.length > 0) {
            setFormData((prevData) => ({
                ...prevData,
                file: files[0],
            }));
        }
    };

    async function handleSubmit(e: FormEvent) {
        e.preventDefault();

        const data = new FormData();
        data.append('title', formData.title);
        data.append('description', formData.description || '');
        if (formData.file) {
            data.append('file', formData.file);
        }

        try {
            const token = localStorage.getItem('token');
            if (token) {
                console.log('uploading...');
                const response = await api.document.createDocument(token, data);
                console.log('Document uploaded successfully:', response.data);
            } else {
                console.log('No token');
            }
        } catch (error) {
            console.error('Error uploading document:', error);
        }

    };

    return (
        <div className="upload-document">
            <h1>Upload PDF Document</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="title">Title:</label>
                    <input
                        type="text"
                        id="title"
                        value={formData.title}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="description">Description:</label>
                    <input
                        id="description"
                        value={formData.description}
                        onChange={handleChange}
                    />
                </div>
                <div>
                    <label htmlFor="file">Upload PDF:</label>
                    <input
                        type="file"
                        id="file"
                        accept="application/pdf"
                        onChange={handleFileChange}
                        required
                    />
                </div>
                <button type="submit">Upload Document</button>
            </form>
        </div>
    );
};