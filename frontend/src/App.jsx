import Main from "./components/Main/Main.jsx"
import Chat from "./components/Chat/Chat.jsx"
import { useState } from 'react';
import Upload from "./components/Upload/Upload.jsx";

function App() {
  const API = import.meta.env.VITE_API_URL;
  const [documents, setDocuments] = useState([])
  const [messages, setMessages] = useState([])
  const [activeDoc, setActiveDoc] = useState(null)

  function handleActiveDoc (newDocument) {
    setActiveDoc(newDocument);
  };

  function handleUpload (uploadedDoc) {
    setDocuments([...documents, uploadedDoc]);
    // Set new document as active doc
    handleActiveDoc(uploadedDoc.fileURL);
  };

  async function handleMessages(newMessage) {
    // 1. Show user question immediately
    setMessages(prev => [...prev, 
        <div className="chat-bubbles user-question">{newMessage}</div>
    ]);

    // 2. Show typing dots while waiting for API
    setMessages(prev => [...prev,
        <div className="chat-bubbles ai-answer">
            <div className="loading">...</div>
        </div>
    ]);

    try {
        // 3. Call backend query endpoint
        const response = await fetch(`${API}/query`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: newMessage })
        });

        const data = await response.json();

        // 4. Replace typing dots with real answer
        setMessages(prev => {
            const withoutDots = prev.slice(0, -1);  // remove last (dots)
            return [...withoutDots, 
                <div className="chat-bubbles ai-answer">{data.answer}</div>
            ];
        });

    } catch (error) {
        // 5. Handle errors
        setMessages(prev => {
            const withoutDots = prev.slice(0, -1);
            return [...withoutDots,
                <div className="chat-bubbles ai-answer">
                    Sorry, something went wrong. Please try again.
                </div>
            ];
        });
      }
  };
  
  return (
    <>
      <header>
        <h1>Ask My Documents</h1>
      </header>
      <main>
        <div className="left-container">
          <Upload
            handleUpload={handleUpload}
          />
          <Chat
            messages={messages}
            handleMessages={handleMessages}
          />
        </div>
        <div className="right-container">
          <Main activeDoc={activeDoc} />
        </div>
      </main>
    </>
  )
}




export default App
