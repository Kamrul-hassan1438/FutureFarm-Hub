from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import pymysql
from flask_cors import CORS
import sys

app = Flask(__name__)
socketio = SocketIO(app)
CORS(app)

# Connect to MySQL
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='',
    database='message'
)

@app.route('/')
def user_id():
    return render_template('user_id.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return app.send_static_file('static/' + filename)


@app.route('/index')
def index():
    user_id = request.args.get('userId')
    
    # Fetch users involved in conversations with the specified user
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT u.id, u.username
        FROM users u
        JOIN (
            SELECT user_id_1 AS user_id FROM conversations WHERE user_id_2 = %s 
            UNION 
            SELECT user_id_2 AS user_id FROM conversations WHERE user_id_1 = %s
        ) AS c ON u.id = c.user_id
    """, (user_id, user_id))
    users = cursor.fetchall()
    print(users)
    
    return render_template('index.html', users=users, userId=user_id)




@app.route('/search_users', methods=['POST'])
def search_users():
    search_query = request.form['searchQuery']
    current_user_id = request.args.get('userId')

    # Fetch search results excluding the current user's username
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT id, username FROM users WHERE username LIKE %s AND id != %s", ('%' + search_query + '%', current_user_id))
    search_results = cursor.fetchall()
    
    return jsonify(search_results)





@app.route('/start_conversation', methods=['POST'])
def start_conversation():
    sender_id = request.json['sender_id']
    receiver_id = request.json['receiver_id']
    print("start_conversation")
    # Check if conversation already exists
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM conversations WHERE (user_id_1 = %s AND user_id_2 = %s) OR (user_id_1 = %s AND user_id_2 = %s)", 
                   (sender_id, receiver_id, receiver_id, sender_id))
    conversation = cursor.fetchone()
    
    if conversation:
        conversation_id = conversation[0]
    else:
        # Create a new conversation
        print("elseee")
        print(f"sender ID: {sender_id}")
        print(f"Receiver ID :{receiver_id}")
        cursor.execute("INSERT INTO conversations (user_id_1, user_id_2) VALUES (%s, %s)", (sender_id, receiver_id))
        conn.commit()
        conversation_id = cursor.lastrowid
    
    return jsonify({"conversation_id": conversation_id})



@app.route('/send_message', methods=['POST'])
def send_message():
    sender_id = request.form['sender_id']
    receiver_id = request.form['receiver_id']
    message = request.form['message']
    
    cursor = conn.cursor()
    # Fetch sender's name
    cursor.execute("SELECT username FROM users WHERE id = %s", (sender_id,))
    sender_name = cursor.fetchone()[0]
    
    cursor.execute("INSERT INTO messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)", (sender_id, receiver_id, message))
    conn.commit()
    
    # Emit the event with sender's name
    emit('messageReceived', {'sender_name': sender_name, 'message': message}, room=receiver_id)

    return jsonify({"success": True})

if __name__ == '__main__':
    port = sys.argv[1] if len(sys.argv) > 1 else 5000
    app.run(host='0.0.0.0', port=port)
