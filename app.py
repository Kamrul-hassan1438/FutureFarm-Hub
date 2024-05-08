from flask import Flask, render_template, request, session, redirect, url_for,jsonify
from db import connect_to_database,login_user_byID,farmer_register,Consultant_register,laborer_register,Retailer_register
import bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import sys
import pymysql
from db2 import conversations
from flask_socketio import SocketIO, emit
import json
from chat import get_response
import base64
from Mail import send_email



app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
socketio = SocketIO(app)

# Connect to MySQL
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='',
    database='futurefarm hub'
)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_id, username, is_active=True):
        self.id = user_id
        self.username = username
        self.is_active = is_active

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value


# Mock user loader function
@login_manager.user_loader
def load_user(user_id):
    # Replace this with your actual user loading logic
    return User(user_id, 'username')  # Assuming 'username' is a placeholder

#Home page
@app.route('/')
def index():
    # Connect to the database
    db_connection = connect_to_database()
    if db_connection:
        cursor = db_connection.cursor()

        # Query the database to get counts
        cursor.execute("SELECT COUNT(*) FROM farmers")
        farmer_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM laborers")
        laborer_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM buyers")
        buyer_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM admins")
        admin_count = cursor.fetchone()[0]


        # Pass counts to the HTML template
        return render_template('index.html', farmer_count=farmer_count, laborer_count=laborer_count, buyer_count=buyer_count, admin_count=admin_count)
    else:
        return "Failed to connect to the database."

@app.route('/Vission' ,methods=['GET'])
def visson():
    return render_template('Vission_Mession_Goal.html')

#for file render like CSS and js 
@app.route('/static/<path:filename>')
def serve_static(filename):
    return app.send_static_file('static/' + filename)


@app.route('/next_template', methods=['GET', 'POST'])
def next_template():
    if request.method == 'GET':
        # No data submitted, just render the login template
        return render_template('login/templates/login.html') 
    # Handle other methods if needed
    #elif request.method == 'POST':
    #    # Handle form submission, potentially interacting with the database
    #    # ...
    #    # Redirect to next page or render a new template with feedback


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ID = request.form['ID']
        password = request.form['password']

        db_connection = connect_to_database()
        if db_connection:
            cursor = db_connection.cursor(pymysql.cursors.DictCursor)  # Use DictCursor
            user = login_user_byID(cursor, ID)
            if user:
                # Verify password
                pass2 = str(user['Password'])
                if bcrypt.checkpw(password.encode('utf-8'), pass2.encode('utf-8')):
                    # Passwords match, proceed with login
                    U = User(ID, user['Name'])
                    login_user(U)

                    # Fetch user_id
                    cursor.execute("SELECT id FROM users WHERE ActualID = %s", (ID,))
                    userId = cursor.fetchone()[0] # Fetch the result
                    print(f"userId :{userId}" )
                    users=conversations(userId)

                    sub=str(ID)
                    sub=sub[:3]  
                                 
                    if(sub=="777"):
                      
                      cursor = conn.cursor(pymysql.cursors.DictCursor)
                      cursor.execute("SELECT * FROM farmers WHERE FarmerID LIKE %s", (ID,))
                      search_results = cursor.fetchall()
                      image=None

                      
                      if search_results[0]["Image"]:
                       image = base64.b64encode(search_results[0]["Image"]).decode('utf-8')
                      
                      # Render the chat template with users
                      return render_template('login/templates/FarmerProfile.html', farmer=search_results[0], userId=userId, image=image)
                    elif(sub=="999"):                      
                      cursor = conn.cursor(pymysql.cursors.DictCursor)
                      cursor.execute("SELECT * FROM admins WHERE AdminID LIKE %s", (ID,))
                      search_results = cursor.fetchall()
                      image=None
                      if search_results[0]["Image"]:
                       image = base64.b64encode(search_results[0]["Image"]).decode('utf-8')
                      
                      # Render the chat template with users
                      return render_template('login/templates/AdminProfile.html', admin=search_results[0], userId=userId, image=image)
                    elif(sub=="888"):                      
                      cursor = conn.cursor(pymysql.cursors.DictCursor)
                      cursor.execute("SELECT * FROM laborers WHERE 	LaborerID LIKE %s", (ID,))
                      search_results = cursor.fetchall()
                      image=None
                      if search_results[0]["Image"]:
                       image = base64.b64encode(search_results[0]["Image"]).decode('utf-8')

                      return render_template('login/templates/LaborerProfile.html', laborer=search_results[0], userId=userId, image=image)
                      
                    elif(sub=="666"):
                      cursor = conn.cursor(pymysql.cursors.DictCursor)
                      cursor.execute("SELECT * FROM buyers WHERE 	BuyerID LIKE %s", (ID,))
                      search_results = cursor.fetchall()
                      image=None
                      if search_results[0]["Image"]:
                        image = base64.b64encode(search_results[0]["Image"]).decode('utf-8')
                    
                      return render_template('login/templates/BuyerProfile.html', buyer=search_results[0], userId=userId, image=image)
                        
                    else:    
                      # Render the chat template with users
                       print("else")
                else:
                        # User ID not found
                        return render_template('login/templates/login.html', warning="User ID not found")
            else:
                    # Passwords don't match
                    return render_template('login/templates/login.html', warning="Invalid email or password")
        else:
                # No user found with the given ID
                return render_template('login/templates/login.html', warning="User not found")

    # Render the login page template for GET requests
    print("nlala")
    return  render_template('login/templates/login.html', warning="You have been logged out successfully.")




#logout-------------------------

@app.route('/logout' ,methods=['POST'])
@login_required
def logout():
    logout_user()
    # Redirect to the login page or any other page after logout
    return render_template('login/templates/login.html', warning="You have been logged out successfully.")




@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    contact = request.form['contact']
    region = request.form['region']
    user_type = request.form['Type']

    # Redirect to the appropriate registration route based on user type
    db_connection = connect_to_database()
    if db_connection:
        cursor = db_connection.cursor()
    
    print(f"pas1={password} pass2={confirm_password}\n")
    print(f"{user_type}\n")
    
    if password == confirm_password:
        #password = generate_password_hash(request.form['password'])
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        if user_type == 'Farmer':
            
            success = farmer_register(db_connection,cursor, name, region, contact, password,email)
            if success:
               
                return "Farmer registered successfully"
            else:
                return "Failed to register farmer"
        elif user_type =='Agricultural Consultant':
            #have to change
            success = Consultant_register(db_connection,cursor, name, region, contact, password,email)
            if success:
               
                return "Consultant registered successfully"
            else:
                return "Failed to register Consultant"
        elif user_type =='Laborer':
            #have to change
            success =laborer_register(db_connection,cursor, name, region, contact, password,email)
            if success:
                return "laborer registered successfully"
            else:
                return "Failed to register laborer"
        elif user_type =='Retailer':
            #have to change
            success =Retailer_register(db_connection,cursor, name, region, contact, password,email)
            if success:
                return "Retailer registered successfully"
            else:
                return "Failed to register Retailer"
        else:
            return "Invalid user type selected"
    else:
        return "Password and confirm password do not match"



@app.route('/protected')
@login_required
def protected_template():
    # Check if user is logged in
    if 'user_id' in session:
        # User is logged in, render protected page
        return render_template('login/templates/Regional_admin/templates/index.html')
    else:
        # User is not logged in, redirect to login page
        return redirect(url_for('.login'))
    




#chatting template 
@app.route('/search_users', methods=['POST'])
def search_users():
    search_query = request.form['searchQuery']
    current_user_id = request.args.get('userId')

    # Fetch search results excluding the current user's username
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT id, username, ActualID FROM users WHERE (username LIKE %s AND id != %s) OR (ActualID LIKE %s)",
               ('%' + search_query + '%', current_user_id, '%' + search_query + '%'))

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





#search user 
@app.route('/search', methods=['POST'])
def search_laborers():
    Ques= request.form['Ques']
    cursor = conn.cursor(pymysql.cursors.DictCursor)
   
    cursor.execute("SELECT id, username FROM users WHERE username LIKE %s or ActualID Like %s", ('%' + Ques + '%', Ques))
    search_results = cursor.fetchall()
  
    # Convert the list of dictionaries to JSON and return it
    return json.dumps(search_results)


#Find Friends
@app.route('/index', methods=['POST'])
def Find():
    Ques= request.form['Ques']
    print(Ques)
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
    """, (Ques, Ques))
    
    # Fetch and sort the search results by user ID
    search_results = sorted(cursor.fetchall(), key=lambda x: x['id'])

    # Convert the sorted list of dictionaries to JSON and return it
    return json.dumps(search_results)



#update Farmer
@app.route('/update_farmer', methods=['POST'])
def update_farmer():
    # Extract the data from the request
    data = request.form
    farmerID = data.get('farmerID')  
    name = data.get('name')
    BIO = data.get('BIO')
    email = data.get('email')
    region = data.get('region')
    contact = data.get('contact')
    bankID = data.get('bankID')
    frameSize = data.get('frameSize')
    onlinePaymentInput = data.get('onlinePaymentInput')
    image_file = request.files['image'] if 'image' in request.files else None
    
    # Check if an image file is uploaded
    if image_file:
        # Read the image data
        image_data = image_file.read()

        # Perform the database update operation with image data
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("UPDATE farmers SET Name=%s, Email=%s, Region_ID=%s, Contact=%s, BankId=%s, Farm_Size=%s, OnlinePaymentNumber=%s, Image=%s ,BIO=%s WHERE FarmerID=%s",
                       (name, email, region, contact, bankID, frameSize, onlinePaymentInput, image_data,BIO, farmerID))
        conn.commit()

        # Return a response indicating the update status
        return "Update successful with image"
    else:
        # Perform the database update operation without image data
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("UPDATE farmers SET Name=%s, Email=%s, Region_ID=%s, Contact=%s, BankId=%s, Farm_Size=%s, OnlinePaymentNumber=%s,BIO=%s  WHERE FarmerID=%s",
                       (name, email, region, contact, bankID, frameSize, onlinePaymentInput,BIO, farmerID))
        conn.commit()
        # Return a response indicating the update status
        return "Update successful without image"


#update Admin
@app.route('/update_Admin', methods=['POST'])
def update_Admin():
    # Extract the data from the request
    data = request.form
    AdminID = data.get('AdminID')  
    name = data.get('name')
    email = data.get('email')
    region = data.get('region')
    contact = data.get('contact')
    image_file = request.files['image'] if 'image' in request.files else None
    
    # Check if an image file is uploaded
    if image_file:
        # Read the image data
        image_data = image_file.read()

        # Perform the database update operation with image data
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("UPDATE admins SET Name=%s, E_mail=%s, RegionID=%s, Contact=%s, Image=%s WHERE AdminID=%s",
                       (name, email, region, contact, image_data, AdminID))
        conn.commit()
       
        # Return a response indicating the update status
        return "Update successful with image"
    else:
        print('on admin update')
        # Perform the database update operation without image data
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("UPDATE admins SET Name=%s, E_mail=%s, RegionID=%s, Contact=%s WHERE AdminID=%s",
               (name, email, region, contact, AdminID))
        conn.commit()
        return "Update successful without image"


#update Laborer
@app.route('/update_Laborer', methods=['POST'])
def update_Laborer():
    # Extract the data from the request
    data = request.form
    LaborerID = data.get('LaborerID')  
    name = data.get('name')
    email = data.get('email')
    region = data.get('region')
    Skill = data.get('Skill')
    ExpectedIncome = data.get('ExpectedIncome')
    contact = data.get('contact')
    bankID = data.get('Bankid')
    onlinePaymentInput = data.get('onlinePaymentInput')
    image_file = request.files['image'] if 'image' in request.files else None


    # Check if an image file is uploaded
    if image_file:
        # Read the image data
        image_data = image_file.read()

        # Perform the database update operation with image data
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("UPDATE laborers SET Name=%s, Email=%s, RegionID=%s, Contact=%s, Bankid=%s, ExpectedIncome=%s, OnlinePaymentNumber=%s, Image=%s,Skills=%s WHERE LaborerID=%s",
                       (name, email, region, contact, bankID, ExpectedIncome, onlinePaymentInput, image_data, Skill, LaborerID))
        conn.commit()

        # Return a response indicating the update status
        return "Update successful with image"
    else:
        # Perform the database update operation without image data
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("UPDATE laborers SET Name=%s, Email=%s, RegionID=%s, Contact=%s, Bankid=%s, ExpectedIncome=%s, OnlinePaymentNumber=%s, Skills=%s WHERE LaborerID=%s",
                       (name, email, region, contact, bankID, ExpectedIncome, onlinePaymentInput, Skill, LaborerID))
        conn.commit()
        # Return a response indicating the update status
        return "Update successful without image"

    


#update labore availability
@app.route('/update_availability', methods=['POST'])
def update_availability():
    laborer_id = request.args.get('laborer_id')
    availability_status = request.args.get('availabilityStatus')

    print(availability_status)

    try:
        # Update the availability status in the database
        with conn.cursor() as cursor:
            sql = "UPDATE laborers SET AvailabilityStatus = %s WHERE LaborerID = %s"
            cursor.execute(sql, (availability_status, laborer_id))
            conn.commit()

        return jsonify({"message": "Availability status updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500




#laborer Hire request

@app.route('/fetch_data', methods=['GET'])
def fetch_data():
    laborer_id = request.args.get('laborer_id')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = """
    SELECT laborer_hire.*, farmers.Name AS FarmerName 
    FROM laborer_hire 
    JOIN farmers ON laborer_hire.FarmerID = farmers.FarmerID 
    WHERE laborer_hire.LaborerID = %s
    """
    cursor.execute(query, (laborer_id,))
    data = cursor.fetchall()
    print(data)
    return jsonify(data)



#update_status-----

@app.route('/update_status', methods=['POST'])
def update_status():
    laborer_id = request.args.get('laborer_id')
    status = request.args.get('status')
    FarmerID = request.args.get('FarmerID')

    print(status)
    print(laborer_id)
    print(FarmerID)

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM farmers WHERE FarmerID=%s",(FarmerID,))

    results = cursor.fetchall()
    
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM laborers WHERE LaborerID=%s",(laborer_id,))

    results2 = cursor.fetchall()

    if status=="accepted":
        sub="Hire Request Confirmation"
        msg1 = f"Dear {results[0]["Name"]}\n\n"

        message =f" Your Hire Request Has Been Accepted {results2[0]["Name"]}\nContact:{results2[0]["Contact"]}\nLaboereID:{laborer_id}"
        send_email(results[0]["Email"],sub,msg1+message)   
    try:
        # Update the availability status in the database
        with conn.cursor() as cursor:
            sql = "UPDATE laborer_hire SET status = %s WHERE LaborerID = %s AND FarmerID=%s"
            cursor.execute(sql, (status, laborer_id,FarmerID))
            conn.commit()

        return jsonify({"message": "Availability status updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500





#chat  ----------= start

@app.route('/Chat')
def chat():
    Id = request.args.get('ID')
    print(Id)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT id FROM users WHERE ActualID = %s", (Id,))
    result = cursor.fetchone()
    
    if result:
        userId = result['id']
        users = conversations(userId)
        # Now you can use the user_data parameter as needed
        return render_template('login/templates/chat/templates/index.html', users=users, userId=userId)
    else:
        # Handle the case when no data is found
        return "User not found"


@app.route('/load_Chat')
def load_Chat():
    id = request.args.get('ID')  # Get the FarmerID from the request
    
    iframe_src = f'/Chat?ID={id}'  # Include the FarmerID in the iframe source URL
    return jsonify({'main-content': f'<iframe src="{iframe_src}" width="100%" height="100%" style="border:none;"></iframe>'})

#chat  ----------= end



#market place     -------- start 


@app.route('/marketplace_farmer')
def market_place():
    # Fetch products grouped by farmers from the database
    FarmerID = request.args.get('FarmerID')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM marketplace WHERE FarmerID = %s"
    cursor.execute(query, (FarmerID,))
    products = cursor.fetchall()
    
    for product in products:
        product['Image'] = base64.b64encode(product['Image']).decode()

    # Corrected print statement

    return render_template('login/templates/AddProductbyFarmer.html', products=products)

@app.route('/load_marketplace')
def load_marketplace():
    FarmerID = request.args.get('FarmerID')  # Get the FarmerID from the request
    
    iframe_src = f'/marketplace_farmer?FarmerID={FarmerID}'  # Include the FarmerID in the iframe source URL
    return jsonify({'main-content': f'<iframe src="{iframe_src}" width="100%" height="100%" style="border:none;"></iframe>'})




@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Get form data
        product_name = request.form['productName']
        product_region = request.form['productRegion']
        product_value = request.form['productValue']
        product_producer = request.form['productProducer']
        product_quantity = request.form['productQuantity']

        print(product_name)
        # Save the uploaded image to your server and get its path
        image_file = request.files['productImageUpload'] 

        # Read the image data
        if image_file:
            image_data = image_file.read()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = "INSERT INTO marketplace (CropName, Price, FarmerID, QuantityAvailable, Image,Region) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (product_name, product_value, product_producer, product_quantity, image_data,product_region)
            cursor.execute(query, values)
            conn.commit()
        else:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = "INSERT INTO marketplace (CropName, Price, FarmerID, QuantityAvailable,Region) VALUES (%s, %s, %s, %s, %s)"
            values = (product_name, product_value, product_producer, product_quantity,product_region)
            cursor.execute(query, values)
            conn.commit()
        return 'Product uploaded successfully!'
    else:
        return 'Method not allowed'




#market place     -------- END 




#search laborer------------   Start


@app.route('/searchlaborer')
def searchlaborer():
    FarmerID = request.args.get('FarmerID')
    return render_template("login/templates/search_laborer.html", FarmerID=FarmerID)



@app.route('/load_searchlaborer')
def load_searchlaborer():
    FarmerID = request.args.get('FarmerID')  # Get the FarmerID from the request
    
    iframe_src = f'/searchlaborer?FarmerID={FarmerID}'  # Include the FarmerID in the iframe source URL
    return jsonify({'main-content': f'<iframe src="{iframe_src}" width="100%" height="100%" style="border:none;"></iframe>'})



#Search laborer by region

@app.route('/search_laborers', methods=['POST'])
def search_labor():
    region = request.form['region']
    region = region.upper()
    cursor = conn.cursor()

    query = """
    SELECT laborers.*, regions.RegionName
    FROM laborers
    INNER JOIN regions ON laborers.RegionID = regions.RegionID
    WHERE regions.RegionName = %s
    """
    cursor.execute(query, (region,))
    laborers = cursor.fetchall()
    cursor.close()
    
    # Prepare a list of dictionaries containing laborer data
    laborer_list = []
    for laborer in laborers:
        image = None
        if laborer[9]:  # Assuming index 10 contains the image data
            # Convert the image data from bytes to base64 encoded string
            image = base64.b64encode(laborer[9]).decode('utf-8')
        
        laborer_dict = {
            'LaborerID': laborer[0],
            'image': image,
            'skills': laborer[3],
            'name': laborer[2],
            'region': region,
            'ExpectedIncome': laborer[7],
            'availability': 'Available' if laborer[5] == 1 else 'Not Available',
            'rating': float(laborer[4]),
            'contact': laborer[8],
            'email': laborer[10]   
        }
        laborer_list.append(laborer_dict)

    # Return JSON response containing laborer data
    return jsonify(laborer_list)


#hire_laborer

@app.route('/hire_laborer', methods=['POST'])
def hire_laborer():
    laborer_id = request.args.get('laborer_id')
    farmer_id = request.args.get('FarmerID')

    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO laborer_hire (LaborerID,FarmerID) VALUES (%s, %s)"
            cursor.execute(sql, (laborer_id, farmer_id))
            conn.commit()

        # Send notification to the laborer with ID laborer_id
        # You can implement this part based on your notification system
        # For example, sending an email or using a messaging service

        return jsonify({"message": "Hire request sent successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500




#search laborer------------   end





#seminarr  ---------- start from here 


from datetime import timedelta

@app.route('/seminar_details')
def seminar_details():
    RegionID = request.args.get('RegionID') 
    cursor = conn.cursor()
    query = """
    SELECT s.*
    FROM seminars s
    JOIN admins a ON s.AdminID = a.AdminID 
    WHERE a.RegionID = %s
    ORDER BY s.SeminarID DESC
    LIMIT 1
    """
    cursor.execute(query, (RegionID,))

    # Fetch seminar details
    seminar = cursor.fetchone()
    seminar_details = {
        'SeminarID': seminar[0],
        'AdminID': seminar[1],
        'Guest': seminar[2],
        'Image': base64.b64encode(seminar[3]).decode(),  # Convert bytes to base64-encoded string 
        'SeminarTitle': seminar[4],
        'SpeakerName': seminar[5],
        'SpeakerQualification': seminar[6],
        'meeting_date': seminar[7],
        'meeting_time': str(seminar[8]), 
        'Email': seminar[9],
        'Venue': seminar[10],
        'KeyTopics': seminar[11],
        'sponsors': seminar[12],
        'city': seminar[13],
        'details': seminar[14]
    }

    return jsonify(seminar_details)




#add and update page functions--------

@app.route('/load_Add_update')
def load_Add_update():
    AdminID = request.args.get('AdminID')
    iframe_src = f'/add_update?AdminID={AdminID}'
    return jsonify({'main-content':'<iframe src="/add_update" width="100%" height="100%" style="border:none;"></iframe>'})

@app.route("/add_update")
def add_update():
    AdminID = request.args.get('AdminID')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print(f"form Add update{AdminID}")
    # Get the last inserted CropID and increment by 1
    cursor.execute("SELECT f.* FROM farmers f JOIN admins a ON f.Region_ID = a.RegionID WHERE a.AdminID = %s ", (AdminID,))
    farmers = cursor.fetchall()

    cursor.execute("SELECT l.* FROM laborers l JOIN admins a ON l.RegionID = a.RegionID WHERE a.AdminID = %s ", (AdminID,))
    laborers = cursor.fetchall()
    return render_template('login/templates/Add_update.html',AdminID=AdminID,farmers=farmers, laborers=laborers)




@app.route('/crops_update', methods=['POST'])
def crops_update():
    # Retrieve form data
    AdminID = request.args.get('AdminID')
    crop_name = request.form['crop_name']
    soil_ph = request.form['soil_ph']
    required_weather = request.form['required_weather']
    required_temperature = request.form['required_temperature']
    growth_period = request.form['growth_period']
    harvest_time_period = request.form['harvest_time_period']
    fertilizer_name = request.form['fertilizer_name']

    print(AdminID)
    # Insert data into the database
    cursor = conn.cursor()

    # Get the last inserted CropID and increment by 1
    cursor.execute("SELECT MAX(CropID) FROM crops")
    result = cursor.fetchone()
    last_crop_id = result[0] if result[0] else 0
    new_crop_id = last_crop_id + 1

    # Insert data with the incremented CropID
    sql = "INSERT INTO crops (CropID, CropName, SoilPH, WeatherConditions, Temperature, GrowthPeriod, HarvestTime, Fertilizer_names) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (new_crop_id, crop_name, soil_ph, required_weather, required_temperature, growth_period, harvest_time_period, fertilizer_name)
    cursor.execute(sql, values)
    conn.commit()

    return "Crop information added successfully!"



from flask import request

@app.route('/crop_prices_update', methods=['POST'])
def crop_prices_update():
    # Retrieve form data
    crop_id = request.form['crop_id']
    region_id = request.form['region_id']
    price = request.form['price']

    # Insert data into the database
    cursor = conn.cursor()
    sql = "INSERT INTO CropPrices (CropID, RegionID, Price) VALUES (%s, %s, %s)"
    values = (crop_id, region_id, price)
    cursor.execute(sql, values)
    conn.commit()

    return "Crop price information added successfully!"




@app.route('/seminar_update', methods=['POST'])
def seminar_update():
    # Retrieve form data
    seminar_title = request.form['seminarTitle']
    speaker_name = request.form['speakerName']
    speaker_qualification = request.form['qualification']
    meeting_date = request.form['meetingDate']
    meeting_time = request.form['meetingTime']
    email = request.form['email']
    venue = request.form['venue']
    key_topics = request.form['keyTopics']
    sponsors = request.form['sponsors']
    city = request.form['city']
    details = request.form['details']
    AdminID = request.args.get('AdminID')
    print(AdminID)
    # Check if an image file is uploaded
    image_file = request.files['image'] if 'image' in request.files else None
    
    # Insert data into the database
    cursor = conn.cursor()
    sql = "INSERT INTO seminars (SeminarTitle, SpeakerName, SpeakerQualification, meeting_date, meeting_time,Email, Venue, KeyTopics, Sponsors, City, Details, Image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (seminar_title, speaker_name, speaker_qualification, meeting_date, meeting_time, email, venue, key_topics, sponsors, city, details, image_file.read() if image_file else None)
    cursor.execute(sql, values)
    conn.commit()

    return "Seminar information added successfully!"





#---------Buyer-------
@app.route('/update_Buyerr', methods=['POST'])
def update_Buyerr():
    # Extract the data from the request
    data = request.form
    UserID = data.get('UserID')  
    name = data.get('name')
    email = data.get('email')
    region = data.get('region')
    contact = data.get('contact')
    bankID = data.get('Bankid')
    onlinePaymentInput = data.get('onlinePaymentInput')
    image_file = request.files['image'] if 'image' in request.files else None

    print(UserID)
    print(name)
    # Check if an image file is uploaded
    if image_file:
        # Read the image data
        image_data = image_file.read()

        # Perform the database update operation with image data
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("UPDATE buyers SET Name=%s, Email=%s, RegionID=%s, Contact=%s, Bankid=%s, OnlinePaymentNumber=%s, Image=%s WHERE UserID =%s",
                       (name, email, region, contact, bankID, onlinePaymentInput, image_data, UserID))
        conn.commit()

        # Return a response indicating the update status
        print(" successful with image")
        return "Update successful with image"
    else:
        # Perform the database update operation without image data
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("UPDATE buyers SET Name=%s, Email=%s, RegionID=%s, Contact=%s, Bankid=%s, OnlinePaymentNumber=%s WHERE UserID =%s",
                       (name, email, region, contact, bankID, onlinePaymentInput, UserID))
        conn.commit()
        print(" successful without image")
        # Return a response indicating the update status
        return "Update successful without image"


@app.route('/blog' ,methods=['GET'])
def blog():
    return render_template ('login/templates/blog.html')




#------------------ Buyer-----------

@app.route('/buyer-profile')
def buyer_profile():
    return render_template('BuyerProfile.html')

@app.route('/marketplace_Buyer')
def market_placeBuyer():
    return render_template('login/templates/MarketPlace.html')

@app.route('/load_marketplace_Buyer')
def load_marketplace_Buyer():
    return jsonify({'main-content': f'<iframe src="/marketplace_Buyer" width="100%" height="100%" style="border:none;"></iframe>'})





#--------store House -------

@app.route('/storeHouse')
def storeHouse():
    return render_template('login/templates/storehouseTest.html')

@app.route('/load_storeHouse')
def load_storeHouse():
    return jsonify({'main-content': f'<iframe src="/storeHouse" width="100%" height="100%" style="border:none;"></iframe>'})




#chatbot page functions
@app.post("/predict")
def predict():
     text = request.get_json().get("message")
     response = get_response(text)
     message = {"Answer": response}
     return jsonify(message)


if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else 5000
    app.run(host='0.0.0.0', port=port)