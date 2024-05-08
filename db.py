import mysql.connector
from Mail import  send_email

def connect_to_database():
    """
    Connect to the MySQL database.
    """
    try:
        # Connect to the database
        db_connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='futurefarm hub'  # Corrected database name
        )
        print("Connected to the database.")
        return db_connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def login_user_byID(cursor, ID):
  
    try:
        ID = str(ID)
        f_three_digits = ID[:3]
        if f_three_digits =='999':
         cursor.execute("SELECT * FROM admins WHERE AdminID = %s", (ID,))

         row = cursor.fetchone()
         # Convert the tuple into a dictionary (assuming column names are known)
         columns = [col[0] for col in cursor.description]  # Get column names
         user = dict(zip(columns, row))
         #user = cursor.fetchone(dictionary=True)
         return user
        elif f_three_digits=='777':
         cursor.execute("SELECT * FROM farmers WHERE FarmerID = %s", (ID,))
         row = cursor.fetchone()
         # Convert the tuple into a dictionary (assuming column names are known)
         columns = [col[0] for col in cursor.description]  # Get column names
         user = dict(zip(columns, row))
         return user

        elif f_three_digits=='888':
         cursor.execute("SELECT * FROM laborers WHERE LaborerID = %s", (ID,))
         row = cursor.fetchone()
         # Convert the tuple into a dictionary (assuming column names are known)
         columns = [col[0] for col in cursor.description]  # Get column names
         user = dict(zip(columns, row))
         return user  
          
        elif f_three_digits=='666':
         cursor.execute("SELECT * FROM buyers WHERE BuyerID = %s", (ID,))
         row = cursor.fetchone()
         # Convert the tuple into a dictionary (assuming column names are known)
         columns = [col[0] for col in cursor.description]  # Get column names
         user = dict(zip(columns, row))
         return user    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    

# Function to get Region ID based on Region Name
def get_region_id(cursor, region_name):
    try:
        cursor.execute("SELECT	RegionID FROM regions WHERE RegionName = %s", (region_name,))
        region_id = cursor.fetchone()
        return region_id[0] if region_id else None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None



def generate_farmer_id(cursor):
    try:
        # Get the count of existing farmers from the database
        cursor.execute("SELECT COUNT(*) FROM farmers")
        count = cursor.fetchone()[0]

        # Format the Farmer ID based on the count
        farmer_id = f"777{count + 1:03d}"  # Assuming count starts from 0, adjust if needed

        return farmer_id
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    



def farmer_register(db_connection,cursor, name, region, contact, password,email):
    try:
        farmer_id = generate_farmer_id(cursor)

        # Make region_name Uppercase
        region = region.upper()
        region_id = get_region_id(cursor, region)
        cursor.execute("INSERT INTO users (ActualID, username) VALUES (%s, %s)",
                       (farmer_id, name))
        db_connection.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")

        user_id = cursor.fetchone()[0] 
        cursor.execute("INSERT INTO farmers (UserID,FarmerID, Name, Region_ID, contact, Password,Email) VALUES (%s, %s, %s, %s, %s, %s,%s)",
                       (user_id,farmer_id, name, region_id, contact, password,email))
        
        # Assuming 'connection' is available in the scope
        db_connection.commit()

        sub="Account Confirmation"
        msg1=f"Dear {name}\n\nThank you for creating an account with us.\n"
        message =f"Your User ID : {farmer_id}\nRegion Name: {region}\nRegion ID : {region_id}\n\nThank you,\nFuturefarm Hub"
        send_email(email,sub,msg1+message)

        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False



def generate_consultant_id(cursor):
    try:
        # Get the count of existing farmers from the database
        cursor.execute("SELECT COUNT(*) FROM admins")
        count = cursor.fetchone()[0]

        # Format the Farmer ID based on the count
        consultant_id = f"999{count + 1:03d}"  # Assuming count starts from 0, adjust if needed

        return consultant_id
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
def Consultant_register(db_connection,cursor, name, region, contact, password,email):
    try:
        consultant_id= generate_consultant_id(cursor)
        # Make region_name Uppercase
        region = region.upper()
        region_id = get_region_id(cursor, region)
        cursor.execute("INSERT INTO users (ActualID, username) VALUES (%s, %s)",
                       (consultant_id, name))
        db_connection.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")

        user_id = cursor.fetchone()[0] 
        cursor.execute("INSERT INTO admins (UserID,AdminID, Name, RegionID,E_mail, contact, Password) VALUES (%s,%s, %s, %s, %s, %s, %s)",
                       (user_id,consultant_id, name, region_id,email, contact, password))

        # Assuming 'connection' is available in the scope
        db_connection.commit()
        sub="Account Confirmation"
        msg1=f"Dear {name}\n\nThank you for creating an account with us.\n"
        message =f"Your User ID : {consultant_id}\nRegion Name: {region}\nRegion ID : {region_id}\n\nThank you,\nFuturefarm Hub"
        send_email(email,sub,msg1+message)

        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False



def generate_laborer_id(cursor):
    try:
        # Get the count of existing farmers from the database
        cursor.execute("SELECT COUNT(*) FROM laborers")
        count = cursor.fetchone()[0]

        # Format the Farmer ID based on the count
        laborer_id = f"888{count + 1:03d}"  # Assuming count starts from 0, adjust if needed

        return laborer_id
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def laborer_register(db_connection,cursor, name, region, contact, password,email):
    try:
        laborer_id = generate_laborer_id(cursor)
        region = region.upper()
        region_id = get_region_id(cursor, region)
        cursor.execute("INSERT INTO users (ActualID, username) VALUES (%s, %s)",
                       (laborer_id, name))
        db_connection.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")

        user_id = cursor.fetchone()[0] 
        cursor.execute("INSERT INTO laborers (UserID,LaborerID, Name, RegionID, Contact, Password,Email) VALUES (%s, %s, %s, %s, %s, %s,%s)",
                       (user_id,laborer_id, name, region_id, contact, password,email))

        db_connection.commit()

        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

def generate_Retailer_id(cursor):
    try:
        # Get the count of existing farmers from the database
        cursor.execute("SELECT COUNT(*) FROM buyers")
        count = cursor.fetchone()[0]

        # Format the Farmer ID based on the count
        Retailer_id = f"666{count + 1:03d}"  # Assuming count starts from 0, adjust if needed

        return Retailer_id
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def Retailer_register(db_connection,cursor, name, region, contact, password,email):
    try:
        Retailer_id = generate_Retailer_id(cursor)
        region = region.upper()
        region_id = get_region_id(cursor, region)
        cursor.execute("INSERT INTO users (ActualID, username) VALUES (%s, %s)",
                       (Retailer_id, name))
        db_connection.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        user_id = cursor.fetchone()[0] 

        print(f"user ID: {user_id}")
        cursor.execute("INSERT INTO buyers (UserID,BuyerID, Name, RegionID, Contact, Password,Email) VALUES (%s, %s, %s, %s, %s, %s,%s)",
                       (user_id,Retailer_id, name, region_id, contact, password,email))
        sub="Account Confirmation"
        msg1=f"Dear {name}\n\nThank you for creating an account with us.\n"
        message =f"Your User ID : {Retailer_id}\nRegion Name: {region}\nRegion ID : {region_id}\n\nThank you,\nFuturefarm Hub"
        send_email(email,sub,msg1+message)
        db_connection.commit()


        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

