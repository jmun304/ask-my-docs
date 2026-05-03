export default function DocButton({document, activeDoc, index, handleActiveDoc}) {
        // If button is active, use active-btn class
        // If button is clicked, make it the active button
        if (document.fileURL == activeDoc) {
            return <button className="active-btn" key={index} onClick={() => handleActiveDoc(document.fileURL)}>{document.fileName}</button>
        }
        else {
            return <button key={index} onClick={() => handleActiveDoc(document.fileURL)}>{document.fileName}</button>
        }
}