// Citation for the following code:
// Date: 04/16/2026
// Adapted from:
// Source URL: https://www.npmjs.com/package/react-pdf

import { useState } from 'react';
import { Document, Page } from 'react-pdf';
import { pdfjs } from 'react-pdf';
import 'react-pdf/dist/Page/TextLayer.css';
import 'react-pdf/dist/Page/AnnotationLayer.css';

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();

export default function DocumentView({activeDoc}) {
    const [numPages, setNumPages] = useState();
    const [pageNumber, setPageNumber] = useState(1);

    // Get total number of pages of PDF
    function onDocumentLoadSuccess({numPages}){
        setNumPages(numPages);
    }

    // Move PDF backwards one page if not on the first page
    function changeBack() {
        if (pageNumber === 1) {
            setPageNumber(pageNumber)
        } else {
            setPageNumber(pageNumber - 1)
        }
    }

    // Move PDF forwards one page if not on the last page
    function changeForward() {
        if (pageNumber === numPages) {
            setPageNumber(pageNumber)
        } else {
            setPageNumber(pageNumber + 1)
        }
    }

    return (
        <>
            <div className="doc-nav-container">
                <button aria-label="Previous Page" onClick={changeBack}><i className="fa-solid fa-angle-left"></i></button>
                <button aria-label="Next Page" onClick={changeForward}><i className="fa-solid fa-angle-right"></i></button>
            </div>
            <div className="document-container">
                <Document file={activeDoc} onLoadSuccess={onDocumentLoadSuccess}>
                    <Page pageNumber={pageNumber} />
                </Document>
            </div>
        </>
    )
}