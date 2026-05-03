import DocButton from "./DocButton.jsx"

export default function DocList({documents, activeDoc, handleActiveDoc}) {
  return (
    <>
      <div className="buttons-container">
        {/* Display a button for each document */}
        {documents.map((document, index) => 
          <DocButton
            key = {index}
            document = {document}
            activeDoc = {activeDoc}
            handleActiveDoc = {handleActiveDoc}
          />
        )}
      </div>
    </>
  )
}