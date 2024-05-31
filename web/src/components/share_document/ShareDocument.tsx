import React, { useState } from "react";
import { SlDocs } from "react-icons/sl";
import { PDFDocument } from "@customTypes/pdf_document";
import { generateUrl } from "@utils";
import './ShareDocument.scss';

interface ShareDocumentProps {
    document: PDFDocument
}

export default function ShareDocument(props: ShareDocumentProps) {
    const [email, setEmail] = useState<string>('');

    return (
        <div className="share-component">
            <div className="share-link">
                <input
                    className="share-input"
                    type="text"
                    value={generateUrl('localhost:3000/share', {
                        token: props.document.share_token
                    })}
                    readOnly
                />
                <button className="button-secondary">
                    <SlDocs className='icon' />
                    Copy
                </button>
            </div>
            <div className="share-email">
                <input
                    type="email"
                    placeholder="Enter email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="email-input"
                />
                <button className="button-secondary">
                    Share via Email
                </button>
            </div>
        </div>
    )
}
