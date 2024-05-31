import React, { useState, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';
import { CreatePDFDocument } from '@customTypes/pdf_document';
import api from '@api/index';
import './UploadDocument.scss';

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
            // TODO - notify success
            await api.document.createDocument(data);
        } catch (error) {
            console.error('Error uploading document:', error);
        }
    };

    return (
        <div className="upload-container">
            <h1>Upload PDF Document</h1>
            <form className="form" onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="title">Title:</label>
                    <input
                        type="text"
                        id="title"
                        value={formData.title}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="description">Description:</label>
                    <input
                        id="description"
                        value={formData.description}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="file">Upload PDF:</label>
                    <input
                        type="file"
                        id="file"
                        accept="application/pdf"
                        onChange={handleFileChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <button className="button-primary" type="submit">Upload Document</button>
                </div>
            </form>
        </div>
    );
};
