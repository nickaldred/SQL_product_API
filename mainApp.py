
from flask import Flask, jsonify, request, make_response, send_from_directory
from db import Db
from product import Product
import simplejson as json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import datetime
import jwt
from dotenv import load_dotenv
import os
from decorators import token_required

app = Flask(__name__)

@app.route('/')
def index():
    """
    API landing page.

    """
    return jsonify({'message' : """Welcome to the purchasing software API. 
        ----------- For list of commands please see /documentation"""})


@app.route('/documentation')
def documentation():
    """
    Displays the documentation on how to use the API.

    """
    workingdir = os.path.abspath(os.getcwd())
    filepath = workingdir + '/static/files'
    return send_from_directory(filepath, 'documentation.txt')


@app.route('/products')
#@token_required
def get_all_products() -> json:
    """
    Returns all the products in the SQL database in JSON format.

    """

    output = []
    products = database.find_all_products(cursor)

    for product in products:
            product_data = {'code' : product[0], 'name': product[1], 
            'supplier' : product[2], 'cost' : product[3], 'rrp' : product[4],
            'pcsl' : product[5], 'prsl' : product[6]}
            output.append(product_data)

    return (jsonify(output))


@app.route("/product/<code>")
#@token_required
def get_product(code) -> json:
    """
    Returns a singular product using the product code.

    Input:
    code -> String - Code of product to be found.

    """

    product = database.find_product(cursor, code)

    #Error checking
    if product == []:
        return jsonify({"Product not found" : 404})

    product_data = {'code' : product[0][0], 'name': product[0][1], 
            'supplier' : product[0][2], 'cost' : product[0][3], 
            'rrp' : product[0][4],
            'pcsl' : product[0][5], 'prsl' : product[0][6]}

    return (jsonify([product_data]))


@app.route("/products/<supplier_name>")
#@token_required
def get_supplier_products(supplier_name) -> json:
    """
    Returns all products from a particular supplier.

    Input:
    supplier_name -> String - Supplier to be searched for.
    
    """
    #Converts underscores to space's
    supplier_name = supplier_name.replace("_", " ")

    output = []
    products = database.find_suppliers_products(cursor, supplier_name)

    for product in products:
            product_data = {'code' : product[0], 'name': product[1], 
            'supplier' : product[2], 'cost' : product[3], 'rrp' : product[4],
            'pcsl' : product[5], 'prsl' : product[6]}
            output.append(product_data)
    
    if output == []:
        return jsonify({"Supplier not found": 404})

    return jsonify(output)


@app.route("/products", methods=["POST"])
#@token_required
def add_product():
    """
    Using the provided JSON data, adds a new product to the SQL 
    database.

    Input:
    JSON data of new product.
    
    """

    #Gathers data from request.
    product = Product(code=request.json['code'], name=request.json['name'],
    supplier=request.json['supplier'], cost=request.json['cost'], 
    rrp=request.json['rrp'], pcsl=request.json['pcsl'], 
    prsl=request.json['prsl'])

    database.add_data(cursor, product)
    database.commit_data(conn)
    return jsonify({"Added product" : product.code})


@app.route("/product/<code>", methods=['DELETE'])
#@token_required
def delete_product(code):
    """
    Using a provided product code, deletes that product from the 
    SQL database.

    Input:
    code -> String - Code of product to be deleted.

    """

    database.delete_product(cursor, code)
    database.commit_data(conn)
    return jsonify({'message' : 'Deleted product'})


@app.route("/product/<code>", methods=['PUT'])
def update_product(code):
    """
    Updates any column of the table with the provided input data.

    Inputs:
    code - String - Product to update.

    column - String - column to update.
    value - Data type varies depending on column - Value to update
            column with.
    
    """
    
    column = request.json['column']
    data_to_update = request.json['value']

    database.update_product(cursor, code, column, data_to_update)
    database.commit_data(conn=conn)

    return(get_product(code))



@app.route('/login')
def login():
    """
    Creates a token after a succesful login so the API can be accessed.

    Input:
    Username - String 
    Password - String
    
    """

    #Request login credentials from the user.
    auth = request.authorization

    if auth and auth.password == os.environ.get("PASSWORD") and os.environ.get("USER_NAME") == auth.username:
        #Creates a token with 120 mins to expire.
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=120)}, os.environ.get("SECRET_KEY"))
        return jsonify({'token' : token})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})





if __name__ == "__main__":

    load_dotenv()

    #Connects to the Postgres database
    database = Db(host="localhost",user=os.environ.get("DB_USER"), 
        password=os.environ.get("DB_PASS"))
    conn = database.connect_db()
    cursor = database.create_cursor(conn)
    table = """CREATE TABLE IF NOT EXISTS products
            (productCode VARCHAR(32) PRIMARY KEY, 
            productName VARCHAR(50),
            productSupplier VARCHAR(50),  
            productCost DECIMAL(19,2),
            productRRP DECIMAL(19,2),
            PCSL SMALLINT,
            PRSL SMALLINT
            )"""
    database.create_db(cursor, "postgres", table)


    #Rate limiter for API
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["10000 per day", "500 per hour"]
    )
        
    app.run(host="127.0.0.2", debug=True)