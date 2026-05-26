import DocumentView from "./DocumentView.jsx"
import './main.css'

export default function Main({activeDoc}) {
  return (
    <>
      <div>
        <DocumentView 
          activeDoc = {activeDoc}
        />
      </div>
    </>
  )
}