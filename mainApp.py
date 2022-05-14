from itertools import product
from os import O_TEMPORARY
from flask import Flask, jsonify, request
from db import Db
from product import Product
from DataHandler import DataHandler
import simplejson as json


app = Flask(__name__)

#Connects to the MySQL database
database = Db(host="localhost",user="root", password="test123")
conn = database.connect_db()
cursor = database.create_cursor(conn)
table = """CREATE TABLE IF NOT EXISTS products
        (productCode VARCHAR(32) PRIMARY KEY, 
        productName VARCHAR(50),
        productSupplier VARCHAR(50),  
        productCost DECIMAL(19,2),
        productRRP DECIMAL(19,2),
        PCSL SMALLINT(32),
        PRSL SMALLINT(32)
        )"""
database.create_db(cursor, "purchasing_program", table)



@app.route('/')
def index():
    """
    API landing page.

    """
    return("""Welcome to the purchasing software API. -----------
        For list of commands please see @ documentation""")


@app.route('/documentation')
def documentation():
    """
    Displays the documentation on how to use the API.

    """
    return("Documentation")


@app.route('/products')
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
def get_product(code) -> json:
    """
    Returns a singular product using the product code.

    Input:
    code -> String - Code of product to be found.

    """

    product = database.find_product(cursor, code)

    #Error checking
    if product == []:
        return("Error 404 - Not found")

    product_data = {'code' : product[0][0], 'name': product[0][1], 
            'supplier' : product[0][2], 'cost' : product[0][3], 
            'rrp' : product[0][4],
            'pcsl' : product[0][5], 'prsl' : product[0][6]}

    return (jsonify([product_data]))


@app.route("/products/<supplier_name>")
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

    return jsonify(output)


@app.route("/products", methods=["POST"])
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
    return({"Added product" : product.code})


@app.route("/products/<code>", methods=['DELETE'])
def delete_product(code):
    """
    Using a provided product code, deletes that product from the 
    SQL database.

    Input:
    code -> String - Code of product to be deleted.

    """

    database.delete_product(cursor, code)
    return("Deleted product")
















app.run(debug=True)