from sqlite3 import Cursor
from unittest import result
import mysql.connector
from mysql.connector import connection




class Db:
    """ 
    Create's a mySQL database hosted on a server and
    provides all the functions to make use of that database.

    Input:
    host: Address of host server = String.
    user: Username to access database = String.
    password: Password to access database = String .

    """
    
    def __init__(self, host, user, password) -> None:
        self.host = host
        self.user = user
        self.password = password



    def connect_db(self) -> object:
        """ Connects to the database using the details provided to the 
        class and returns the connection so it can be utilised.
        """

        conn = mysql.connector.connect(
        host = self.host,
        user = self.user,
        password = self.password,

        )

        return conn


    def create_cursor(self, conn) -> object:
        """
        Creates and returns a cursor for the mySQL connection 
        that can be used to interact with the database.

        Input:
        conn: Connection to database object.
        """ 

        cursor = conn.cursor()
        return(cursor)


    def create_db(self, cursor, database, table) -> bool:
        """
        Creates a database and table using the mySQL connection.

        Input:
        cursor: Cursor object to navigate database
        database: Name of database - String

        
        """
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            cursor.execute(f"USE {database}")
            cursor.execute(table)
            return True
        
        except:
            raise RuntimeError("Failure to create database")



    def add_data(self, cursor, product) -> bool:
        """
        A method to add a new product to the table using the mySQL 
        connection and using an Product object.  

        Input:
        cursor: Cursor object to navigate database.
        product: Product object to store in database. 
        """
        try:
            cursor.execute(f"""INSERT INTO products (productCode, productName, 
            productSupplier, productCost, productRRP, PCSL, PRSL) VALUES 
            ('{product.code}','{product.name}','{product.supplier}','{product.cost}','{product.rrp}','{product.pcsl}','{product.prsl}')""")
            return True

        except:
            raise RuntimeError("Failed to add data to database")


    def commit_data(self, conn) -> bool:
        """
        Commits the data to the table.

        Input:
        conn: Connection object for connection to database.
        """
        try:
            conn.commit()
            return True

        except:
            raise RuntimeError("Failed to commit data to database")

    def delete_all_rows(self, cursor) -> bool:
        """
        A method that deletes all the products contained in the 
        products table.
        
        Input:
        cursor: Cursor object to navigate database.
        
        """
        try:
            cursor.execute("DELETE FROM products ")
            return True

        except:
            raise RuntimeError("Failed to delete all rows")

    def delete_product(self, cursor, code) -> bool:
        """
        A method that deletes a product from the table.
        
        Input:
        cursor: Cursor object to navigate database.
        code: code of product to be deleted = String

        """
        try:
            cursor.execute(f"DELETE FROM products WHERE productCode= '{code}'")
            return True
        except:
            raise RuntimeError("Failed to delete product")


    def find_product(self, cursor, code) -> list:
        """
        A method that finds and returns the product details using the 
        product provided.

        Input:
        cursor: Cursor object to navigate database.
        code: code of product to be deleted = String

        """
        cursor.execute(f"SELECT * From products WHERE productCode= '{code}'")
        result = cursor.fetchall()
        return(result)


    def find_suppliers_products(self, cursor, supplier) -> list:
        """
        Finds and returns all the products from a particular supplier.

        Input:
        cursor: Cursor object to navigate database.
        suppler: Name of supplier - String

        """

        cursor.execute(f"""SELECT * From products WHERE 
            productSupplier= '{supplier}'""")
        result = cursor.fetchall()
        return(result)


    def find_all_products(self, cursor) -> list:
        """
        Finds and returns all the products from the database.

        Input:
        cursor: Cursor object to navigate database.

        """

        cursor.execute(f"SELECT * From products")
        result = cursor.fetchall()
        return(result)



    

    

    

