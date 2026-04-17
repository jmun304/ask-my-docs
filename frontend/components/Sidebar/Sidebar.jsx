import DocList from "./DocList.jsx"
import Upload from "./Upload.jsx"
import './sidebar.css'

export default function Sidebar({documents, handleActiveDoc, handleUpload}) {
  return (
    <>
      <div className="sidebar-container">
        <Upload 
          handleUpload={handleUpload}
        />
        <DocList 
          documents = {documents}
          handleActiveDoc = {handleActiveDoc}
        />
      </div>
    </>
  )
}