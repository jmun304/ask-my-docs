import { useState } from 'react';

export default function ChatInput({handleMessages}) {
    // Citation for the following code:
    // Date: 04/14/2026
    // Adapted from:
    // Source URL: https://www.geeksforgeeks.org/reactjs/react-onsubmit-event/
    const [value, setValue] = useState("");

    // Call handleMessages with input value
    function handleSubmit(e) {
        e.preventDefault();
        handleMessages(value)
        setValue("")
    }

    // Set value to input value
    function handleChange(e) {
        setValue(e.target.value);
    }

    return (
        <div className="chat-input-container">
            <form onSubmit={handleSubmit}>
                <label>
                    <div className="chat-inputs">
                        <input type="text" placeholder="Type your question here" value={value} onInput={handleChange}/>
                        <button aria-label="Submit" type="submit"><i className="fa-solid fa-paper-plane"></i></button>
                    </div>
                </label>
            </form>
        </div>
    )
}