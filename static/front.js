// static/front.js

document.addEventListener('DOMContentLoaded', () => {
    // --- Get all the necessary HTML elements by their IDs ---
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    
    const rightSidebar = document.getElementById('right-sidebar');
    const openSidebarBtn = document.getElementById('open-sidebar-btn');
    const closeSidebarBtn = document.getElementById('close-sidebar-btn');

    // "Under the Hood" display elements
    const userQueryEmbeddingEl = document.getElementById("user-query-embedding");
    const matchedKbEmbeddingEl = document.getElementById("matched-kb-embedding");
    const matchedQuestionEl = document.getElementById("matched-question");
    const similarityScoreEl = document.getElementById("similarity-score");
    // This flag will help us clear the initial welcome message
    let isFirstMessage = true;

    // --- Main function to handle sending a message ---
    const sendMessage = async () => {
        const message = messageInput.value.trim();
        if (message === '') return; // Don't send empty messages

        // If it's the first message, clear the welcome screen
        if (isFirstMessage) {
            chatMessages.innerHTML = '';
            isFirstMessage = false;
        }

        // Display the user's message immediately
        displayUserMessage(message);
        messageInput.value = ''; // Clear the input field

        // Display a typing indicator for the bot
        const typingIndicator = displayTypingIndicator();

        try {
            // Send the message to the Flask backend
            const response = await fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message }),
            });

            const data = await response.json();

            // Remove the typing indicator
            chatMessages.removeChild(typingIndicator);
            
            // Display the bot's response
            displayBotMessage(data.response);

        } catch (error) {
            console.error('Error:', error);
            chatMessages.removeChild(typingIndicator); // Remove indicator on error too
            displayBotMessage('Sorry, an error occurred. Please try again.');
        }
    };

    // --- Event Listeners ---
    // 1. Listen for clicks on the send button
    sendButton.addEventListener('click', sendMessage);

    // 2. Listen for 'Enter' key press in the textarea
    messageInput.addEventListener('keydown', (event) => {
        // Send message on Enter, but allow new lines with Shift+Enter
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Prevent default new line on Enter
            sendMessage();
        }
    });

    // --- Sidebar Toggle Logic ---
    openSidebarBtn.addEventListener('click', () => {
        rightSidebar.classList.remove('translate-x-full');
        openSidebarBtn.classList.add("opacity-0");
    });

    closeSidebarBtn.addEventListener('click', () => {
        rightSidebar.classList.add('translate-x-full');
        openSidebarBtn.classList.add("opacity-0");
    });

    // --- Helper functions to create message bubbles ---
    function displayUserMessage(message) {
        const userMessageHTML = `
            <div class="flex items-start gap-4 justify-end">
                <div class="bg-blue-500 rounded-lg p-3 max-w-lg">
                    <p>${message}</p>
                </div>
                <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center font-bold text-sm flex-shrink-0">
                    You
                </div>
            </div>
        `;
        chatMessages.innerHTML += userMessageHTML;
        scrollToBottom();
    }
    
    function displayBotMessage(message) {
        // Replace newline characters with <br> tags for proper formatting
        const formattedMessage = message.replace(/\n/g, '<br>');

        const botMessageHTML = `
            <div class="flex items-start gap-4">
                <div class="w-8 h-8 rounded-full bg-emerald-500 flex items-center justify-center font-bold text-sm flex-shrink-0">
                    SB
                </div>
                <div class="bg-[#40414f] rounded-lg p-3 max-w-lg">
                    <p>${formattedMessage}</p>
                </div>
            </div>
        `;
        chatMessages.innerHTML += botMessageHTML;
        scrollToBottom();
    }

    function displayTypingIndicator() {
        const typingIndicatorHTML = `
            <div class="flex items-start gap-4" id="typing-indicator">
                <div class="w-8 h-8 rounded-full bg-emerald-500 flex items-center justify-center font-bold text-sm flex-shrink-0">
                    SB
                </div>
                <div class="bg-[#40414f] rounded-lg p-3 max-w-lg">
                    <div class="typing-dots">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
        `;
        chatMessages.innerHTML += typingIndicatorHTML;
        scrollToBottom();
        return document.getElementById('typing-indicator');
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});