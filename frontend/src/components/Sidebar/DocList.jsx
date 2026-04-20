import DocButton from "./DocButton.jsx"

export default function DocList({documents, handleActiveDoc}) {
  return (
    <>
      <div className="buttons-container">
        {/* Display a button for each document */}
        {documents.map((document, index) => 
          <DocButton
            key = {index}
            document = {document}
            handleActiveDoc = {handleActiveDoc}
          />
        )}
      </div>
    </>
  )
}