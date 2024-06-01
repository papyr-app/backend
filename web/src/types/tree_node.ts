import { PDFDocument } from "./pdf_document";

export interface TreeNode {
  name: string;
  children: TreeNode[];
  isFile?: boolean;
  doc?: PDFDocument;
}
