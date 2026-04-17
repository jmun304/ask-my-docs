export default function Messages({messages}) {
  return (
    <div className="scrollbar-container">
      <div className="messages-container">
          {/* Display each message in array */}
          {messages.map(message => 
            message
          )}
      </div>
    </div>
  )
}
