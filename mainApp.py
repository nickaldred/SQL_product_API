
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



class APIApp:

    def __init__(self) -> None:
        self.app = Flask(__name__)

        #Create url rules for API
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule(
            '/documentation', 'documentation', self.documentation)
        self.app.add_url_rule(
            '/products', 'products', self.get_all_products)
        self.app.add_url_rule(
            '/product/<code>', 'product', self.get_product)
        self.app.add_url_rule(
            '/products/<supplier_name>', 'supplier_products', 
            self.get_supplier_products)
        self.app.add_url_rule(
            '/products', 'add_products', self.add_product, methods=["POST"])
        self.app.add_url_rule(
            '/products/<code>', 'delete_product', self.delete_product, 
            methods=['DELETE'])
        self.app.add_url_rule(
            '/product/<code>', 'update_product', self.update_product, 
            methods=['PUT'])
        self.app.add_url_rule(
            '/login/<username>/<password>', 'login', self.login)


        #Rate limiter for API
        self.limiter = Limiter(
            self.app,
            key_func=get_remote_address,
            default_limits=["10000 per day", "500 per hour"]
        )

        #Connects to the Postgres self.database
        self.database = Db(host="localhost",user=os.environ.get("DB_USER"), 
            password=os.environ.get("DB_PASS"))
        self.conn = self.database.connect_db()
        self.cursor = self.database.create_cursor(self.conn)
        table = """CREATE TABLE IF NOT EXISTS products
                (productCode VARCHAR(32) PRIMARY KEY, 
                productName VARCHAR(50),
                productSupplier VARCHAR(50),  
                productCost DECIMAL(19,2),
                productRRP DECIMAL(19,2),
                PCSL SMALLINT,
                PRSL SMALLINT
                )"""
        self.database.create_db(self.cursor, "postgres", table)


    def index(self) -> json:
        """
        API landing page.

        """
        return jsonify({'message' : """Welcome to the purchasing software API. 
            ----------- For list of commands please see /documentation"""})


    def documentation(self) -> object:
        """
        Displays the documentation on how to use the API.

        """
        workingdir = os.path.abspath(os.getcwd())
        filepath = workingdir + '/static/files'
        return send_from_directory(filepath, 'documentation.txt')


    @token_required
    def get_all_products(self) -> json:
        """
        Returns all the products in the SQL self.database in JSON 
        format.

        """

        output = []
        products = self.database.find_all_products(self.cursor)

        for product in products:
                product_data = {'code' : product[0], 'name': product[1], 
                'supplier' : product[2], 'cost' : product[3], 
                'rrp' : product[4],'pcsl' : product[5], 'prsl' : product[6]}
                output.append(product_data)

        return (jsonify(output))


    #@token_required
    def get_product(self, code) -> json:
        """
        Returns a singular product using the product code.

        Input:
        code -> String - Code of product to be found.

        """

        product = self.database.find_product(self.cursor, code)

        #Error checking
        if product == []:
            return jsonify({"Product not found" : 404})

        product_data = {'code' : product[0][0], 'name': product[0][1], 
                'supplier' : product[0][2], 'cost' : product[0][3], 
                'rrp' : product[0][4],
                'pcsl' : product[0][5], 'prsl' : product[0][6]}

        return (jsonify([product_data]))


    #@token_required
    def get_supplier_products(self, supplier_name) -> json:
        """
        Returns all products from a particular supplier.

        Input:
        supplier_name -> String - Supplier to be searched for.
        
        """
        #Converts underscores to space's
        supplier_name = supplier_name.replace("_", " ")

        output = []
        products = self.database.find_suppliers_products(self.cursor, 
            supplier_name)

        for product in products:
                product_data = {'code' : product[0], 'name': product[1], 
                'supplier' : product[2], 'cost' : product[3], 
                'rrp' : product[4], 'pcsl' : product[5], 'prsl' : product[6]}
                output.append(product_data)
        
        if output == []:
            return jsonify({"Supplier not found": 404})

        return jsonify(output)


    #@token_required
    def add_product(self) -> json:
        """
        Using the provided JSON data, adds a new product to the SQL 
        self.database.

        Input:
        JSON data of new product.
        
        """

        #Gathers data from request.
        product = Product(code=request.json['code'], 
        name=request.json['name'], supplier=request.json['supplier'], 
        cost=request.json['cost'], rrp=request.json['rrp'], 
        pcsl=request.json['pcsl'], prsl=request.json['prsl'])

        self.database.add_data(self.cursor, product)
        self.database.commit_data(self.conn)
        return jsonify({"Added product" : product.code})


    #@token_required
    def delete_product(self, code) -> json:
        """
        Using a provided product code, deletes that product from the 
        SQL self.database.

        Input:
        code -> String - Code of product to be deleted.

        """

        self.database.delete_product(self.cursor, code)
        self.database.commit_data(self.conn)
        return jsonify({'message' : 'Deleted product'})


    def update_product(self, code) -> json:
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

        self.database.update_product(self.cursor, code, 
            column, data_to_update)
        self.database.commit_data(conn=self.conn)

        return(self.get_product(code))


    def login(self, username, password) -> json:
        """
        Creates a token after a succesful login so the API can be 
        accessed.

        Input:
        Username - String 
        Password - String
        
        """

        if (username and password == os.environ.get("PASSWORD") and 
                os.environ.get("USER_NAME") == username):

            #Creates a token with 120 mins to expire.
            token = jwt.encode({'user' : username, 
            'exp' : datetime.datetime.utcnow() + 
                datetime.timedelta(minutes=120)},
            os.environ.get("SECRET_KEY"))
            
            return jsonify({'token' : token})

        return make_response('Could not verify!', 401, 
            {'WWW-Authenticate' : 'Basic realm="Login Required"'})





if __name__ == "__main__":

    load_dotenv()

    apiApp = APIApp()
        
    apiApp.app.run(host="127.0.0.2", debug=True)