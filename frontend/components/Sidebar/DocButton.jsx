export default function DocButton({document, index, handleActiveDoc}) {
    return (
        // Display button for document, if clicked make active
        <button key={index} onClick={() => handleActiveDoc(document.fileURL)}>{document.fileName}</button>
    )
}