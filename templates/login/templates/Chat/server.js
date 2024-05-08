const express = require("express");
const app = express();
const http = require("http").createServer(app);
const socketIO = require("socket.io")(http, {
    cors: {
        origin: "*"
    }
});
const mysql = require("mysql");

const connection = mysql.createConnection({
    host: "localhost",
    port: 3306,
    user: "root",
    password: "", // Enter your MySQL password here
    database: "futurefarm hub"
});

connection.connect(function (error) {
    if (error) {
        console.log("Database error: " + error);
    } else {
        console.log("Database connected");
    }
});

const users = {};

socketIO.on("connection", function (socket) {
    console.log("User connected:", socket.id);

    socket.on("connected", function (userId) {
        users[userId] = socket.id;
        console.log("User connected:", userId);
    });

    socket.on("disconnect", function () {
        // Remove disconnected user from the users object
        const userId = Object.keys(users).find(key => users[key] === socket.id);
        delete users[userId];
        console.log("User disconnected:", userId);
    });




    socket.on("sendEvent", function (data) {
        const receiverId = data.userId;
        const senderId = data.myId;
        const message = data.message;

        // Debugging: Print senderId and receiverId
        console.log("Sender ID:", senderId);
        console.log("Receiver ID:", receiverId);

        // Retrieve sender's name from the database
        const senderQuery = "SELECT id, username FROM users WHERE id = ?";
        connection.query(senderQuery, [senderId], function (error, senderResults) {
            if (error) {
                console.error("Error retrieving sender's name:", error);
                return;
            }

            // Retrieve receiver's name from the database
            const receiverQuery = "SELECT id, username FROM users WHERE id = ?";
            connection.query(receiverQuery, [receiverId], function (error, receiverResults) {
                if (error) {
                    console.error("Error retrieving receiver's name:", error);
                    return;
                }

                // Check if sender and receiver data are found
                if (senderResults.length === 1 && receiverResults.length === 1) {
                    const senderName = senderResults[0].username;
                    const receiverName = receiverResults[0].username;

                    // Debugging: Print sender and receiver names
                    console.log("Sender:", senderName);
                    console.log("Receiver:", receiverName);



                    // Emit the message data to the receiver's socket

                    connection.query("SELECT id FROM conversations WHERE (user_id_1 = ? AND user_id_2 = ?) OR (user_id_1 = ? AND user_id_2 = ?)", [data.userId, data.myId, data.myId, data.userId], function (error, conversations) {
                        if (conversations && conversations.length > 0) {
                            var conversation_id = conversations[0].id;
                            // Conversation already exists, proceed to insert the message
                            connection.query("INSERT INTO messages (conversation_id, sender_id, receiver_id, message) VALUES (?, ?, ?, ?)", [conversation_id, data.myId, data.userId, data.message], function (error, result) {
                                if (error) {
                                    console.error("Error storing message:", error);
                                } else {
                                    console.log("Message stored successfully:", result);
                                }
                                // Inside the "sendEvent" event handler
                                socketIO.to(users[receiverId]).emit("messageReceived", {
                                    sender: senderName,
                                    receiver: receiverName,
                                    message: message
                                });

                                console.log("Conversation ID"+conversation_id);
                            });
                        } else {
                        //if they dont have conversation ID

                        }
                    });

                } else {
                    console.log("Sender's or receiver's name not found.");
                }
            });
        });
    });






    function saveMessage(conversationId, senderId, receiverId, message) {
        const insertMessageQuery = "INSERT INTO messages (conversation_id, sender_id, receiver_id, message) VALUES (?, ?, ?, ?)";
        connection.query(insertMessageQuery, [conversationId, senderId, receiverId, message], function (error, results) {
            if (error) {
                console.error("Error saving message:", error);
                return;
            }
            console.log("Message saved successfully.");
        });
    }

    function createConversationAndSaveMessage(senderId, receiverId, message) {
        // Create a new conversation between sender and receiver
        const createConversationQuery = "INSERT INTO conversations (user_id_1, user_id_2) VALUES (?, ?)";
        connection.query(createConversationQuery, [senderId, receiverId], function (error, results) {
            if (error) {
                console.error("Error creating conversation:", error);
                return;
            }
            const conversationId = results.insertId;
            // Save the message with the newly created conversation ID
            saveMessage(conversationId, senderId, receiverId, message);
        });
    }

});

http.listen(process.env.PORT || 3000, function () {
    console.log("Server is started.");
});
