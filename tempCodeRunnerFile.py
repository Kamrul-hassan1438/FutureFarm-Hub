@app.route('/fetch_data', methods=['GET'])
def fetch_data():
    laborer_id = request.args.get('laborer_id')
    print(laborer_id)
    cursor = conn.cursor()
    # Assuming you have a database connection and cursor
    query = """
    SELECT laborer_hire.*, farmers.Name AS FarmerName 
    FROM laborer_hire 
    JOIN farmers ON laborer_hire.FarmerID = farmers.FarmerID 
    WHERE laborer_hire.LaborerID = %s
    """
    cursor.execute(query, (laborer_id,))
    
    # Fetch all rows from the result set
    data = cursor.fetchall()
    print(data)
    # Close cursor and database connection
    cursor.close()
    
    return jsonify(data)