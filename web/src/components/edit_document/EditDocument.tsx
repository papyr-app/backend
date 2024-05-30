import React, { useState } from "react";
import { PDFDocument } from "@customTypes/pdf_document";
import './EditDocument.scss';

interface EditDocumentProps {
    document: PDFDocument
}

export default function ShareDocument(props: EditDocumentProps) {
    return (
        <div className="edit-component">
            Edit stuff goes here
        </div>
    )
}
