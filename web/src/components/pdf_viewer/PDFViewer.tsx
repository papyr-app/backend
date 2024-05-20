import React, { useEffect, useState } from 'react';
import { Worker, Viewer } from '@react-pdf-viewer/core';
import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout';
import '@react-pdf-viewer/core/lib/styles/index.css';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';

export default function PDFViewer(props: {fileBytes: ArrayBuffer}) {
    const [fileUrl, setFileUrl] = useState<string | null>(null);
    const defaultLayoutPluginInstance = defaultLayoutPlugin();

    useEffect(() => {
        if (props.fileBytes) {
            const blob = new Blob([props.fileBytes], { type: 'application/pdf' });
            const url = URL.createObjectURL(blob);
            setFileUrl(url);

            return () => {
                URL.revokeObjectURL(url);
            };
        }
    }, [props.fileBytes]);

    return (
        <Worker workerUrl={`https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js`}>
            <div style={{ height: '750px' }}>
                {fileUrl ? <Viewer fileUrl={fileUrl} plugins={[defaultLayoutPluginInstance]} /> : null}
            </div>
        </Worker>
    )
};
