import React  from 'react';
import { Document, Page } from 'react-pdf'
import './pdf.worker';

export default function PDFViewer(props: { fileBytes: ArrayBuffer }) {
    return (
        <Document file={{ data: props.fileBytes }}><Page pageNumber={1} /></Document>
    )
};
