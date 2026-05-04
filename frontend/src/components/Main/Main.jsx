import DocumentView from "./DocumentView.jsx"
import './Main.css'

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