export default function Upload({handleUpload}) {
    // Citation for the following function:
    // Date: 04/15/2026
    // Adapted from:
    // Source URL: https://www.xjavascript.com/blog/how-get-get-file-name-in-file-chooser-in-react/
    const uploadFile = (e) => {
        handleUpload({
            fileName: e.target.files[0].name, // Set name of file
            fileURL: URL.createObjectURL(e.target.files[0]) // Create a URL for the file path
        }
        );
  };
    return (
        <>
            <div className="upload-container">
            <form>
                {/* Citation for the following code:
                Date: 04/15/2026
                Adapted from:
                Source URL: https://stackoverflow.com/questions/572768/styling-an-input-type-file-button */}
                <label htmlFor="file-upload" className="custom-file-upload">
                    <i className="fa-solid fa-arrow-up-from-bracket"></i>
                    Upload
                </label>
                    <input accept="application/pdf, .pdf" id="file-upload" type="file" onChange={uploadFile}/>
            </form>
            </div>
        </>
    )
}
