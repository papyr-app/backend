import React, { useState } from "react";
import { SlDocs } from "react-icons/sl";
import { PDFDocument } from "@customTypes/pdf_document";
import './ShareDocument.scss';

interface ShareDocumentProps {
    document: PDFDocument
}

export default function ShareDocument(props: ShareDocumentProps) {
    return (
        <div className="share-component">
            <div className="share-link">
                <input
                    className="share-input"
                    type="text"
                    value={`localhost:3000/share/${props.document.share_token}`}
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
                    value={""}
                    onChange={() => null}
                    className="email-input"
                />
                <button className="button-secondary">
                    Share via Email
                </button>
            </div>
        </div>
    )
}
