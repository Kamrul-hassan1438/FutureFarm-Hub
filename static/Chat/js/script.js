// Function to get URL parameters
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

// Get user ID from URL query parameters
var userId = getParameterByName('userId');
console.log(userId)

// Connect to Socket.IO server
var socketIO = io("http://localhost:3000");
socketIO.emit("connected", userId);

// Handle received messages
socketIO.on("messageReceived", function (data) {
    // Find the chat box for the sender
    const chatBox = document.querySelector(`.chat-box[data-username="${data.sender}"] .messages`);
    console.log("Chat Box Element:", chatBox); // Log the chat box element
    if (chatBox) {
        // Determine if the message is sent by the current user or received from another user
        const isSentByCurrentUser = data.sender === userId;

        // Create a new list item for the message
        const li = document.createElement('li');
        li.textContent = `${data.message}`;

        // Add appropriate class based on whether the message is sent or received
        if (isSentByCurrentUser) {
            li.classList.add('sent');
        } else {
            li.classList.add('received');
        }

        // Append the message to the chat box
        chatBox.appendChild(li);
    }
});


// Add event listener for the send button
document.querySelectorAll('.sendButton').forEach(button => {
    button.addEventListener('click', function () {
        // Get the recipient user ID and message input value
        const receiverId = this.getAttribute('data-receiver-id');
        const messageInput = this.parentElement.querySelector('.messageInput').value;

        // Emit the sendEvent event with the message data
        socketIO.emit("sendEvent", {
            "myId": userId,
            "userId": receiverId,
            "message": messageInput
        });
        const chatBox = document.querySelector(`.chat-box[data-receiver-id="${receiverId}"] .messages`);
        const li = document.createElement('li');
        li.textContent = `${messageInput}`;
        if (chatBox) {
            // Append the message to the chat box
            chatBox.appendChild(li);
        }

        // Clear the message input after sending
        this.parentElement.querySelector('.messageInput').value = '';


    });
});

// Toggle display of chat box
document.querySelectorAll('.toggleButton').forEach(button => {
    button.addEventListener('click', function () {
        const chatBox = this.parentElement.querySelector('.chat-box');
        chatBox.classList.toggle('show');
    });
});

// Add event listener for the search button
document.getElementById('searchButton').addEventListener('click', function () {
    const searchInput = document.getElementById('searchInput').value;
    if (searchInput.trim() !== '') {
        // Send AJAX request to search for users
        fetch('/search_users?userId=' + userId, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'searchQuery': searchInput
            })
        })
            .then(response => response.json())
            .then(data => {
                // Clear previous search results
                const userList = document.querySelector('.user-list');
                userList.innerHTML = '';

                // Display search results
                data.forEach(user => {
                    const userCard = `
                        <div class="user-card">
                            <div class="user-details">
                                <h3>${user.username}</h3>
                                <p>ID: ${user.id}</p>
                            </div>
                            <div class="user-actions">
                                <button class="startConversationButton" data-user-id="${user.id}">Start Conversation</button>
                            </div>
                            <div class="chat-container">
                                <div class="chat-box" data-username="${user.username}">
                                    <div class="chat-header">
                                        <h3>${user.username}</h3>
                                    </div>
                                    <ul class="messages">
                                        <!-- Received messages will be appended here -->
                                    </ul>
                                </div>
                                <div class="chat-inputs" style="display: none;">
                                    <input type="text" class="messageInput" placeholder="Type your message..." required>
                                    <button class="sendButton" data-receiver-id="${user.id}">Send</button>
                                </div>
                            </div>
                        </div>
                    `;
                    userList.innerHTML += userCard;
                });

                // Add event listeners for "Start Conversation" buttons
                document.querySelectorAll('.startConversationButton').forEach(button => {
                    button.addEventListener('click', function () {
                        const receiverId = this.getAttribute('data-user-id');
                        const senderId = userId; // Get sender ID from the surrounding scope

                        // Send AJAX request to start conversation
                        fetch('/start_conversation', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                sender_id: senderId,
                                receiver_id: receiverId
                            })
                        })
                            .then(response => response.json())
                            .then(data => {
                                const chatBox = this.parentElement.querySelector('.chat-box');
                                chatBox.dataset.conversationId = data.conversation_id;
                                alert('Conversation started with user ID: ' + receiverId);
                            })
                            .catch(error => {
                                console.error('Error starting conversation:', error);
                                alert('Error starting conversation');
                            });
                    });
                });
            })
            .catch(error => {
                console.error('Error searching for users:', error);
            });
    }
});





// Add event listener to the document body to hide chat container when clicking outside
document.body.addEventListener('click', function (event) {

    // Check if the clicked element is outside the chat container or its related elements
    if (!event.target.closest('.chat-container')) {
        // Hide all chat containers
        document.querySelectorAll('.chat-container').forEach(container => {
            container.querySelector('.chat-box').style.display = 'none'; // Hide chat box
            container.querySelector('.chat-inputs').style.display = 'none'; // Hide text input bar
            const toggleButton = container.querySelector('.toggleButton');
            toggleButton.textContent = 'Show Chat'; // Update toggle button text
        });
    }
});


// Add event listeners to toggle buttons
document.querySelectorAll('.toggleButton').forEach(button => {
    button.addEventListener('click', function () {
        // Toggle the display of chat inputs and chat box
        const chatInputs = this.parentElement.querySelector('.chat-inputs');
        const chatBox = this.parentElement.querySelector('.chat-box');
        if (chatInputs.style.display === 'none') {
            chatInputs.style.display = 'block';
            chatBox.style.display = 'block';
            this.textContent = 'Hide Chat'; // Update button text
        } else {
            chatInputs.style.display = 'none';
            chatBox.style.display = 'none';
            this.textContent = 'Show Chat'; // Update button text
        }
    });
});


