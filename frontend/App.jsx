import Sidebar from "./components/Sidebar/Sidebar.jsx"
import Main from "./components/Main/Main.jsx"
import Chat from "./components/Chat/Chat.jsx"
import { useState } from 'react';
import './App.css'

function App() {
  const [documents, setDocuments] = useState([])
  const [messages, setMessages] = useState([])
  const [activeDoc, setActiveDoc] = useState(null)

  function handleActiveDoc (newDocument) {
    setActiveDoc(newDocument);
  };

  function handleUpload (uploadedDoc) {
    setDocuments([...documents, uploadedDoc]);
    // If its the first document uploaded, set as active doc
    if (documents.length == 0) {
      handleActiveDoc(uploadedDoc.fileURL)
    }
  };

  function handleMessages (newMessage) {
    setMessages([...messages, <div className="chat-bubbles user-question">{newMessage}</div>]);
    // Wait then display typing dots
    setTimeout(function() {
            setMessages([...messages, <div className="chat-bubbles user-question">{newMessage}</div>, <div className="chat-bubbles ai-answer"><div className="loading">...</div></div>]);
        }, 1000);
    // Wait then display AI message
    setTimeout(function() {
            setMessages([...messages, <div className="chat-bubbles user-question">{newMessage}</div>, <div className="chat-bubbles ai-answer">AI Reply Here</div>]);
        }, 3000);
  };

  return (
    <>
      <header>
        <h1>Ask My Documents</h1>
      </header>
      <main>
          <div><Sidebar 
                documents={documents}
                handleActiveDoc={handleActiveDoc}
                handleUpload={handleUpload}
          /></div>
          <div><Main 
                activeDoc={activeDoc}
          /></div>
          <div><Chat 
                messages={messages}
                handleMessages={handleMessages}
          /></div>
      </main>
    </>
  )
}

export default App
