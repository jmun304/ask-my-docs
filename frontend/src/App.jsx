import Sidebar from "./components/Sidebar/Sidebar.jsx"
import Main from "./components/Main/Main.jsx"
import Chat from "./components/Chat/Chat.jsx"
import { useState } from 'react';

function App() {
  const [documents, setDocuments] = useState([])
  const [messages, setMessages] = useState([])
  const [activeDoc, setActiveDoc] = useState(null)
  const [messageReply, setMessageReply] = useState(null)

  function handleActiveDoc (newDocument) {
    setActiveDoc(newDocument);
  };

  async function handleUpload (uploadedDoc) {
    // Citation for the following code:
    // Date: 05/19/2026
    // Adapted from:
    // Source URL: https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Sending_forms_through_JavaScript
    
    // Create a new FormData object and append the uploaded document
    const formData = new FormData();
    formData.append("file", uploadedDoc.file)

    try {
      const response = await fetch("http://127.0.0.1:8000", {
        method: "POST",
        body: formData,
      });
    } catch (e) {
        console.error(e);
    }
    setDocuments([...documents, uploadedDoc]);
    // Set new document as active doc
    handleActiveDoc(uploadedDoc.fileURL);
  };

  function handleMessages (newMessage) {
    setMessages([...messages, <div className="chat-bubbles user-question">{newMessage}</div>]);
    // Wait then display typing dots
    setTimeout(function() {
            setMessages([...messages, <div className="chat-bubbles user-question">{newMessage}</div>, <div className="chat-bubbles ai-answer"><div className="loading">...</div></div>]);
        }, 1000);
        
    try {
      const response = await fetch("http://127.0.0.1:8000", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: newMessage }),
      });

      const reply = await response.json();
      setMessageReply(reply)

    } catch (e) {
        console.error(e);
    }

    // Wait then display AI message
    setTimeout(function() {
            setMessages([...messages, <div className="chat-bubbles user-question">{messageReply}</div>, <div className="chat-bubbles ai-answer">AI Reply Here</div>]);
        }, 3000);
  };

  return (
    <>
      <header>
        <h1>Ask My Documents</h1>
      </header>
      <main>
          <div className="sidebar-container"><Sidebar 
                documents={documents}
                activeDoc={activeDoc}
                handleActiveDoc={handleActiveDoc}
                handleUpload={handleUpload}
          /></div>
          <div className="main-container"><Main 
                activeDoc={activeDoc}
          /></div>
          <div className="chat-container"><Chat 
                messages={messages}
                handleMessages={handleMessages}
          /></div>
      </main>
    </>
  )
}

export default App
