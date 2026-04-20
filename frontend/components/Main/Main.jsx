import DocumentView from "./DocumentView.jsx"
import './Main.css'

export default function Main({activeDoc}) {
  return (
    <>
      <div className="main-container">
        <DocumentView 
          activeDoc = {activeDoc}
        />
      </div>
    </>
  )
}