import { PDFDocument } from "./pdf_document";
import { User } from "./user";

export interface Comment {
    id: string,
    document: PDFDocument;
    user: User;
    text: string;
    created_at: Date;
    updated_at: Date;
}
