import React from 'react';
import { PDFDocument } from '@customTypes/pdf_document';
import { SlShare, SlPencil } from 'react-icons/sl';
import { TreeNode } from '@customTypes/tree_node';

interface FileProps {
  doc: PDFDocument;
  handleShowEditModal?: (doc: PDFDocument) => void;
  handleShowShareModal?: (doc: PDFDocument) => void;
}

export function File({ doc, handleShowEditModal, handleShowShareModal }: FileProps) {
    return (
        <li className="document-item">
            <a className="document-link" href={`document/${doc._id}`}>{doc.title}</a>
            <p className="document-description">{doc.description}</p>
            <p className="document-status">Status: {doc.status}</p>
            <p className="document-owner">Owner: {doc.owner.first_name} {doc.owner.last_name} ({doc.owner.username})</p>
            <p className="document-created">Created at: {new Date(doc.created_at).toLocaleDateString()}</p>
            <p className="document-updated">Updated at: {new Date(doc.updated_at).toLocaleDateString()}</p>
            {doc.collaborators && doc.collaborators.length > 0 && (
                <p className="document-collaborators">Collaborators: {doc.collaborators.map(col => `${col.first_name} ${col.last_name}`).join(', ')}</p>
            )}
            <button className="button-secondary edit-button" >
                <SlPencil className="icon" /> Edit
            </button>
            <button className="button-secondary share-button" >
                <SlShare className="icon" /> Share
            </button>
        </li>
    );
}

export function Directory(treeNode: TreeNode) {
    return (
        <li>
            <div className="directory-name">{treeNode.name}</div>
            <ul>
                {treeNode.children.map(child => (
                    (child.isFile && child.doc) ?
                        <File key={child.doc._id} doc={child.doc} />
                        :
                        <Directory key={child.name} {...child} />
                ))}
            </ul>
        </li>
    );
}
