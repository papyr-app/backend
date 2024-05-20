import { PDFDocument } from "./pdf_document";
import { User } from "./user";

export interface Invitation {
    _id: string,
    document: PDFDocument;
    invited_by: User;
    invitee: User;
    expires_at: Date;
}

export interface CreateInvitation {
    email: string;
    document_id: string;
}
