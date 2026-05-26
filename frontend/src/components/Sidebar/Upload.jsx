export default function Upload({handleUpload}) {
    // Citation for the following function:
    // Date: 04/15/2026
    // Adapted from:
    // Source URL: https://www.xjavascript.com/blog/how-get-get-file-name-in-file-chooser-in-react/
    const uploadFile = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
    
        // 1. Create local URL for PDF display (keep existing behavior)
        const fileURL = URL.createObjectURL(file);
    
        // 2. Send file to backend
        const formData = new FormData();
        formData.append("file", file);
    
        try {
            const response = await fetch("http://localhost:8000/upload", {
                method: "POST",
                body: formData  // no Content-Type header needed — browser sets it automatically
            });
    
            const data = await response.json();
            console.log("Upload successful:", data);  // { message, num_chunks }
    
            // 3. Update parent state with both local URL and upload confirmation
            handleUpload({
                fileName: file.name,
                fileURL: fileURL,
                numChunks: data.num_chunks  // optional — useful for debugging
            });
    
        } catch (error) {
            console.error("Upload failed:", error);
            alert("Failed to upload PDF. Please try again.");
        }
    };
    return (
        <div className="upload-container">
            <form>
                {/* Citation for the following code:
                Date: 04/15/2026
                Adapted from:
                Source URL: https://stackoverflow.com/questions/572768/styling-an-input-type-file-button */}
                <label htmlFor="file-upload" className="custom-file-upload">
                    <i aria-hidden="true" className="fa-solid fa-arrow-up-from-bracket"></i>
                    Upload
                </label>
                <input accept="application/pdf, .pdf" id="file-upload" type="file" onChange={uploadFile}/>
            </form>
        </div>
    )
}