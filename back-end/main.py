from flask import Flask, jsonify , request
import sqlite3
from flask_cors import CORS, cross_origin
import io
from datetime import datetime
from fileinput import filename 
from hashlib import md5
import random

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect("./data-shop.db")
    conn.row_factory = sqlite3.Row
    return conn

# back test
@app.route('/',methods=['GET'])
def test():
    return "ok"

#-----------------user---------------------------

# users crud function
def get_all_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users')
    Users = cur.fetchall()
    final_Users = []
    for User in Users:
        final_Users.append({
            "id": User[0],
            "Name": User[1],
            "Password": User[2],
            "Email": User[3],
            "Phone": User[4],
            "registration_date": User[5],
            "Role": User[6],
            "address": User[7],
        })
    conn.close()
    return final_Users
def get_users(users_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users WHERE user_id = ?', (users_id,))
    User = cur.fetchone()
    final_users = {
            "id": User[0],
            "Name": User[1],
            "Password": User[2],
            "Email": User[3],
            "Phone": User[4],
            "registration_date": User[5],
            "Role": User[6],
            "address": User[7],
        }
    conn.close()
    return final_users
def create_user(Name, Password, Email, Phone, Role,address ):
    conn = get_db_connection()
    cur = conn.cursor()
    password_hash = md5(Password.encode()).hexdigest()
    registration_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute('INSERT INTO Users (username, password_hash,email,phone_number,registration_date,role,default_shipping_address) VALUES (?, ?, ?, ? , ?, ?, ?)', (Name, password_hash, Email, Phone, registration_date, Role,address ))
    conn.commit()
    customer_id = cur.lastrowid
    conn.close()
    return customer_id
def update_user(id,Name, Password, Email, Phone, registration_date, Role,address):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE Users SET username = ?, password_hash = ?, email = ?, phone_number = ?, registration_date = ?, role = ? , default_shipping_address = ? WHERE user_id = ?', (Name, Password, Email, Phone, registration_date, Role,address,id))
    conn.commit()
    conn.close()
    return get_users(id)
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
def login_user(user_name,Password):
    conn = get_db_connection()
    cur = conn.cursor()
    password_hash = md5(Password.encode()).hexdigest()
    cur.execute('SELECT * FROM Users WHERE username = ? and password_hash = ?', (user_name,password_hash,))
    user_data = cur.fetchone()
    if user_data:
        return "ok"
    else : 
        return "mousavi"

# users CRUD routes
@app.route('/Users', methods=['GET'])
def list_users():
    range = request.args.get('range')
    users = get_all_users()
    response = jsonify(users)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(users)
    return response
@app.route('/Users/<int:user_id>', methods=['GET'])
def get_customer_by_id(user_id):
    user = get_users(user_id)
    if user is None:
        return '', 404
    return jsonify(user), 200
@app.route('/Users', methods=['POST'])
def add_customer():
    name = request.json['Name']
    Password = request.json['Password']
    Email = request.json['Email']
    Phone = request.json['Phone']
    Role = request.json['Role']
    address = request.json['address']
    user_id = create_user(name, Password, Email, Phone, Role,address)
    if user_id:
        return jsonify(get_users(user_id)), 201
    else:
        return jsonify("NO")
@app.route('/Users/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    name = request.json['Name']
    Password = request.json['Password']
    Email = request.json['Email']
    Phone = request.json['Phone']
    registration_date = request.json['registration_date']
    Role = request.json['Role']
    address = request.json['address']
    updated = update_user(user_id,name, Password, Email, Phone, registration_date, Role,address)
    return jsonify(updated), 200
@app.route('/Users/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    delete_user(user_id)
    return jsonify({"id":user_id}), 200

@app.route('/Users/login', methods=['POST'])
def login_users():
    user_name = request.json['user_name']
    password = request.json['password']
    response = login_user(user_name, password)
    return jsonify(response)

#-----------------user---------------------------
#----------------category--------------------------

#category crud function
def get_all_Categories():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Categories')
    Categories = cur.fetchall()
    final_Categories = []
    for Categorie in Categories:
        final_Categories.append({
            "id": Categorie[0],
            "name": Categorie[1],
            "description": Categorie[2],
            "parent_category_id": Categorie[3],
            "created_at": Categorie[4],
        })
    conn.close()
    return final_Categories
def create_Categories(name, description, parent_category_id):
    conn = get_db_connection()
    cur = conn.cursor()
    created_at = datetime.today().strftime('%Y-%m-%d')
    cur.execute('INSERT INTO Categories (name, description,parent_category_id,created_at) VALUES (?, ?, ?, ?)', (name, description, parent_category_id, created_at))
    conn.commit()
    Category_id = cur.lastrowid
    conn.close()
    return get_Categories(Category_id)
def get_Categories(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Categories WHERE category_id = ?',(id,))
    Categorie = cur.fetchone()
    conn.close()
    final_category = {
        "id": Categorie[0],
        "name": Categorie[1],
        "description": Categorie[2],
        "parent_category_id": Categorie[3],
        "created_at": Categorie[4],
    }
    return final_category
def delete_category(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Categories WHERE category_id = ?', (id,))
    conn.commit()
    conn.close()
def update_category(name,description,parent_category_id,created_at,id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE Categories SET name = ?, description = ?, parent_category_id = ?, created_at = ? WHERE category_id = ?', (name,description,parent_category_id,created_at,id))
    conn.commit()
    conn.close()
    return get_Categories(id)

# category crud routes
@app.route('/Categories', methods=['GET'])
def list_Categories():
    Categories = get_all_Categories()
    response = jsonify(Categories)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(Categories)
    return response

# @app.route('/parent_categories', methods=['GET'])
# def parent_categories():
#     return "arr"

@app.route('/Categories/<int:id>', methods=['GET'])
def Category(id):
    Category = get_Categories(id)
    if Category is None:
        return '', 404
    return jsonify(Category), 200
@app.route('/Categories', methods=['POST'])
def add_Categories():
    name = request.json['name']
    description = request.json['description']
    parent_category_id = request.json['parent_category_id']
    Categories_id = create_Categories(name, description, parent_category_id)
    return Categories_id , 201
@app.route('/Categories/<int:id>', methods=['DELETE'])
def delete_category_by_id(id):
    delete_category(id)
    return jsonify({"id":id}), 200
@app.route('/Category/<int:id>', methods=['PUT'])
def update_category_by_id(id):
    name = request.json['name']
    description = request.json['description']
    parent_category_id = request.json['parent_category_id']
    created_at = request.json['created_at']
    updated = update_category(name, description, parent_category_id, created_at,id)
    return jsonify(updated), 200

#----------------category--------------------------

#------------------order--------------------------
#order crud function
def get_all_orders():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Orders')
    orders = cur.fetchall()
    final_orders = []
    for order in orders:
        final_orders.append({
            "id": order[0],
            "user_id": order[1],
            "order_date": order[2],
            "total_amount": order[3],
            "status": order[4],
    })
    conn.close()
    return final_orders
def create_order(user_id, order_date, total_amount, status):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO Orders (user_id, order_date, total_amount, status) VALUES (?, ?, ?, ?)', (user_id, order_date, total_amount, status))
    conn.commit()
    current_id = cur.lastrowid
    conn.close()
    return current_id
def get_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Orders WHERE order_id = ?', (order_id,))
    order = cur.fetchone()
    conn.close()
    if order is None:
        return None
    order_data = {
        "id": order[0],
        "user_id": order[1],
        "order_date": order[2],
        "total_amount": order[3],
        "status": order[4],
    }
    return order_data

def delete_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Orders WHERE order_id = ?', (order_id,))
    conn.commit()
    conn.close()
    return "ok"
def update_order(order_id, customer_id, order_date, total_amount, status):
    conn = get_db_connection()
    cur = conn.cursor()
    update_stmt = "UPDATE Orders SET "
    update_params = []
    if customer_id is not None:
        update_stmt += "customer_id = ?, "
        update_params.append(customer_id)
    if order_date is not None:
        order_date_str = order_date.strftime('%Y-%m-%d %H:%M:%S')
        update_stmt += "order_date = ?, "
        update_params.append(order_date_str)        
#order crud routes
@app.route('/Orders', methods=['GET'])
def list_orders():
    orders = get_all_orders()
    response = jsonify(orders)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(orders)
    return response

@app.route('/Orders/<int:order_id>', methods=['GET'])
def order(order_id):
    order = get_order(order_id)
    if order is None:
        return '', 404
    return order, 201

@app.route('/Orders', methods=['POST'])
def add_order():
    user_id = request.json['user_id']
    order_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    total_amount = request.json['total_amount']
    status = request.json['status']
    order_id = create_order(user_id, order_date, total_amount, status)
    return get_order(order_id), 201

@app.route('/Orders/<int:order_id>', methods=['DELETE'])
def delete_order_by_id(order_id):
    delete_order(order_id)
    return jsonify({"id": order_id}), 200

@app.route('/Orders/<int:order_id>', methods=['PUT'])
def update_order_by_id(order_id):
    user_id = request.json['user_id']
    order_date_str = request.json['order_date']
    order_date = datetime.strptime(order_date_str, '%Y-%m-%d %H:%M:%S')
    total_amount = request.json['total_amount']
    status = request.json['status']
    updated_order = update_order(order_id, user_id, order_date, total_amount, status)
    return jsonify(updated_order), 200

#------------------order--------------------------
# -----------------------order-detail---------------------------------

#order-detail crud function
def get_all_orderDetail():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM OrderDetails')
    details = cur.fetchall()
    final_details = []
    for detail in details:
        final_details.append({
            "id": detail[0],
            "order_id": detail[1],
            "product_id": detail[2],
            "quantity": detail[3],
            "unit_price": detail[4],
        })
    conn.close()
    return final_details

def get_details(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM OrderDetails WHERE order_detail_id = ?',(id,))
    detail = cur.fetchone()
    conn.close()
    final_details = {
            "id": detail[0],
            "order_id": detail[1],
            "product_id": detail[2],
            "quantity": detail[3],
            "unit_price": detail[4],
    }
    return final_details

def create_detail(order_id,quantity,unit_price):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO OrderDetails (order_id,quantity,unit_price) VALUES ( ?, ?,?)', (order_id,quantity,unit_price,))
    conn.commit()
    current_id = cur.lastrowid
    conn.close()
    return current_id

def delete_detail(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM OrderDetails WHERE order_detail_id = ?', (id,))
    conn.commit()
    conn.close()
    
def update_detail(order_id, product_id,quantity,unit_price,id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE OrderDetails SET order_id = ?, product_id = ?, quantity = ?, unit_price = ? WHERE order_detail_id = ?', (order_id, product_id,quantity,unit_price,id))
    conn.commit()
    conn.close()
    return get_details(id)

# order-detail routes
@app.route('/Order_Details', methods=['GET'])
def list_details():
    details = get_all_orderDetail()
    response = jsonify(details)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(details)
    return response

@app.route('/Order_Details/<int:id>', methods=['GET'])
def detail(id):
    detail = get_details(id)
    if detail is None:
        return '', 404
    return jsonify(detail), 200

@app.route('/Order_Details', methods=['POST'])
def add_details():
    order_id = request.json['order_id']
    # product_id = request.json['product_id']
    quantity = request.json['quantity']
    unit_price = request.json['unit_price']
    detail_id = create_detail(order_id, quantity,unit_price)
    return get_details(detail_id), 200

@app.route('/Order_Details/<int:id>', methods=['DELETE'])
def delete_detail_by_id(id):
    delete_detail(id)
    return jsonify({"id":id}), 200

@app.route('/Order_Details/<int:id>', methods=['PUT'])
def update_detail_by_id(id):
    order_id = request.json['order_id']
    product_id = request.json['product_id']
    quantity = request.json['quantity']
    unit_price = request.json['unit_price']
    updated = update_detail(order_id, product_id, quantity,unit_price,id)
    return jsonify(updated), 200
# -----------------------order-detail---------------------------------
# ---------------------payment-----------------------

#Payments crud function
def get_all_Payments():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Payments')
    Payments = cur.fetchall()
    final_Payments = []
    for Payment in Payments:
        final_Payments.append({
            "id": Payment[0],
            "order_id": Payment[1],
            "payment_method": Payment[2],
            "amount": Payment[3],
            "payment_date": Payment[4],
        })
    conn.close()
    return final_Payments

def get_Payment(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Payments WHERE payment_id = ?',(id,))
    Payment = cur.fetchone()
    conn.close()
    final_Payment = {
        "payment_id": Payment[0],
        "order_id": Payment[1],
        "payment_method": Payment[2],
        "amount": Payment[3],
        "payment_date": Payment[4]
    }
    return final_Payment

def create_one_payment(order_id, payment_method, amount): 
    conn = get_db_connection() 
    cur = conn.cursor() 
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    cur.execute('INSERT INTO Payments (order_id, payment_method, amount, payment_date) VALUES (?, ?, ?, ?)', (order_id, payment_method, amount, current_datetime)) 
    conn.commit() 
    conn.close() 
    return "ok" 

def delete_payment(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Payments WHERE payment_id = ?', (id,))
    conn.commit()
    conn.close()

def update_payment(order_id, payment_method, amount,id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE Payments SET order_id = ?, payment_method = ?, amount = ? WHERE payment_id = ?', (order_id,payment_method,amount,id))
    conn.commit()
    conn.close()
    return get_Payment(id)

# Payments routes
@app.route('/Payments', methods=['GET'])
def list_Payments():
    Payments = get_all_Payments()
    response = jsonify(Payments)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(Payments)
    return response

@app.route('/Payments/<int:id>', methods=['GET'])
def Payment(id):
    Payments = get_Payment(id)
    if Payments is None:
        return '', 404
    return jsonify(Payments), 200

@app.route('/Payments', methods=['POST']) 
def create_payment(): 
    order_id = request.json['id']
    payment_method = request.json['payment_method'] 
    amount = request.json['amount'] 
    result = create_one_payment(order_id, payment_method,amount)
    return jsonify({"message": result})

@app.route('/Payments/<int:id>', methods=['DELETE'])
def delete_payment_by_id(id):
    delete_payment(id)
    return jsonify({"id":id}), 200

@app.route('/Payments/<int:id>', methods=['PUT'])
def update_payment_by_id(id):
    data = request.get_json() 
    order_id = data['order_id']
    payment_method = data['payment_method'] 
    amount = data['amount'] 
    updated = update_payment(order_id, payment_method, amount,id)
    return jsonify(updated), 200
# ---------------------payment-----------------------

if __name__ == '__main__':
    app.run(debug=True)