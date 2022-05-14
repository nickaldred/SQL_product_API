from itertools import product
from os import O_TEMPORARY
from flask import Flask, jsonify
from requests import request
from db import Db
from product import Product
from DataHandler import DataHandler
import simplejson as json


app = Flask(__name__)


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
    return("""Welcome to the purchasing software API. -----------
        For list of commands please see @ documentation""")

@app.route('/documentation')
def documentation():
    return("Documentation")

@app.route('/products')
def get_all_products():
    output = []
    products = database.find_all_products(cursor)
    for product in products:
            product_data = {'code' : product[0], 'name': product[1], 
            'supplier' : product[2], 'cost' : product[3], 'rrp' : product[4],
            'pcsl' : product[5], 'prsl' : product[6]}
            output.append(product_data)

    return {"products" : output}


@app.route("/product/<code>")
def get_product(code):
    product = database.find_product(cursor, code)
    if product == []:
        return("Error 404 - Not found")
    product_data = {'code' : product[0][0], 'name': product[0][1], 
            'supplier' : product[0][2], 'cost' : product[0][3], 
            'rrp' : product[0][4],
            'pcsl' : product[0][5], 'prsl' : product[0][6]}

    print(product_data)

    return (product_data)














app.run(debug=True)