import DocList from "./DocList.jsx"
import Upload from "./Upload.jsx"
import './sidebar.css'

export default function Sidebar({documents, activeDoc, handleActiveDoc, handleUpload}) {
  return (
    <>
      <div>
        <Upload 
          handleUpload={handleUpload}
        />
        <DocList 
          documents = {documents}
          activeDoc = {activeDoc}
          handleActiveDoc = {handleActiveDoc}
        />
      </div>
    </>
  )
}