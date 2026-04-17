import ChatInput from "./ChatInput.jsx"
import Messages from "./Messages.jsx"
import './chat.css'

export default function Chat({messages, handleMessages}) {
return (
        <>
          <div className="chat-container">
            <div className="chat-top"><h2><i className="fa-regular fa-message"></i> Doc Chat</h2></div>
            <Messages 
              messages={messages}
            />
            <ChatInput 
              handleMessages={handleMessages}
            />
          </div>
        </>
  )
}